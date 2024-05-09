from logger_local.LoggerComponentEnum import LoggerComponentEnum
from user_context_remote.user_context import UserContext


DEVELOPER_EMAIL = 'heba.a@circ.zone'
STAR_LOCAL_PYTHON_COMPONENT_ID = 244
STAR_LOCAL_PYTHON_COMPONENT_NAME = "star-local-python-package"
STAR_LOCAL_PYTHON_CODE_LOGGER_OBJECT = {
    'component_id': STAR_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': STAR_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
STAR_LOCAL_PYTHON_TEST_LOGGER_OBJECT = {
    'component_id': STAR_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': STAR_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': DEVELOPER_EMAIL
}
# TODO Why USER_CONTEXT and not user_context?
USER_CONTEXT = UserContext()
PROFILE_ID = USER_CONTEXT.get_effective_profile_id()
USER_ID = USER_CONTEXT.get_effective_user_id()
# TODO What is the use of ACTION_ID? Why 50000?
ACTION_ID = 50000

STAR_TABLE_NAME = 'star_table'
STAR_VIEW_NAME = 'star_ml_table'

STAR_ML_TABLE_NAME = 'star_ml_table'
STAR_ML_VIEW_NAME = 'star_ml_view'
