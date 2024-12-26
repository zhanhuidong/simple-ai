from .base import(
    AbsPrompt
)


from jinja2 import Template, Undefined, Environment, meta

class BasePrompt(AbsPrompt):
    '''
    基础的prompt类
    使用jinjia2作为模板处理
    '''

    def __init__(self, prompt_str: str) -> None:
        super().__init__(prompt_str)

    def generate_prompt(self, params: dict) -> str:
        '''根据参数处理prompt'''
        # 创建 Jinja2 环境
        env = Environment()

        # 解析模板源代码，生成抽象语法树（AST）
        parsed_content = env.parse(self.prompt)

        # 提取未声明的变量名
        undeclared_variables = meta.find_undeclared_variables(parsed_content)

        # 校验是否所有参数都已提供
        for var in undeclared_variables:
            if var not in params:
                raise ValueError(f"Missing parameter: {var}")
            
        return Template(self.prompt).render(params)