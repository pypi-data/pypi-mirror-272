import os

from core.settings import (
    TEMPLATE_ENUM_PREFIX,
    TEMPLATE_MODEL_PREFIX
)

class JinjaTemplateDiscovery:
    model_prefix = TEMPLATE_MODEL_PREFIX
    enum_prefix = TEMPLATE_ENUM_PREFIX

    def __init__(self, models_dir: str = "templates"):
        self.models_dir = models_dir
        self.model_templates = {}
        self.enum_templates = {}
        self.discover()

    def discover(self):
        """
        Discovers model and enum template files in the specified models directory and categorizes them
        into model and enum templates dictionaries.
        """
        for filename in os.listdir(self.models_dir):
            if filename.endswith('.jinja2'):
                if filename.startswith(self.model_prefix):
                    template_name = filename[len(self.model_prefix):-len('.jinja2')]
                    self.model_templates[template_name] = os.path.join(self.models_dir, filename)
                elif filename.startswith(self.enum_prefix):
                    template_name = filename[len(self.enum_prefix):-len('.jinja2')]
                    self.enum_templates[template_name] = os.path.join(self.models_dir, filename)


class FileSystemHandler:
    def __init__(self, root_dir_name: str):
        self.root_dir_name = root_dir_name

    def setup_domain(self, table_groups):
        path=os.path.join(self.root_dir_name,"helpers")
        os.makedirs(path)
        for table_group in table_groups:
            table_group_path = os.path.join(self.root_dir_name, table_group.name.lower())
            os.makedirs(table_group_path, exist_ok=True)
            for table_name in table_group.items:
                model_name = f"{table_name.name.lower()}.py"
                model_path = os.path.join(table_group_path, model_name)
                init_name = os.path.join(table_group_path,'__init__.py')
                with open(model_path, 'w') as model_file:
                    model_file.close()
                with open(init_name,'w') as init_file:
                    init_file.close()

    def find_file_location(self, file_name, start_path="."):
        try:
            file_name = file_name + '.py'
            for root, dirs, files in os.walk(start_path):
                if file_name in files:
                    return os.path.abspath(os.path.join(root, file_name))

            print(f"File '{file_name}' not found.")
            return None
        except FileNotFoundError:
            print(f"Path '{start_path}' not found.")
            return None
