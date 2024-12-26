from jinja2 import Environment, Template, meta
class BasePrompt:
    '''
    基础的prompt类
    使用jinjia2作为模板处理
    '''

    def __init__(self, prompt_str: str) -> None:
        self.prompt = prompt_str

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
    

if __name__ == "__main__":
    # 定义模板字符串，其中包含替换符
    template_string = """
    Hello, {{ name }}!
    Today is {{ day }}.
    {% if age > 18 %}
    You are an adult.
    {% else %}
    You are a minor.
    {% endif %}
    """

    # 定义要替换的变量
    context = {
        'name': 'John',
        'day': 'Monday',
        'age': 20
    }

    # 创建prompt对象
    prompt = BasePrompt(template_string)

    # 生成prompt
    print(prompt.generate_prompt(context))