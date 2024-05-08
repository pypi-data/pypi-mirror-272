# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd

from promptflow.evals.evaluate._utils import load_jsonl

LOGGER = logging.getLogger(__name__)


class CodeRun:
    def __init__(self, run, column_mapping, input_data, evaluator_name=None, **kwargs):
        self.run = run
        self.column_mapping = column_mapping
        self.evaluator_name = evaluator_name if evaluator_name is not None else ""
        self.input_data = input_data

    def get_result_df(self, exclude_inputs=False):
        result_df = self.run.result(timeout=60 * 60)
        if exclude_inputs:
            result_df = result_df.drop(columns=[col for col in result_df.columns if col.startswith("inputs.")])
        return result_df


class CodeClient:
    def __init__(self):
        self._thread_pool = ThreadPoolExecutor(thread_name_prefix="evaluators_thread")

    def _calculate_metric(self, evaluator, input_df, column_mapping, evaluator_name):
        row_metric_futures = []
        row_metric_results = []
        input_df = input_df.rename(columns={v: k for k, v in column_mapping.items()}) if column_mapping else input_df
        for value in input_df.to_dict("records"):
            row_metric_futures.append(self._thread_pool.submit(evaluator, **value))

        for row_number, row_metric_future in enumerate(row_metric_futures):
            try:
                row_metric_results.append(row_metric_future.result())
            except Exception as ex:  # pylint: disable=broad-except
                msg_1 = f"Error calculating value for row {row_number} for metric {evaluator_name}, "
                msg_2 = f"failed with error {str(ex)} : Stack trace : {str(ex.__traceback__)}"
                LOGGER.info(msg_1 + msg_2)
                # If a row fails to calculate, add an empty dict to maintain the row index
                # This is to ensure the output dataframe has the same number of rows as the input dataframe
                # pd concat will fill NaN for missing values
                row_metric_results.append({})

        return pd.concat(
            [
                input_df.add_prefix("inputs."),
                pd.DataFrame(row_metric_results).add_prefix(
                    f"outputs.{evaluator_name}." if evaluator_name else "outputs."
                ),
            ],
            axis=1,
            verify_integrity=True,
        )

    def run(self, flow, data, evaluator_name=None, column_mapping=None, **kwargs):
        try:
            json_data = load_jsonl(data)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to parse data as JSON: {data}. Please provide a valid json lines data.")

        input_df = pd.DataFrame(json_data)
        if column_mapping:
            input_df.rename(columns={v: k for k, v in column_mapping.items()}, inplace=True)
        eval_future = self._thread_pool.submit(self._calculate_metric, flow, input_df, column_mapping, evaluator_name)
        return CodeRun(run=eval_future, column_mapping=column_mapping, input_data=data, evaluator_name=evaluator_name)

    def get_details(self, run, all_results=False):
        result_df = run.run.result(timeout=60 * 60)
        return result_df
