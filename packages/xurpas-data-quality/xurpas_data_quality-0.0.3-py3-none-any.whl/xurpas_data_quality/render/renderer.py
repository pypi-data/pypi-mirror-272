from abc import ABC, abstractmethod
from typing import Any, Dict,List

from xurpas_data_quality.render.templates import template

class BaseRenderer(ABC):
    def __init__(self, content: Dict[str, Any], name: str = None, id:str=None, **kwargs):
        self.content = content

        if name is not None:
            self.content['name'] = name
        
        if id is not None:
            self.content['id'] = id

    @property
    def name(self) -> str:
        return self.content.get('name', None)
    
    @property
    def id(self) -> str:
        return self.content.get('id', None)

    @abstractmethod
    def render(self) -> Any:
        pass

class HTMLTable(BaseRenderer):
    def __init__(self, data:Any, id:str=None, name:str=None,**kwargs):
        super().__init__(id=id, name=name,content={'data': data}, **kwargs)

    def render(self):
        return template("table.html").render(**self.content)

        
class HTMLToggle(BaseRenderer):
    def __init__(self, text:str, id:str, **kwargs):
        super().__init__( content={'text': text, 'id': id}, **kwargs)

    def render(self):
        return template("toggle.html").render(**self.content)
        
class HTMLCollapse(BaseRenderer):
    def __init__(self, button: HTMLToggle, body:Any, **kwargs):
        super().__init__({'button':button, 'body':body})
    
    def render(self):
        return template("collapse.html").render(**self.content)
    
class HTMLVariable(BaseRenderer):
    def __init__(self, name, body, bottom=None, **kwargs):
        super().__init__({"variable_name":name, "variable_body": body, "variable_bottom": bottom}, **kwargs)

    def render(self):
        return template("variable.html").render(name = self.content['variable_name'], bottom=self.content['variable_bottom'],**self.content['variable_body'])
    
class HTMLPlot(BaseRenderer):
    def __init__(self, plot:Any, type="small", **kwargs):
        super().__init__({"plot": plot}, **kwargs)
        if type !="small" and type !="large":
            raise ValueError("Plot type should be either 'small' or 'large'")
        else:
            self.type=type

    def render(self):
        return template("plot.html").render(**self.content, type=self.type)
    

class HTMLDropdown(BaseRenderer):
    def __init__(self, id:str, dropdown_items: List[str], dropdown_content: Any,name:str=None, **kwargs):
        super().__init__(
                        {
                            'dropdown_items': dropdown_items,
                            'dropdown_content': dropdown_content
                        },
                        name,
                        id,
                        **kwargs)
    def render(self):
        return template("dropdown.html").render(**self.content)

class HTMLContainer(BaseRenderer):
    def __init__(self, type:str, container_items:list, name:str=None, id:str=None, col=None, **kwargs):
        super().__init__({'container_items':container_items, 'name': name, 'id':id, 'col':col}, **kwargs)
        self.type = type
    def render(self):
        if self.type == 'box':
            return template("containers/box.html").render(container_items=self.content['container_items'])
        elif self.type == 'column':
            return template("containers/column.html").render(container_items=self.content['container_items'])
        elif self.type == 'sections':
            return template("containers/sections.html").render(
                container_items=self.content['container_items'])
        elif self.type == 'tabs':
            return template("containers/tabs.html").render(**self.content)
        elif self.type == 'default':
            return template("containers/default.html").render(**self.content)
        elif self.type == 'test':
            return template("containers/test.html").render(**self.content)
        else:
            raise ValueError(f"unknown Container ({self.type}) type!")

class HTMLBase(BaseRenderer):
    def __init__(self, body: Any, name: str, **kwargs):
        if name is None:
            name = "Profile Report"
        super().__init__(content={"body":body}, name=name, *kwargs)

    def render(self, **kwargs) -> str:
        nav_items = [self.content['name']]
        return template("base.html").render(**self.content, nav_items=nav_items, **kwargs)