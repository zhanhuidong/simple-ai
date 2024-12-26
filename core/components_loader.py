import os
import importlib
import sys
import yaml
import inspect

exclude_name = ["datetime", "Undefined", "Path"]
def load_classes_from_components():
    components_path = os.path.join(os.path.dirname(__file__), '../components')
    print(f"components_path: {components_path}")
    
    # 将 components 目录添加到模块搜索路径
    sys.path.append(os.path.dirname(components_path))
    
    classes_dict = {}

    # 遍历 components 目录及其子目录
    for root, dirs, files in os.walk(components_path):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_name = os.path.splitext(file)[0]
                module_path = os.path.relpath(root, components_path).replace(os.sep, '.')
                full_module_name = f"components.{module_path}.{module_name}" if module_path else f"components.{module_name}"
                
                print(f"Importing module: {full_module_name}")  # 调试信息
                module = importlib.import_module(full_module_name)

                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type):
                        print(f"Found class: {attr_name}")  # 调试信息
                        if attr_name != "ABC" and not attr_name.startswith('Abs') and attr_name not in exclude_name:
                            classes_dict[attr_name] = f"{full_module_name}.{attr_name}"
                            # 加载类尝试一下
                            # importlib.import_module(classes_dict[attr_name])

    return classes_dict

# 调用函数并获取类字典
classes_dict = load_classes_from_components()
# print(classes_dict)  # 可以根据需要选择是否打印

from pydantic import BaseModel, Extra

class VariableModel(BaseModel):

    class Config:
        # extra = Extra.allow  # 允许额外字段
        extra='allow'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 调用父类的构造函数
        for name, value in kwargs.items():
            self.__setattr__(name, value)

data = """
name: Mix
param:
    parameter:
        model: "llama3pro"
        api_key: '123'
        base_url: http://127.0.0.1:1234
        full_url: http://127.0.0.1:1234/v1/chat/completions
        max_retry: 2
"""

config = yaml.safe_load(data)
config_name = config['name']
config_param = config['param']

# 通过指定的类名字符串，获取类对象
class_path = classes_dict[config_name]
module_name, class_name = class_path.rsplit('.', 1)
module = importlib.import_module(module_name)
class_ = getattr(module, class_name)
# 获取类的 __init__ 方法的参数
init_signature = inspect.signature(class_.__init__)
init_params = init_signature.parameters
print(init_params)  # 打印 __init__ 方法的参数
params = {name: VariableModel(**config_param[name]) for name, param in init_params.items() if name != 'self'}
instance = class_(**params)
print(instance.__dict__)