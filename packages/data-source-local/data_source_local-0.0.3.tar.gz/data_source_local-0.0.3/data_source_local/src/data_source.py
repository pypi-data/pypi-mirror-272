from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger

# TODO constans -> constants, obj -> data_source_logger_code_obj
from .data_source_constans import obj

logger = Logger.create_logger(object=obj)


# TODO Change to DataSources
# TODO Add MetaLogger
class DataSource(GenericCRUD):

    def __init__(self):
        super().__init__(default_schema_name='data_source',
                         default_table_name='data_source_table',
                         default_view_table_name='data_source_ml_en_view')

    # TODO Why do we return two ints?
    # TODO lang_code: LangCode
    # TODO insert_fields() per our Python Class methods naming conventions https://docs.google.com/document/d/1QtCVak8f9rOtZo9raRhYHf1-7-Sfs8rru_iv3HjTH6E/edit?usp=sharing
    def insert_data_source(self, data_source_name: str, lang_code: str = LangCode.ENGLISH.value) -> (int, int):
        # TODO Both are not needed if using the MetaLogger
        METHOD_NAME = 'insert_data_source'
        logger.start(METHOD_NAME, object={
            'data_source_name': data_source_name,
            'lang_code': lang_code})
        try:
            data_source_json = {
                'created_user_id': logger.user_context.get_effective_user_id(),
                'updated_user_id': logger.user_context.get_effective_user_id()
            }
            data_source_id = self.insert(data_json=data_source_json)
            data_source_ml_json = {
                'data_source_id': data_source_id,
                'lang_code': lang_code,
                'data_source_name': data_source_name,
                'created_user_id': logger.user_context.get_effective_user_id(),
                'updated_user_id': logger.user_context.get_effective_user_id()
            }
            data_source_ml_id = self.insert(
                table_name='data_source_ml_table',
                data_json=data_source_ml_json)
            # TODO Why do we need to return the data_source_ml_id?
            logger.end(METHOD_NAME, object={
                'data_source_id': data_source_id,
                'data_source_ml_id': data_source_ml_id})
            return data_source_id, data_source_ml_id

        except Exception as e:
            logger.exception(
                log_message="faild to insert data_source " + METHOD_NAME + str(e), object=e)
            logger.end(METHOD_NAME, object={
                'data_source_name': data_source_name, 'lang_code': lang_code})
            raise e

    def get_data_source_id_by_name(self, data_source_name: str) -> int or None:
        METHOD_NAME = 'get_data_source_id_by_name'
        try:
            logger.start(log_message=METHOD_NAME, object={
                'data_source_name': data_source_name})
            data_source_id = self.select_one_value_by_id(
                select_clause_value='data_source_id',
                id_column_name='data_source_name',
                id_column_value=data_source_name)
            if data_source_id:
                logger.end(METHOD_NAME, object={
                    'data_source_id': data_source_id})
                return data_source_id
            else:
                logger.end(METHOD_NAME, object={
                    'data_source_id': data_source_id})
                return None
        except Exception as e:
            logger.exception(
                log_message="faild to get data_source_id " + METHOD_NAME + str(e), object=e)
            logger.end(METHOD_NAME, object={
                'data_source_name': data_source_name})
            raise e

    def get_data_source_name_by_id(self, data_source_id: int) -> str or None:
        METHOD_NAME = 'get_data_source_name_by_id'
        try:
            logger.start(log_message=METHOD_NAME, object={
                'data_source_id': data_source_id})
            data_source_name = self.select_one_value_by_id(
                select_clause_value='data_source_name',
                id_column_name='data_source_id',
                id_column_value=data_source_id)
            if data_source_name:
                logger.end(METHOD_NAME, object={
                    'data_source_name': data_source_name})
                return data_source_name
            else:
                logger.end(METHOD_NAME, object={
                    'data_source_name': data_source_name})
                return None
        except Exception as e:
            logger.exception(
                log_message="faild to get data_source_name " + METHOD_NAME + str(e), object=e)
            logger.end(METHOD_NAME, object={'data_source_id': data_source_id})
            raise e
