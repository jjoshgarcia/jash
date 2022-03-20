# Jash
## Class based abstraction of Dash Callbacks

A class based approach to callbacks in Dash is less prone to components naming errors and more testable. It is more declarative than procedural too.

Transform the classic Dash callback

```
@app.callback(
  Output('my_component_output_1','my_component_output_attribute'),
  Output('my_component_output_2','my_component_output_attribute'),
  Input('my_component_input_1','my_component_input_attribute'),
  Input('my_component_input_2','my_component_input_attribute'))
def update(my_input_1,my_input_2):
  ...
  return my_output_1, my_output_2
```

for the class based version
```
from jash import Jash, callback_registration

class MyClass(Jash):
  my_input_1=Input('my_component_input_1','my_component_input_attribute')
  my_input_2=Input('my_component_input_2','my_component_input_attribute')
  
  @Jash.Output('my_component_output_1','my_component_output_attribute')
  def my_output_1(self):
    # use self.input_1 self.input_2 to do computations
    ...
    return result
    
  @Jash.Output('my_component_output_2','my_component_output_attribute')
  def my_output_2(self):
    ...
    return result

```
Finally, register the callback class
```
from jash import callback_registration

callback_registration(app,[MyClass])
```
