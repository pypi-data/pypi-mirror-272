from database_mysql_local.generic_crud_ml import GenericCRUDML
from database_mysql_local.generic_mapping import GenericMapping
from logger_local.LoggerLocal import Logger
from language_remote.lang_code import LangCode
from database_infrastructure_local.number_generator import NumberGenerator
from user_context_remote.user_context import UserContext
from group_local.group_local_constants import GroupLocalConstants

from .labels_local_constants import LABELS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT

logger = Logger.create_logger(object=LABELS_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)
user_context = UserContext()

DEFAULT_SCHEMA_NAME = "label"
DEFAULT_TABLE_NAME = "label_table"
DEFAULT_VIEW_TABLE_NAME = "label_view"
DEFAULT_ID_COLUMN_NAME = "label_id"
DEFAULT_ML_ID_COLUMN_NAME = "label_ml_id"
DEFAULT_ENTITY1_NAME = "label"
ENGLISH_GROUP_ID = GroupLocalConstants.ENGLISH_GROUP_ID


class LabelsLocal(GenericMapping, GenericCRUDML):

    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_table_name: str = DEFAULT_TABLE_NAME,
                 default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 default_id_column_name: str = DEFAULT_ID_COLUMN_NAME, default_entity_name1: str = DEFAULT_ENTITY1_NAME,
                 default_entity_name2: str = None, is_test_data: bool = False):
        GenericMapping.__init__(self, default_schema_name=default_schema_name, default_table_name=default_table_name,
                                default_view_table_name=default_view_table_name,
                                default_id_column_name=default_id_column_name, default_entity_name1=default_entity_name1,
                                default_entity_name2=default_entity_name2, is_test_data=is_test_data)
        GenericCRUDML.__init__(self, default_schema_name=default_schema_name, default_table_name=default_table_name,
                               default_id_column_name=DEFAULT_ML_ID_COLUMN_NAME,
                               is_test_data=is_test_data)

    def insert_label(self, label_name: str, label_title: str = None, lang_code: LangCode = None,
                     parent_label_id: int = None, location_id: int = None, is_main: int = 0) -> tuple[int, int]:
        logger.start(object={"label_name": label_name, "label_title": label_title})
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        data_json = {
            "name": label_name,
            "number": NumberGenerator.get_random_number(
                schema_name=DEFAULT_SCHEMA_NAME,
                view_name=DEFAULT_TABLE_NAME
            ),
            "is_approved": 1,
            "parent_label_id": parent_label_id,
            "location_id": location_id
        }
        data_ml_json = {
            "title": label_title,
            "lang_code": lang_code.value,
            "is_title_approved": 1
        }
        label_id, label_ml_id = self.add_value(data_ml_json=data_ml_json, data_json=data_json,
                                               lang_code=lang_code, is_main=is_main)

        logger.end(object={"label_id": label_id, "label_ml_id": label_ml_id})
        return label_id, label_ml_id

    def add_label_entity(self, label_id: int, entity_id: int, entity_name: str) -> int:
        logger.start(object={"label_id": label_id, "entity_id": entity_id, "entity_name": entity_name})
        label_entity_id = self.insert_mapping(entity_id1=label_id, entity_id2=entity_id, entity_name2=entity_name,
                                              ignore_duplicate=True)
        logger.end(object={"label_entity_id": label_entity_id})
        return label_entity_id
