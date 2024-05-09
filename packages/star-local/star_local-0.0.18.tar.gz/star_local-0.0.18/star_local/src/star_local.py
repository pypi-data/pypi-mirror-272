import mysql.connector
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerLocal import Logger
# from api_management_local.Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,NotEnoughStarsForActivityException,PassedTheHardLimitException
from user_context_remote.user_context import UserContext

from .star_constants import STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT
from .exception_star import NotEnoughStarsForActivityException
from .star_transaction import StarTransactionsLocal

logger = Logger.create_logger(object=STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT)


class StarsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="action_star_subscription",
                         default_table_name="action_star_subscription_table",
                         default_view_table_name="action_star_subscription_view",
                         default_id_column_name="action_id")
        self.star_transaction = StarTransactionsLocal()
        self.user_context = UserContext()

    def __get_the_action_stars_by_profile_id_action_id(self, profile_id: int, action_id: int) -> int:
        logger.start(object={"profile_id": str(profile_id), "action_id": str(action_id)})
        try:
            subscription_id = self.user_context.get_effective_subscription_id()
            where = "subscription_id = %s AND action_id = %s"
            action_star = self.select_one_value_by_where(select_clause_value="action_stars", where=where,
                                                         params=(subscription_id, action_id))
        except Exception as e:
            logger.exception(object=e)
            raise e
        logger.end(object={'action_star': str(action_star)})
        return action_star

    # We must increase/decrease the stars before the action, to make sure they have enough starts before the action, regardless if the action performed or not - We should split to two methods and add BEGIN TRANSACTION and COMMIT
    def _update_profile_stars_before_action(self, profile_id: int, action_id: int) -> None:
        logger.start(object={"profile_id": profile_id, "action_id": action_id})
        try:
            action_stars = self.__get_the_action_stars_by_profile_id_action_id(profile_id, action_id)
            try:
                self.update_by_id(schema_name="profile", table_name="profile_table",
                                  data_json={"stars": f"stars + {action_stars}"},
                                  id_column_name="profile_id", id_column_value=profile_id)
            except mysql.connector.errors.DataError:
                logger.warning("Profile " + str(profile_id) + " do not have enough stars for action " + str(action_id))
                raise NotEnoughStarsForActivityException

            subscription_id = self.user_context.get_effective_subscription_id()
            data_json = {'action_id': action_id, 'action_stars': action_stars, 'subscription_id': subscription_id}
            self.star_transaction.insert(data_json=data_json)
            logger.info({'action_id': action_id,  # 'stars': stars,#
                         'action_stars': action_stars})
        except Exception as e:
            logger.exception(object=e)
            raise e
        logger.end(object={'action_id': action_id, 'action_stars': action_stars})

    def api_executed(self, api_type_id: int) -> None:
        logger.start(object={"api_type_id": str(api_type_id)})
        try:
            action_id = self.select_one_value_by_id(schema_name="api_type",
                                                    select_clause_value="action_id",
                                                    view_table_name="api_type_view",
                                                    id_column_name="api_type_id",
                                                    id_column_value=api_type_id)
            profile_id = self.user_context.get_effective_profile_id()
            self._update_profile_stars_before_action(profile_id, action_id)
        except Exception as e:
            logger.exception(object=e)
            raise e
        logger.end()

    def __how_many_stars_for_action_id(self, action_id: int) -> int:
        start_obj = {"action_id": action_id}
        logger.start(object=start_obj)
        try:
            action_star = self.select_one_value_by_id(schema_name="action_star_subscription",
                                                      select_clause_value="action_stars",
                                                      view_table_name="action_star_subscription_view",
                                                      id_column_name="action_id",
                                                      id_column_value=action_id)
        except Exception as e:
            logger.exception(object=e)
            raise e
        logger.end(object={'action_star': action_star})
        return action_star

    def __how_many_stars_for_profile_id_and_user_id(self, user_id: int, profile_id: int) -> int:
        start_obj = {"user_id": str(user_id), "profile_id": str(profile_id)}
        logger.start(object=start_obj)
        try:
            profile_stars = self.select_one_value_by_id(schema_name="profile",
                                                        select_clause_value="stars",
                                                        view_table_name="profile_view",
                                                        id_column_name="profile_id",
                                                        id_column_value=profile_id)
            user_stars = self.select_one_value_by_id(schema_name="user",
                                                     select_clause_value="stars",
                                                     view_table_name="user_view",
                                                     id_column_name="user_id",
                                                     id_column_value=user_id)
            total_stars = profile_stars + user_stars
        except Exception as e:
            logger.exception(object=e)
            raise e
        logger.end(object={'total_stars': str(total_stars)})
        return total_stars

    def verify_profile_star_before_action(self, action_id: int) -> None:
        start_obj = {"action_id": str(action_id)}
        logger.start(object=start_obj)
        try:
            action_stars = self.__how_many_stars_for_action_id(action_id)
            profile_id = self.user_context.get_effective_profile_id()
            user_id = self.user_context.get_effective_user_id()
            stars_for_profile_and_user = self.__how_many_stars_for_profile_id_and_user_id(user_id, profile_id)
            if stars_for_profile_and_user - action_stars < 0:
                raise NotEnoughStarsForActivityException
        except Exception as e:
            logger.exception(object=e)
            raise e
        finally:
            logger.end()
