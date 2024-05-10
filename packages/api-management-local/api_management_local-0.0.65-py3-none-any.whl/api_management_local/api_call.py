from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT


class APICallsLocal(GenericCRUD, metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="api_call", default_id_column_name="api_call_id",
                         default_table_name="api_call_table", default_view_table_name="api_call_view",
                         is_test_data=is_test_data)

    def insert_api_call_json(self, api_call_json: dict) -> int:
        """Inserts a row into the api_call_table and returns the id of the inserted row"""
        api_call_id = self.insert(data_json=api_call_json)
        return api_call_id
