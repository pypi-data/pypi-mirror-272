from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerLocal import Logger

# from api_management_local.Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,NotEnoughStarsForActivityException,PassedTheHardLimitException
from .star_constants import STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT

logger = Logger.create_logger(object=STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT)


class StarTransactionsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="star_transaction",
                         default_table_name="star_transaction_table",
                         default_view_table_name="star_transaction_view",
                         default_id_column_name="star_transaction_id")

    # def insert_stars(self,data_json: dict):
    #     self.insert(data_json=data_json)
