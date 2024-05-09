from typing import Union, List, Optional

from baram.s3_manager import S3Manager
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.core import ExpectationSuite, ExpectationConfiguration
from great_expectations.core import ExpectationSuiteValidationResult
from great_expectations.core import ExpectationValidationResult
from great_expectations.core.batch import Batch
from great_expectations.data_context import EphemeralDataContext
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.data_context.types.resource_identifiers import GXCloudIdentifier
from great_expectations.dataset import Dataset
from great_expectations.datasource.fluent.pandas_datasource import CSVAsset
from great_expectations.datasource.fluent.sql_datasource import TableAsset
from great_expectations.exceptions import DataContextError
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.validator.validator import Validator


class Dolbaram(object):
    def __init__(self, gx_s3_bucket_name: str, data_s3_bucket_name: str, athena_workgroup: Optional[str] = None):
        '''

        :param data_s3_bucket_name:
        '''

        self.DATASOURCE_S3_PANDAS_NAME = 's3'
        self.DATASOURCE_S3_SPARK_NAME = 'spark'
        self.DATASOURCE_ATHENA_NAME = 'athena'
        self.DATA_CONNECTOR_NAME = 'default_inferred_data_connector_name'
        self.GX_S3_BUCKET_NAME = gx_s3_bucket_name
        self.DATA_S3_BUCKET_NAME = data_s3_bucket_name
        self.DATA_S3_BUCKET_PREFIX = 'incoming'
        self.S3_EXPECTATION_STORE_DIR = 'expectations'
        self.S3_VALIDATION_STORE_DIR = 'uncommitted/validations'
        self.S3_CHECKPOINT_STORE_DIR = 'checkpoint'
        self.S3_PROFILER_STORE_DIR = 'profiler'
        self.S3_METRIC_STORE_DIR = 'metric'

        self.data_context_config = DataContextConfig(
            config_version=3,
            plugins_directory=None,
            config_variables_file_path=None,
            stores={
                'expectations_store': {
                    'class_name': 'ExpectationsStore',
                    'store_backend': {
                        'class_name': 'TupleS3StoreBackend',
                        'bucket': self.GX_S3_BUCKET_NAME,
                        'prefix': self.S3_EXPECTATION_STORE_DIR
                    },
                },
                'validations_store': {
                    'class_name': 'ValidationsStore',
                    'store_backend': {
                        'class_name': 'TupleS3StoreBackend',
                        'bucket': self.GX_S3_BUCKET_NAME,
                        'prefix': self.S3_VALIDATION_STORE_DIR
                    },
                },
                'evaluation_parameter_store': {'class_name': 'EvaluationParameterStore'},
                'checkpoint_store': {
                    'class_name': 'CheckpointStore',
                    'store_backend': {
                        'class_name': 'TupleS3StoreBackend',
                        'bucket': self.GX_S3_BUCKET_NAME,
                        'prefix': self.S3_CHECKPOINT_STORE_DIR
                    },
                },
                'profiler_store': {
                    'class_name': 'ProfilerStore',
                    'store_backend': {
                        'class_name': 'TupleS3StoreBackend',
                        'bucket': self.GX_S3_BUCKET_NAME,
                        'prefix': self.S3_PROFILER_STORE_DIR,
                        'filepath_suffix': '.yml',
                        'fixed_length_key': False,
                        'platform_specific_separator': True,
                        'suppress_store_backend_id': False,
                    },
                },
                'metric_store': {
                    'class_name': 'MetricStore',
                    'store_backend': {
                        'class_name': 'TupleS3StoreBackend',
                        'bucket': self.GX_S3_BUCKET_NAME,
                        'prefix': self.S3_METRIC_STORE_DIR,
                    },
                }
            },
            expectations_store_name='expectations_store',
            validations_store_name='validations_store',
            evaluation_parameter_store_name='evaluation_parameter_store',
            checkpoint_store_name='checkpoint_store',
            profiler_store_name='profiler_store',
            data_docs_sites={
                's3_site': {
                    'class_name': 'SiteBuilder',
                    'store_backend': {
                        'class_name': 'TupleS3StoreBackend',
                        'bucket': self.GX_S3_BUCKET_NAME,
                        'base_public_path': f'http://{self.GX_S3_BUCKET_NAME}'
                    },
                    'site_index_builder': {
                        'class_name': 'DefaultSiteIndexBuilder',
                        'show_cta_footer': False
                    }
                }
            },
            anonymous_usage_statistics={
                'enabled': True
            }
        )
        self.context = EphemeralDataContext(project_config=self.data_context_config)
        self.s3_datasource = self.context.sources.add_pandas_s3(
            name=self.DATASOURCE_S3_PANDAS_NAME, bucket=self.DATA_S3_BUCKET_NAME, boto3_options={}
        )
        connection_string = f'awsathena+rest://@athena.ap-northeast-2.amazonaws.com/?s3_staging_dir=s3://{self.DATA_S3_BUCKET_NAME}/query_results/'
        if athena_workgroup:
            connection_string += f'&work_group={athena_workgroup}'
        self.athena_datasource = self.context.sources.add_sql(
            name=self.DATASOURCE_ATHENA_NAME,
            connection_string=connection_string
        )
        self.spark_datasource = self.context.sources.add_or_update_spark_s3(
            name=self.DATASOURCE_S3_SPARK_NAME,
            bucket=self.DATA_S3_BUCKET_NAME,
            boto3_options={}
        )

    def make_suite(self, suite_name: str) -> ExpectationSuite:
        '''
        generate GX suite on S3.

        :param suite_name: suite name
        :return:
        '''
        return self.context.add_or_update_expectation_suite(expectation_suite_name=suite_name)

    def get_suite_by_name(self, suite_name: str) -> ExpectationSuite:
        '''
        Get suite by suite name.

        :param suite_name: suite name
        :return:
        '''
        return self.context.get_expectation_suite(suite_name)

    def delete_suite(self, suite_name: str):
        '''
        delete suite on S3.

        :param suite_name: suite name
        :return:
        '''
        try:
            self.context.delete_expectation_suite(expectation_suite_name=suite_name)
        except DataContextError:
            pass

    def list_expectation_suites(self) -> Optional[Union[List[str], List[GXCloudIdentifier]]]:
        '''
        list suites.

        :return:
        '''
        return self.context.list_expectation_suites()

    def add_s3_pandas_csv_dataset(self, file_prefix: str, file_name: str) -> CSVAsset:
        '''
        add s3 csv file into GX dataset.

        :param file_prefix: s3 file directory path
        :param file_name: s3 file name. You should not include directory path.
        :return:
        '''
        file_prefix = file_prefix if file_prefix else self.DATA_S3_BUCKET_PREFIX
        return self.s3_datasource.add_csv_asset(
            s3_prefix=file_prefix,
            name=file_name
        )

    def add_s3_spark_csv_dataset(self, file_prefix: str, file_name: str) -> CSVAsset:
        '''
        add s3 csv file into GX dataset.

        :param file_prefix: s3 file directory path
        :param file_name: s3 file name. You should not include directory path.
        :return:
        '''

        file_prefix = file_prefix if file_prefix else self.DATA_S3_BUCKET_PREFIX
        return self.spark_datasource.add_csv_asset(
            s3_prefix=file_prefix,
            name=file_name,
            header=True,
            infer_schema=False,
        )

    def add_athena_dataset(self,
                           athena_database_name: Optional[str],
                           athena_table_name: Optional[str]) -> TableAsset:
        '''
        add athena table into GX dataset.

        :param athena_database_name: athena database name
        :param athena_table_name: athena table name
        :return:
        '''
        return self.athena_datasource.add_table_asset(name=athena_table_name,
                                                      schema_name=athena_database_name,
                                                      table_name=athena_table_name)

    def _get_validator(self, batch_list: List[Batch], suite: ExpectationSuite) -> Validator:
        '''
        get validator.

        :param batch_list: batch list
        :param suite: expectation suite
        :return:
        '''
        return self.context.get_validator(
            batch_list=batch_list,
            expectation_suite=suite
        )

    def validate(self, batch_list: List[Batch], suite: ExpectationSuite) \
            -> Union[ExpectationValidationResult, ExpectationSuiteValidationResult]:
        '''
        validate suite.

        :param batch_list: batch list
        :param suite: expectation suite
        :return:
        '''
        validator = self._get_validator(batch_list, suite)
        return validator.validate()

    def add_expectations(self, suite_name: str, expectation_configurations) \
            -> ExpectationSuite:
        '''
        add expectations into suite.

        :param suite_name: suite name
        :param expectation_configurations: expectation confs
        :return:
        '''
        suite = self.get_suite_by_name(suite_name)

        for e_confs in expectation_configurations:
            suite.add_expectation(e_confs)

        return self.context.add_or_update_expectation_suite(expectation_suite=suite)

    def _get_batch_list(self,
                        s3_file_prefix: Optional[str] = None,
                        s3_file_name: Optional[str] = None,
                        athena_database_name: Optional[str] = None,
                        athena_table_name: Optional[str] = None,
                        engine: str = 'spark', ) -> List[Batch]:
        '''
        get batch list.

        :param s3_file_prefix: s3 file prefix
        :param s3_file_name: s3 file name
        :param athena_database_name: athena database name
        :param athena_table_name: athena table name
        :param engine: spark, pandas, athena
        :return:
        '''
        if s3_file_prefix and not s3_file_name:
            sm = S3Manager(self.DATA_S3_BUCKET_NAME)
            for i in sm.list_objects(prefix=f'{s3_file_prefix}'):
                data_asset = self._add_data_asset(engine=engine,
                                                  s3_file_prefix=s3_file_prefix,
                                                  s3_file_name=i['Key'].rsplit('/')[-1])
        else:
            data_asset = self._add_data_asset(engine,
                                              s3_file_prefix,
                                              s3_file_name,
                                              athena_database_name,
                                              athena_table_name)
        batch_request = data_asset.build_batch_request()
        batch_list = self.context.get_batch_list(batch_request=batch_request)
        print(f'batch_list={batch_list}')
        assert len(batch_list) > 0
        return batch_list

    def _add_data_asset(self,
                        engine: str,
                        s3_file_prefix: Optional[str] = None,
                        s3_file_name: Optional[str] = None,
                        athena_database_name: Optional[str] = None,
                        athena_table_name: Optional[str] = None):

        if engine == 'pandas':
            data_asset = self.add_s3_pandas_csv_dataset(s3_file_prefix, s3_file_name)
        elif engine == 'spark':
            data_asset = self.add_s3_spark_csv_dataset(s3_file_prefix, s3_file_name)
        elif engine == 'athena':
            data_asset = self.add_athena_dataset(athena_database_name, athena_table_name)
        return data_asset

    def profile(self,
                suite: ExpectationSuite,
                s3_file_prefix: Optional[str] = None,
                s3_file_name: Optional[str] = None,
                pands_or_spark: str = 'pandas',
                athena_database_name: Optional[str] = None,
                athena_table_name: Optional[str] = None) -> ExpectationSuite:
        '''
        profile asset and generate auto-generated expectations.

        :param suite: expectation suite
        :param s3_file_prefix: s3 file prefix
        :param s3_file_name: s3 file name
        :param pands_or_spark: pandas or spark, default is pandas
        :param athena_database_name: athena database name
        :param athena_table_name: athena table name
        :return:
        '''
        batch_list = self._get_batch_list(s3_file_prefix, s3_file_name, athena_database_name, athena_table_name)
        validator = self.context.get_validator(batch_list=batch_list, expectation_suite=suite)
        return self._profile_with_validator(validator)

    def _profile_with_validator(self, validator: Union[Batch, Dataset, Validator]) -> ExpectationSuite:
        '''
        profile s3 file and generate auto-generated expectations.

        :param validator: validator
        :return:
        '''
        profiler = UserConfigurableProfiler(
            profile_dataset=validator,
            excluded_expectations=None,
            not_null_only=False,
            semantic_types_dict=None,
            table_expectations_only=False,
            value_set_threshold='MANY',
        )
        suite = profiler.build_suite()
        self.context.add_or_update_expectation_suite(expectation_suite=suite)
        return suite

    def checkpoint(self,
                   suite: ExpectationSuite,
                   s3_file_prefix: Optional[str] = None,
                   s3_file_name: Optional[str] = None,
                   engine: str = 'pandas',
                   athena_database_name: Optional[str] = None,
                   athena_table_name: Optional[str] = None,
                   ) -> CheckpointResult:
        '''
        Checkpoint test suite and generate result document and so on.

        :param suite: expectation suite
        :param s3_file_prefix: s3 file prefix
        :param s3_file_name: s3 file name
        :param engine: pandas or spark, default is pandas
        :param athena_database_name: athena database name
        :param athena_table_name: athena table name
        :return:
        '''
        batch_list = self._get_batch_list(s3_file_prefix, s3_file_name, athena_database_name, athena_table_name, engine)
        validator = self.context.get_validator(batch_list=batch_list, expectation_suite=suite)
        return self._checkpoint_with_validator(validator)

    def _checkpoint_with_validator(self, validator: Union[Batch, Dataset, Validator]) \
            -> CheckpointResult:
        '''
        Checkpoint test suite and generate result document and so on.

        :param validator: validator
        :return:
        '''
        checkpoint = self.context.add_or_update_checkpoint(
            name=f'checkpoint_{validator.expectation_suite_name}',
            validator=validator,
            run_name_template='checkpoint_results'
        )
        results = checkpoint.run()
        # validation_result_identifier = results.list_validation_result_identifiers()[0]
        # print(f'validation_result_identifier={validation_result_identifier}')
        return results

    def run(self,
            suite_name: str,
            expectation_conf_list: List[ExpectationConfiguration],
            s3_file_prefix: Optional[str] = None,
            s3_file_name: Optional[str] = None,
            pands_or_spark: str = 'pandas',
            athena_database_name: Optional[str] = None,
            athena_table_name: Optional[str] = None):
        '''
        run GX.

        :param suite_name: suite name
        :param expectation_conf_list: expectation configuration list
        :param s3_file_prefix: s3 file prefix
        :param s3_file_name: s3 file name
        :param pands_or_spark: pandas or spark engine
        :param athena_database_name: athena database name
        :param athena_table_name: athena table name
        :return:
        '''

        self.make_suite(suite_name)
        suite = self.add_expectations(suite_name, expectation_conf_list)
        self.checkpoint(s3_file_prefix=s3_file_prefix,
                        s3_file_name=s3_file_name,
                        pands_or_spark=pands_or_spark,
                        athena_database_name=athena_database_name,
                        athena_table_name=athena_table_name,
                        suite=suite)

    def validate_s3_csv(self, suite_name: str,
                        csv_path: str,
                        ecs: List[ExpectationConfiguration],
                        is_dir: bool = False,
                        engine='spark'):
        '''
        Validate s3 csv with pandas engine

        :param suite_name:
        :param csv_path:
        :param ecs:
        :param is_dir:
        :param engine:
        :return:
        '''

        self.make_suite(suite_name)
        suite = self.add_expectations(suite_name, ecs)
        if not is_dir:
            result = self.checkpoint(s3_file_prefix=csv_path,
                                     suite=suite,
                                     engine=engine)
        else:
            token = csv_path.rsplit('/')
            result = self.checkpoint(s3_file_prefix="/".join(token[0:-1]),
                                     s3_file_name=token[-1],
                                     suite=suite,
                                     engine=engine)
        print(f'result={result}')

        for k in result['run_results']:
            path = str(k).replace('ValidationResultIdentifier::', '')
            self._print_s3_web_url(f'validations/{path}')

        return result

    def _print_s3_web_url(self, path: str):
        print(
            f's3_web_url=https://s3.console.aws.amazon.com/s3/buckets/{self.GX_S3_BUCKET_NAME}?bucketType=general&prefix={path}.html&showversions=false')

    def validate_athena(self, suite_name: str, db_name: str, table_name: str, ecs: List[ExpectationConfiguration]):
        '''
        Validate table with athena engine

        :param suite_name:
        :param db_name:
        :param table_name:
        :param ecs:
        :return:
        '''

        self.make_suite(suite_name)
        suite = self.add_expectations(suite_name, ecs)
        result = self.checkpoint(athena_database_name=db_name,
                                 athena_table_name=table_name,
                                 suite=suite,
                                 engine='athena')
        print(f'result={result}')

        for k in result['run_results']:
            path = str(k).replace('ValidationResultIdentifier::', '')
            self._print_s3_web_url(f'validations/{path}')

        return result
