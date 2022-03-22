from dash import Input, State,Output
import dash
class Jash:
    class Output:
        # Output class non-data descriptor
        def __init__(self,component_id, component_property,):
            '''
            Get the id of the dash component and attribute.
            '''
            self.component_id=component_id
            self.component_property=component_property
        def __call__(self, f) :
            '''
            Get the decorated function.
            '''
            self.fget=f
            return self
        def __get__(self, obj, objtype=None):
            '''
            This methods makes the decorated function behave like one of the returned result of the output.
            self.fget is the output function, obj is the Jash subclass, so self.fget(obj) is the result of the output method call.
            '''
            return self.fget(obj)
    def __call__(self,  *args, **kwargs):
        '''
        args is the list of Inputs and States values injected by Dash.
        Here inputs and states values are matched with their respective attribute names in the class then the outputs are collected and returned.
        '''
        inputs=[i for i in self.__class__.__dict__.items() if type(i[1]) is Input]
        state=[i for i in self.__class__.__dict__.items() if type(i[1]) is State]
        items=inputs+state
        arg_list=list(*args)
        for (k,_), arg in zip(items,arg_list):
            setattr(self,k,arg)
        outputs_=self.outputs()
        outputs=[getattr(self,output[0]) for output in outputs_]
        if len(outputs_)==1:
            return outputs[0]
        return outputs
    @property
    def trigger_input(self):
        '''
        Helper function to that returns name of the component that triggered the callback
        '''
        ctx = dash.callback_context
        if ctx.triggered:
            return ctx.triggered[0]['prop_id'].split('.')[0]
        return None
    @classmethod
    def outputs(cls):
        items=[i for i in cls.__dict__.items() if type(i[1]) is cls.Output]
        return items
    @classmethod
    def dependencies(cls):
        '''
        All output, input and states to be injected into the dash callback decorator
        '''
        outputs=[Output(i[1].component_id,i[1].component_property) for i in cls.__dict__.items() if type(i[1]) is cls.Output]
        inputs=[i[1] for i in cls.__dict__.items() if type(i[1]) is Input]
        state=[i[1] for i in cls.__dict__.items() if type(i[1]) is State]
        _dependencies=list(outputs+inputs+state)
        return _dependencies
def callbacks_class(cls):
    '''
    Decorator for intercepting callback inputs, inserting it into the Jash Class and returning outputs in the correct order.
    '''
    def inner(func):
        def wrapper(*args):
            i=cls()
            r=i(args)
            return func(r)
        return wrapper
    return inner
def callback_registration(app,callbacks):
    '''
    callbacks → list of Jash subclasses
    '''
    functions=[]
    for jash_subclass in callbacks:
        @app.callback(*jash_subclass.dependencies())
        @callbacks_class(jash_subclass)
        def func(output):
            return output
        functions.append(func)
    return functions
