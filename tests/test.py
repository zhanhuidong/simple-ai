from pydantic import BaseModel
from typing import Union
class A(BaseModel):
    name:str


class B(BaseModel):
    age:int

class C(BaseModel):
    a:A
    b:B
    def __init__(self, a:Union[A,dict], b:Union[B,dict]) -> None:
        super().__init__(a=a, b=b)
        if isinstance(a,A):
            self.a = a
        elif isinstance(a, dict):
            self.a = A(**a)
        
        if isinstance(b,A):
            self.b = b
        elif isinstance(b, dict):
            self.b = B(**b)

    def info(self):
        print(f"{self.a.name} 今年 {str(self.b.age)} 岁")

class D(BaseModel):
    b:B
    a:A

if __name__ == "__main__":
    d = D(b = B(age=34),a=A(name = "小马"))
    para = d.model_dump(exclude_unset=True)
    print(para)
    C(**para).info()