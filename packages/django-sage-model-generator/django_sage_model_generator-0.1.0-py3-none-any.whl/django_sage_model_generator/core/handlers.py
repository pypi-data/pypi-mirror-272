import os
import subprocess
from pathlib import Path
from pydbml import PyDBML

from jinja2 import Environment, FileSystemLoader


from .utils import JinjaTemplateDiscovery
from core.utils import JinjaTemplateDiscovery, FileSystemHandler
from helper.enums import FieldType
from helper.dataclasses import DBMLRelation, TableRelation
from helper.filter import snake_to_pascal_case

class DBMLHandler:
    def __init__(self, database: PyDBML, discovery: JinjaTemplateDiscovery) -> None:
        self.database = database
        self.discovery = discovery
        self.func_dict = {
            "standard":snake_to_pascal_case,
        }

    @property
    def table_groups(self):
        return self.database.table_groups

    @property
    def tables(self):
        return self.database.tables

    @property
    def enums(self):
        return self.database.enums

    @property
    def relations(self):
        return self.database.refs


class DBMLToDjango(DBMLHandler):
    def __init__(self, database: PyDBML, template_manager: JinjaTemplateDiscovery):
        super().__init__(database, template_manager)

    def get_django_field(self, dbml_type):
        return getattr(FieldType, dbml_type.upper(), None).value

    def standardize_enums(self) -> dict[str, list[str]]:
        enums = dict()
        for enum in self.enums:
            enum_values = [value.name for value in enum.items]
            enums[enum.name] = enum_values
        return enums

    def standardize_relations(self) -> list[dict[str, str]]:
        rels = []
        for rel in self.relations:
            operation = DBMLRelation.from_str(rel.type)
            from_table = rel.table1.name
            from_fields = rel.col1[0].name
            to_table = rel.table2.name
            to_fields = rel.col2[0].name
            from_field_name = from_fields[0] if from_fields else None
            to_field_name = to_fields[0] if to_fields else None

            if 'id' in [from_field_name, to_field_name]:
                continue

            relationship = TableRelation(
                name=from_table,
                fk_field=from_fields,
                rel_type=operation,
                to_table=to_table,
                to_field=to_fields
            )
            relationship = {
                "table_name": from_table,
                "field_name": from_fields,
                "operation": operation,
                "other_table_name": to_table,
                "other_field_name": to_fields
            }
            rels.append(relationship)

        return rels

    def create_models(self):
        std_rels = self.standardize_relations()
        enum_dict = self.standardize_enums()
        specific_relationships = []

        for table in self.tables:
            for col in table.columns:
                if col.name == 'id' or ' ' in col.name:
                    col.name = col.name.replace(' ', '_')
                    continue

                self.process_column(col, table.name, std_rels, enum_dict, specific_relationships)

        return specific_relationships

    def process_column(self, col, table_name, std_rels, enum_dict, specific_relationships):
        field_related = any(rel["table_name"] == table_name and rel["field_name"] == col.name for rel in std_rels)
        if field_related:
            self.process_relationship(col, table_name, std_rels, specific_relationships)
        elif str(col.type) in enum_dict:
            self.process_enum_column(col, table_name, specific_relationships, enum_dict[str(col.type)])
        else:
            self.process_standard_column(col)

    def process_relationship(self, col, table_name, std_rels, specific_relationships):
        specific_relationships.append(table_name + col.name)
        for rel in std_rels:
            if table_name == rel["table_name"] and col.name == rel["field_name"]:
                col.type = self.get_relationship_field_type(rel)

    def get_relationship_field_type(self, rel):
        if rel["operation"] == DBMLRelation.ManyToOne:
            return "ForeignKey('{}', related_name='{}', on_delete=models.CASCADE".format(
                rel["other_table_name"].capitalize(), rel["field_name"] + '_' + rel["table_name"]
            )
        elif rel["operation"] == DBMLRelation.ManyToMany:
            return "ManyToManyField('{}', related_name='{}')".format(
                rel["other_table_name"].capitalize(), rel["field_name"] + '_' + rel["table_name"]
            )
        elif rel["operation"] == DBMLRelation.OneToOne:
            return "OneToOneField('{}', related_name='{}', on_delete=models.CASCADE".format(
                rel["other_table_name"].capitalize(), rel["field_name"] + '_' + rel["table_name"]
            )
        return "UNKNOWN_RELATIONSHIP_TYPE"

    def process_enum_column(self, col, table_name, specific_relationships, enum_values):
        specific_relationships.append(table_name + col.name)
        col.type = f"CharField(choices={enum_values}, max_length=100"

    def process_standard_column(self, col):
        column_type = str(col.type).lower()

        if 'varchar' in column_type:
            parts = column_type.strip('()').split('(')
            col.max_length = int(parts[1]) if len(parts) > 1 else 255
            col.type = FieldType.VARCHAR.value
        else:
            col.type = FieldType[column_type.upper()].value if column_type.upper() in FieldType.__members__ else 'TextField'

    def convert_enum_dbml(self, enums):
        template_path = self.discovery.enum_templates.get('base')
        if not template_path or not Path(template_path).is_file():
            raise FileNotFoundError("Jinja2 template file for enums not found.")

        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template(os.path.basename(template_path))
        template.globals.update(self.func_dict)
        models = template.render(enums=enums)
        return models

    def convert_dbml_to_django(self, specific_relationships, enums, domain: str):
        file_sys = FileSystemHandler(domain)
        template_path = self.discovery.model_templates.get('base')
        if not template_path or not Path(template_path).is_file():
            raise FileNotFoundError("Jinja2 template file for models not found.")

        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template(os.path.basename(template_path))
        template.globals.update(self.func_dict)
        for table in self.tables:
            table_name = table.name
            table_file_path = file_sys.find_file_location(table_name.lower(), start_path=domain) or os.path.join(domain, f"{table_name.lower()}.py")
            os.makedirs(os.path.dirname(table_file_path), exist_ok=True)
            if any(column.name.lower() == 'id' for column in table.columns):
                table.columns = [column for column in table.columns if column.name.lower() != 'id']
            table_model = template.render(tables=[table], specific_relationships=specific_relationships, enum_names=[name.capitalize() for name in enums.keys()])
            
            with open(table_file_path, "w") as table_file:
                table_file.write(table_model)

            subprocess.run(['black', table_file_path])

    def create_text_choices(self,enums,root_dir_name):
        file_path = os.path.join(root_dir_name,"helpers","choices.py")
        with open(file_path,"w") as f:
            f.write(enums)

    def run_conversion(self, root_dir_name: Path):
        file_sys = FileSystemHandler(root_dir_name)
        file_sys.setup_domain(self.table_groups)
        specify = self.create_models()
        enums = self.standardize_enums()
        django_models = self.convert_dbml_to_django(specify, enums, root_dir_name)
        enum_models = self.convert_enum_dbml(enums)
        self.create_text_choices(enum_models,root_dir_name)
