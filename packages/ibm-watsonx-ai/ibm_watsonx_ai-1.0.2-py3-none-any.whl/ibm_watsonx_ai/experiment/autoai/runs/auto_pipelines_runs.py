#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

__all__ = [
    "AutoPipelinesRuns"
]


from copy import deepcopy
from typing import List, Dict, Union, Optional
import warnings

from pandas import DataFrame

from ibm_watsonx_ai.experiment.autoai.engines import WMLEngine, ServiceEngine
from ibm_watsonx_ai.experiment.autoai.optimizers import RemoteAutoPipelines
from ibm_watsonx_ai.utils.autoai.utils import NextRunDetailsGenerator, get_node_and_runtime_index
from ibm_watsonx_ai.helpers import DataConnection, S3Location, AssetLocation
from ibm_watsonx_ai.utils.autoai.enums import ForecastingPipelineTypes
from .base_auto_pipelines_runs import BaseAutoPipelinesRuns
from ibm_watsonx_ai.wml_client_error import ApiRequestFailure


class AutoPipelinesRuns(BaseAutoPipelinesRuns):
    """AutoPipelinesRuns class is used to work with historical Optimizer runs.

    :param engine: Engine to handle Service operations
    :type engine:  ServiceEngine or WMLEngine (deprecated)

    :param filter: filter, user can choose which runs to fetch specifying AutoPipelines name
    :type filter: str, optional
    """

    def __init__(self, engine: Union['WMLEngine', 'ServiceEngine'], filter: str = None) -> None:
        self._engine: Union['WMLEngine', 'ServiceEngine'] = engine
        self.auto_pipeline_optimizer_name = filter
        self._workspace = None

    @property
    def _wml_engine(self):
        # note: backward compatibility
        warnings.warn(("`_wml_engine` is deprecated and will be removed in future. "
                "Instead, please use `_engine`."), category=DeprecationWarning)
        
        # --- end note
        return self._engine
    
    def __call__(self, *, filter: str = None) -> 'AutoPipelinesRuns':
        self.auto_pipeline_optimizer_name = filter
        return self

    def list(self) -> 'DataFrame':
        """Lists historical runs/fits with status. If user has a lot of runs stored,
        it may take long time to fetch all the information.

        :return: Pandas DataFrame with runs IDs and state
        :rtype: pandas.DataFrame
        """

        columns = ['timestamp', 'run_id', 'state', 'auto_pipeline_optimizer name']

        # note: download all runs details
        client = self._engine._api_client if isinstance(self._engine, ServiceEngine) else self._engine._wml_client
        runs_details = client.training.get_details(get_all=True if self.auto_pipeline_optimizer_name else False,
                                                   limit=None if self.auto_pipeline_optimizer_name else 50,
                                                   training_type='pipeline',
                                                   _internal=True)
        data = runs_details.get('resources', [])

        # note: some of the pending experiments do not have these information (checking with if statement)
        runs_pipeline_ids = [run['entity']['pipeline']['id'] for run in data if
                             run['entity'].get('pipeline', {}).get('id')]
        runs_timestamps = [run['metadata'].get('modified_at') for run in data if
                           run['entity'].get('pipeline', {}).get('id')]
        data = [run for run in data if run['entity'].get('pipeline', {}).get('id')]
        # --- end note


        def get_value(pipeline_id, timestamp, run):
            try:
                client = self._engine._api_client if isinstance(self._engine, ServiceEngine) else self._engine._wml_client
                pipeline_details = client.pipelines.get_details(pipeline_id=pipeline_id)
            except ApiRequestFailure:
                pipeline_details = {'metadata': {'name': 'Experiment data is missing...'}}

            if self.auto_pipeline_optimizer_name and pipeline_details['metadata']['name'] != self.auto_pipeline_optimizer_name:
                return None

            if not ('automl' in str(pipeline_details) or 'autoai-ts' in str(pipeline_details)) or not 'hybrid' in str(pipeline_details):
                return None

            pipeline_name = pipeline_details['metadata'].get('name', 'Unknown')

            return [timestamp, run['metadata'].get('id', run['metadata'].get('guid')), run['entity']['status']['state'],
                 pipeline_name]

        values = []
        for pipeline_id, timestamp, run in zip(runs_pipeline_ids, runs_timestamps, data):
            v = get_value(pipeline_id, timestamp, run)
            if v:
                values.append(v)
            if len(values) >= 50:
                break

        self.auto_pipeline_optimizer_name = None
        runs = DataFrame(data=values, columns=columns)
        return runs.sort_values(by=["timestamp"], ascending=False)[:50]

    def get_params(self, run_id: str = None) -> dict:
        """Get executed optimizers configs parameters based on the run_id.

        :param run_id: ID of the fit/run, if not specified, latest is taken
        :type run_id: str, optional

        :return: optimizer configuration parameters
        :rtype: dict

        **Example**

        .. code-block:: python

            from ibm_watsonx_ai.experiment import AutoAI
            experiment = AutoAI(credentials, ...)

            experiment.runs.get_params(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
            experiment.runs.get_params()

            # Result:
            # {
            #     'name': 'test name',
            #     'desc': 'test description',
            #     'prediction_type': 'classification',
            #     'prediction_column': 'y',
            #     'scoring': 'roc_auc',
            #     'holdout_size': 0.1,
            #     'max_num_daub_ensembles': 1
            # }
        """
        client = self._engine._api_client if isinstance(self._engine, ServiceEngine) else self._engine._wml_client
        if run_id is None:
            
            optimizer_id = client.training.get_details(
                limit=1, training_type='pipeline', _internal=True
                ).get('resources')[0]['entity']['pipeline']['id']

        else:
            optimizer_id = client.training.get_details(
                training_id=run_id, _internal=True
                ).get('entity')['pipeline']['id']

        optimizer_config = client.pipelines.get_details(pipeline_id=optimizer_id)

        # note: if experiment has more than 1 node (e.g. KB + sth), we need to find which one is KB
        kb_node_number, kb_runtime_number = get_node_and_runtime_index(node_name='kb',
                                                                       optimizer_config=optimizer_config)
        # --- end note

        # note: try to find ts node
        ts_node_number, ts_runtime_number = get_node_and_runtime_index(node_name='ts',
                                                                       optimizer_config=optimizer_config)
        # --- end note

        # note: try to find tsad node
        tsad_node_number, tsad_runtime_number = get_node_and_runtime_index(node_name='tsad',
                                                                           optimizer_config=optimizer_config)
        # --- end note

        try:
            name = optimizer_config['entity']['name']
            description = optimizer_config['entity'].get('description', '')

        except KeyError:
            name = optimizer_config['metadata']['name']
            description = optimizer_config['metadata'].get('description', '')

        # note: check if not only data preprocessing experiment
        if kb_node_number is not None:
            autoai_parameters = optimizer_config['entity']['document']['pipelines'][0]['nodes'][kb_node_number][
                'parameters']
            kb_parameters = autoai_parameters['optimization']
            kb_data = optimizer_config['entity']['document']['runtimes'][kb_runtime_number]['app_data']['wml_data']

            csv_separator = autoai_parameters.get('input_file_separator', ',')
            excel_sheet = autoai_parameters.get('excel_sheet', None)
            encoding = autoai_parameters.get('encoding', 'utf-8')
            drop_duplicates = autoai_parameters.get('drop_duplicates', True)

            params = {
                'name': name,
                'desc': description,
                'prediction_type': kb_parameters['learning_type'],
                'prediction_column': kb_parameters.get('label'),
                'prediction_columns': kb_parameters.get('target_columns'),
                'timestamp_column_name': kb_parameters.get('timestamp_column'),
                'holdout_size': kb_parameters.get('holdout_param'),
                'max_num_daub_ensembles': kb_parameters.get('max_num_daub_ensembles'),
                't_shirt_size': kb_data['hardware_spec']['id'],
                'include_only_estimators': kb_parameters.get('daub_include_only_estimators'),
                'cognito_transform_names': kb_parameters.get('cognito_transform_names'),
                'train_sample_rows_test_size': kb_parameters.get('train_sample_rows_test_size'),
                'text_processing': kb_parameters.get('text_processing_flag'),
                'train_sample_columns_index_list': kb_parameters.get('train_sample_columns_index_list'),
                'daub_give_priority_to_runtime': kb_parameters.get('daub_runtime_ranking_power'),
                'positive label': kb_parameters.get('daub_runtime_ranking_power'),
                'incremental_learning': kb_parameters.get('incremental_learning'),
                'early_stop_enabled': kb_parameters.get('early_stop_enabled'),
                'early_stop_window_size': kb_parameters.get('early_stop_window_size'),
                'outliers_columns': kb_parameters.get('outliers_columns'),
                'numerical_columns': kb_parameters.get('numerical_columns'),
                'categorical_columns': kb_parameters.get('categorical_columns'),
                'time_ordered_data': kb_parameters.get('time_ordered_data'),
                'feature_selector_mode': kb_parameters.get('feature_selector_mode'),
                'test_data_csv_separator': autoai_parameters.get('input_file_separator', ','),
                'test_data_excel_sheet': autoai_parameters.get('test_excel_sheet', None),
                'test_data_encoding': autoai_parameters.get('test_encoding', 'utf-8'),
                'drop_duplicates': drop_duplicates,
                'csv_separator': csv_separator,
                'excel_sheet': excel_sheet,
                'encoding': encoding,
                'retrain_on_holdout': kb_parameters.get('retrain_on_holdout')
            }

            if kb_parameters.get('train_sample_rows_test_size'):
                params['train_sample_rows_test_size'] = kb_parameters['train_sample_rows_test_size']
            if kb_parameters.get('scorer_for_ranking'):
                params['scoring'] = kb_parameters['scorer_for_ranking']
            if kb_parameters.get('text_processing_options') and kb_parameters['text_processing_options'].get(
                    'word2vec'):
                params['word2vec_feature_number'] = kb_parameters['text_processing_options']['word2vec'].get(
                    'output_dim')
            if kb_parameters.get('fairness_info'):
                params['fairness_info'] = kb_parameters.get('fairness_info')
        elif ts_node_number is not None:
            ts_parameters = optimizer_config['entity']['document']['pipelines'][0]['nodes'][ts_node_number][
                'parameters']['optimization']
            ts_data = optimizer_config['entity']['document']['runtimes'][ts_node_number]['app_data']['wml_data']

            csv_separator = optimizer_config['entity']['document']['pipelines'][0]['nodes'][ts_node_number][
                'parameters'].get('input_file_separator', ',')
            encoding = optimizer_config['entity']['document']['pipelines'][0]['nodes'][ts_node_number][
                'parameters'].get('encoding', 'utf-8')

            if ts_parameters.get('pipeline_type') == 'customized':
                pipeline_types = ts_parameters.get('customized_pipelines')
                pipeline_types = [ForecastingPipelineTypes(p) for p in pipeline_types]
            elif ts_parameters.get('pipeline_type') == 'exogenous':
                pipeline_types = ForecastingPipelineTypes.get_exogenous()
            elif ts_parameters.get('pipeline_type') == 'non_exogenous':
                pipeline_types = ForecastingPipelineTypes.get_non_exogenous()
            elif ts_parameters.get('pipeline_type') == 'all':
                pipeline_types = [l for l in ForecastingPipelineTypes]
            else:
                pipeline_types = None

            params = {
                'name': name,
                'desc': description,
                'prediction_type': ts_parameters['learning_type'],
                'prediction_column': ts_parameters.get('label'),
                'prediction_columns': ts_parameters.get('target_columns'),
                'timestamp_column_name': ts_parameters.get('timestamp_column'),
                'holdout_size': ts_parameters.get('holdout_param', 20),
                'max_num_daub_ensembles': ts_parameters.get('max_num_daub_ensembles', 3),
                'backtest_gap_length': ts_parameters.get('gap_len'),
                'backtest_num': ts_parameters.get('num_backtest'),
                'forecast_window': ts_parameters.get('prediction_horizon'),
                'include_only_estimators': ts_parameters.get('include_only_estimators'),
                'lookback_window': ts_parameters.get('lookback_window'),
                't_shirt_size': ts_data['hardware_spec']['id'],
                'csv_separator': csv_separator,
                'encoding': encoding,
                'feature_columns': ts_parameters.get('feature_columns'),
                'supporting_features_at_forecast': ts_parameters.get('future_exogenous_available'),
                'pipeline_types': pipeline_types,
                'retrain_on_holdout': ts_parameters.get('retrain_on_holdout', True),
            }
        elif tsad_node_number is not None:
            tsad_parameters = optimizer_config['entity']['document']['pipelines'][0]['nodes'][tsad_node_number][
                'parameters']['optimization']
            tsad_data = optimizer_config['entity']['document']['runtimes'][tsad_node_number]['app_data']['wml_data']

            csv_separator = optimizer_config['entity']['document']['pipelines'][0]['nodes'][tsad_node_number][
                'parameters'].get('input_file_separator', ',')
            encoding = optimizer_config['entity']['document']['pipelines'][0]['nodes'][tsad_node_number][
                'parameters'].get('encoding', 'utf-8')

            params = {
                'name': name,
                'desc': description,
                'prediction_type': tsad_parameters.get('learning_type'),
                'feature_columns': tsad_parameters.get('feature_columns'),
                'prediction_column': tsad_parameters.get('label'),
                'prediction_columns': tsad_parameters.get('target_columns'),
                'timestamp_column_name': tsad_parameters.get('timestamp_column'),
                'holdout_size': tsad_parameters.get('holdout_param', 0.2),
                'max_num_daub_ensembles': tsad_parameters.get('max_num_pipelines', 3),
                'include_only_estimators': tsad_parameters.get('daub_include_only_estimators'),
                't_shirt_size': tsad_data['hardware_spec']['id'],
                'csv_separator': csv_separator,
                'encoding': encoding,
                'pipeline_types': tsad_parameters.get('pipelines'),
                'retrain_on_holdout': tsad_parameters.get('retrain_on_holdout', True),
                'scoring': tsad_parameters.get('evaluation_metric', 'average_precision'),
                # 'confidence_level': tsad_parameters.get('confidence_level', 0.95),
            }
        else:
            params = {
                'name': name,
                'desc': description,
                'prediction_type': None,
                'prediction_column': None,
                'prediction_columns': None,
                'timestamp_column_name': None,
                'scoring': None,
            }
        # --- end note

        return params

    def get_run_details(self, run_id: str = None) -> dict:
        """Get run details. If run_id is not supplied, last run will be taken.

        :param run_id: ID of the fit/run
        :type run_id: str, optional

        :return: run configuration parameters
        :rtype: dict

        **Example**

        .. code-block:: python

            from ibm_watsonx_ai.experiment import AutoAI
            experiment = AutoAI(credentials, ...)

            experiment.runs.get_run_details(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
            experiment.runs.get_run_details()
        """
        client = self._engine._api_client if isinstance(self._engine, ServiceEngine) else self._engine._wml_client
        if run_id is None:
            details = client.training.get_details(limit=1, 
                                                  training_type='pipeline', 
                                                  _internal=True).get('resources')[0]

        else:
            details = client.training.get_details(training_id=run_id, _internal=True)

        if details['entity']['status'].get('metrics', False):
            del details['entity']['status']['metrics']
            return details
        else:
            return details

    def get_optimizer(self,
                      run_id: Optional[str] = None,
                      metadata: Dict[str, Union[List['DataConnection'], 'DataConnection', str, int]] = None
                      ) -> 'RemoteAutoPipelines':
        """Create instance of AutoPipelinesRuns with all computed pipelines computed by AutoAI.

        :param run_id: ID of the fit/run
        :type run_id: str, optional

        :param metadata: option to pass information about COS data reference
        :type metadata: dict, optional

        :return: optimizer object
        :rtype: AutoPipelinesRuns class instance

        **Example**

        .. code-block:: python

            from ibm_watsonx_ai.experiment import AutoAI
            experiment = AutoAI(credentials, ...)

            historical_optimizer = experiment.runs.get_optimizer(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
        """
        # note: normal scenario
        if metadata is None:
            optimizer_parameters = self.get_params(run_id=run_id)

            remote_pipeline_optimizer = RemoteAutoPipelines(**optimizer_parameters, engine=self._engine)

            remote_pipeline_optimizer._engine._current_run_id = run_id
            remote_pipeline_optimizer._workspace = self._workspace

            return remote_pipeline_optimizer
        # --- end note

        # note: Cloud auto-gen notebook scenario (when user provides his credentials)
        else:
            from ibm_watsonx_ai.experiment import AutoAI
            training_result_reference = metadata.get('training_result_reference')

            # note: check for cloud
            if isinstance(training_result_reference.location, (S3Location, AssetLocation)):
                run_id = training_result_reference.location._training_status.split('/')[-2]
            else:
                run_id = training_result_reference.location.path.split('/')[-3]

            # note: CP4D notebook scenario
            if self._engine is not None:
                return AutoAI(self._workspace).runs.get_optimizer(run_id)

        # --- end note

    def get_data_connections(self, run_id: str) -> List['DataConnection']:
        """Create DataConnection objects for further user usage
            (eg. to handle data storage connection or to recreate autoai holdout split).

        :param run_id: ID of the historical fit/run
        :type run_id: str

        :return: list of DataConnections with populated optimizer parameters
        :rtype: list['DataConnection']

        **Example**

        .. code-block:: python

            from ibm_watsonx_ai.experiment import AutoAI
            experiment = AutoAI(credentials, ...)

            data_connections = experiment.runs.get_data_connections(run_id='02bab973-ae83-4283-9d73-87b9fd462d35')
        """
        optimizer_parameters = self.get_params(run_id=run_id)
        training_data_references = self.get_run_details(run_id=run_id)['entity']['training_data_references']

        data_connections = [
            DataConnection._from_dict(_dict=data_connection) for data_connection in training_data_references]

        for data_connection in data_connections:  # note: populate DataConnections with optimizer params
            data_connection.auto_pipeline_params = deepcopy(optimizer_parameters)
            client = self._engine._api_client if isinstance(self._engine, ServiceEngine) else self._engine._wml_client
            data_connection.set_client(client)
            data_connection._run_id = run_id

        return data_connections
