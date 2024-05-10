# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/16 11:14
@Author  : itlubber
@Site    : itlubber.art
"""
import os
import numpy as np
import pandas as pd

import h2o
from h2o.automl import H2OAutoML
from h2o.estimators import H2ORuleFitEstimator

from .utils import init_setting
from .excel_writer import ExcelWriter, dataframe2excel


h2o.init()


class H2oRuleExtractor:

    def __init__(self, target="target", labels=["positive", "negative"], feature_map={}, nan=-1., max_iter=128, writer=None, combiner=None, seed=None, theme_color="2639E9"):
        """决策树自动规则挖掘工具包

        :param target: 数据集中好坏样本标签列名称，默认 target
        :param labels: 好坏样本标签名称，传入一个长度为2的列表，第0个元素为好样本标签，第1个元素为坏样本标签，默认 ["positive", "negative"]
        :param feature_map: 变量名称及其含义，在后续输出报告和策略信息时增加可读性，默认 {}
        :param nan: 在决策树策略挖掘时，默认空值填充的值，默认 -1
        :param max_iter: 最多支持在数据集上训练多少颗树模型，每次生成一棵树后，会剔除特征重要性最高的特征后，再生成树，默认 128
        :param writer: 在之前程序运行时生成的 ExcelWriter，可以支持传入一个已有的writer，后续所有内容将保存至该workbook中，默认 None
        """
        self.seed = seed
        self.nan = nan
        self.target = target
        self.labels = labels
        self.theme_color = theme_color
        self.feature_map = feature_map
        self.decision_trees = []
        self.max_iter = max_iter
        self.target_enc = None
        self.feature_names = None
        self.dt_rules = pd.DataFrame()
        self.end_row = 2
        self.start_col = 2
        self.describe_columns = ["组合策略", "命中数", "命中率", "好样本数", "好样本占比", "坏样本数", "坏样本占比", "坏率", "样本整体坏率", "LIFT值"]

        init_setting()

        if writer:
            self.writer = writer
        else:
            self.writer = ExcelWriter(theme_color=self.theme_color)

    def fit(self, x, max_depth=2, lift=0., max_samples=1., min_score=None, verbose=False, *args, **kwargs):
        """组合策略挖掘

        :param x: 包含标签的数据集
        :param max_depth: 决策树最大深度，即最多组合的特征个数，默认 2
        :param lift: 组合策略最小的lift值，默认 0.，即全部组合策略
        :param max_samples: 每条组合策略的最大样本占比，默认 1.0，即全部组合策略
        :param min_score: 决策树拟合时最小的auc，如果不满足则停止后续生成决策树
        :param verbose: 是否调试模式，仅在 jupyter 环境有效
        :param kwargs: H2ORuleFitEstimator 参数，参考
        """
        worksheet = self.writer.get_sheet_by_name("策略详情")

        y = x[self.target]
        X_TE = self.encode_cat_features(x.drop(columns=[self.target]), y)
        X_TE = X_TE.fillna(self.nan)

        self.feature_names = list(X_TE.columns)

        for i in range(self.max_iter):
            decision_tree = DecisionTreeClassifier(max_depth=max_depth, *args, **kwargs)
            decision_tree = decision_tree.fit(X_TE, y)

            if (min_score is not None and decision_tree.score(X_TE, y) < min_score) or len(X_TE.columns) < max_depth:
                break

            try:
                parsed_rules, remove, total_rules = self.select_dt_rules(decision_tree, X_TE, y, lift=lift, max_samples=max_samples, verbose=verbose, save=f"model_report/auto_mining_rules/combiner_rules_{i}.png", drop=True)

                if len(parsed_rules) > 0:
                    self.dt_rules = pd.concat([self.dt_rules, parsed_rules]).reset_index(drop=True)

                    if self.writer is not None:
                        if self.feature_map is not None and len(self.feature_map) > 0:
                            parsed_rules["组合策略"] = parsed_rules["组合策略"].replace(self.feature_map, regex=True)
                        self.end_row, _ = self.insert_dt_rules(parsed_rules, self.end_row, self.start_col, save=f"model_report/auto_mining_rules/combiner_rules_{i}.png", figsize=(500, 100 * total_rules), sheet=worksheet)

                X_TE = X_TE.drop(columns=remove)
                self.decision_trees.append(decision_tree)
            except:
                import traceback
                traceback.print_exc()

        if len(self.dt_rules) <= 0:
            print(f"未挖掘到有效策略, 可以考虑适当调整预设的筛选参数, 降低 lift / 提高 max_samples, 当前筛选标准为: 提取 lift >= {lift} 且 max_samples <= {max_samples} 的策略")

        return self
