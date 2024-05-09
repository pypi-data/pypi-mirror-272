from logger_local.LoggerComponentEnum import LoggerComponentEnum


LABELS_LOCAL_PYTHON_COMPONENT_ID = 284
LABELS_LOCAL_PYTHON_COMPONENT_NAME = "labels-local-python-package"
DEVELOPER_EMAIL = "tal.g@circ.zone"
LABELS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT = {
    'component_id': LABELS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': LABELS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}

LABELS_PYTHON_PACKAGE_TEST_LOGGER_OBJECT = {
    'component_id': LABELS_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': LABELS_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': DEVELOPER_EMAIL
}
