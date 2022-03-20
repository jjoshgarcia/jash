from dash import Input, State,Output
import dash


class Jash:
    # Output decorator 
    class Output:
        def __init__(self,component_id, component_property,):
            self.component_id=component_id
            self.component_property=component_property
            
        def __call__(self, f) :
            self.fget=f
            return self
          
        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            return self.fget(obj)
          
    def __call__(self,  *args, **kwargs):
        inputs=[i for i in self.__class__.__dict__.items() if type(i[1]) is Input]
        state=[i for i in self.__class__.__dict__.items() if type(i[1]) is State]
        items=inputs+state
        arg_list=list(*args)
        for (k,_), arg in zip(items,arg_list):
            setattr(self,k,arg)
        outputs_=self.outputs()
        outputs=[getattr(self,output[0]) for output in outputs_]
        if len(outputs_)==1:
            output=outputs[0]
            return output
        return outputs
      
    @property
    def trigger_input(self):
        ctx = dash.callback_context
        if ctx.triggered:
            return ctx.triggered[0]['prop_id'].split('.')[0]
        return None
      
    @classmethod
    def outputs(cls):
        items=list((i for i in cls.__dict__.items() if type(i[1]) is cls.Output))
        return items
      
    @classmethod
    def dependencies(cls,):
        outputs=[Output(i[1].component_id,i[1].component_property) for i in cls.__dict__.items() if type(i[1]) is cls.Output]
        inputs=[i[1] for i in cls.__dict__.items() if type(i[1]) is Input]
        state=[i[1] for i in cls.__dict__.items() if type(i[1]) is State]
        _dependencies=list(outputs+inputs+state)
        return _dependencies

      
def callbacks_class(cls):
    def inner(func):
        def wrapper(*args):
            i=cls()
            r=i(args)
            return func(r)
        return wrapper
    return inner
  
  
def callback_registration(app,callbacks):
    '''
    Register a list class based Jash callbacks
    '''
    functions=[]
    for jash_subclass in callbacks:
        @app.callback(*jash_subclass.dependencies())
        @callbacks_class(jash_subclass)
        def func(output):
            return output
        functions.append(func)
    return functions
