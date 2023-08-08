* [Python decorator walk-through](#s1)
  * [Decorators as objects](#s1-1)
      * [Callable objects](#s1-1-1)
      * [Simple decorators](#s1-1-2)
      * [Decorators that can receive parameters](#s1-1-3)
  * [Decorators with first class functions/Closures](#s1-2)
      * [First class functions/Closures in Python](#s1-2-1)
      * [Decorators by means of first class functions/closures](#s1-2-2)
  * [Decorators in the python standard library](#s1-3)
      * [@staticmethod and @classmethod](#s1-3-1)
      * [The functools library](#s1-3-2)
      * [dataclasses](#s1-3-3)
      * [contextlib](#s1-3-4)


# <a id='s1' />Python decorator walk-through


## <a id='s1-1' />Decorators as objects


### <a id='s1-1-1' />Callable objects

A class is callable, if an object of the class can be called as a function.
This requires us to define a \_\_call\_\_ instance method
Let's look at an example:


__Source:__

```python

class CallableObject:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self):
        print(type(self), self.prefix)

callable_obj = CallableObject("show me")

# by virtue of the __callable__ member: lets call an instance of the callable object of class CallableObject
callable_obj()

```

__Result:__

```
>> <class '__main__.CallableObject'> show me
```

The next example shows a callable object that accepts additional parameters, like a real function.
Here we need to add parameters to the \_\_call\_\_ method.


__Source:__

```python

class CallableObject2:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, x, y):
        print(type(self), self.prefix, "x:", x, "y:", y)
        return x * y

callable_obj = CallableObject2("callable with arguments, and return values")
print("callable_obj(2,3):", callable_obj(2,3))

```

__Result:__

```
>> <class '__main__.CallableObject2'> callable with arguments, and return values x: 2 y: 3
>> callable_obj(2,3): 6
```


### <a id='s1-1-2' />Simple decorators

Function decorators take a given function, and intercept the call to that function. They act as a kind of proxy for calls of a given function.
This gives them the chance to add the following behavior:
- Add code that is run before calling the intercepted function, it can also alter the arguments of the function call, before they are passed to the intercepted/original function.
- Add code that is run after calling the intercepted function, it can also alter the return value of the original function, before it is returned to the caller.
  
A function decorator therefore acts as a kind of 'smart proxy' around a given Python function.

Lets start with an interceptor class, the class receives the wrapped function as an argument to its \_\_init\_\_ method;
The class is a callable object, and it calls the original function in its \_\_call\_\_ method.
The style of doing it as a class has a big plus: you can add instance variables to the decorator, like for example a counter of calls to the original function.

Here is the decorator class, that intercepts the calls to an argument function:


__Source:__

```python

class CountCalls:

    # init method, gets the original function reference,
    # the CountCalls decorator forwards arguments to this original function, and it does so with style...
    def __init__(self, func):

        # Copy the __name__, ___qualname_, __doc__, __module__, __module__, __annotations__ attributes of the function argument into CountCalls instance,
        # the CountCalls instance also gets a __wrapped__ attribute, which points to the intercepted/wrapped function supplied by the func constructor argument.
        # as well as all entries in __dict__ of the wrapped function are copied into  __dict__ member of the CountCalls instance.
        # this is in order ot make the wrapper look the same as the wrapped function.
        functools.update_wrapper(self, func)

        # The forwarded function reference is put into an instance member, so that __call__ will be able to forward the call.
        self.func = func

        # Set the state variable, the number of calls. This counter is update upon each call.
        self.num_calls = 0

    # the __call__ function is called, when an instance of the CounCalls class is used as a function.
    # gets both positional arguments *args and keyword arguments **kwargs, these are all forwarded to the original function.
    def __call__(self, *args, **kwargs):

        # Count the number of invocations.
        self.num_calls += 1

        # log that we are about to forward the call to the original function
        print("Calling:", self.func.__name__, "#call:", self.num_calls, "positional-arguments:", *args, "keyword-arguments:", **kwargs)

        # forward the call.
        ret_val = self.func(*args, **kwargs)

        # log the event, that we returned from the original function. Also log the return value of the original function
        print("Return from:", self.func.__name__, "#call:", self.num_calls, "return-value:", ret_val)

        # the return value of the original function call is returned to the caller
        return ret_val

```
Lets intercept the say\_miau function.


__Source:__

```python

def say_miau():
    ''' docstring: print the vocalization of a Felis Catus, also known as cat '''
    print("Miau!")

# The global variable say_miau now refers to an object, that wraps the original say_miau function.
say_miau = CountCalls(say_miau)

# the call to say_miau first calls the __call__ method of the CountCalls object, 
# This object
#  - counts the invocation
#  - logs the call 
#  - forwards the call to the original say_miau function.
#  - logs the return value of the siau_miau function
#
say_miau()
say_miau()

```

__Result:__

```
>> Calling: say_miau #call: 1 positional-arguments: keyword-arguments:
>> Miau!
>> Return from: say_miau #call: 1 return-value: None
>> Calling: say_miau #call: 2 positional-arguments: keyword-arguments:
>> Miau!
>> Return from: say_miau #call: 2 return-value: None
```

now lets look at the properties of the say\_miau variable

__Source:__

```python

# the type of the wrapped object is CountCalls
print("type(say_miau) : ", type(say_miau))

# but the name and docstring are copied from the wrapped object, because of the call to functools.update_wrapper
# This way, the decorated function appears as the original function, despite it having been wrapped.
print("say_miau.__name__ : ", say_miau.__name__)
print("say_miau.__doc__ : ", say_miau.__doc__)
print("say_miau.__wrapped__ : ", say_miau.__wrapped__)

```

__Result:__

```
>> type(say_miau) :  <class '__main__.CountCalls'>
>> say_miau.__name__ :  say_miau
>> say_miau.__doc__ :   docstring: print the vocalization of a Felis Catus, also known as cat 
>> say_miau.__wrapped__ :  <function say_miau at 0x1046320c0>
```

Attention!
Here is the equivalent way of setting up the decorator instance! just as the previous case, only for the say\_woof method.
The @CountCalls syntax is supposed to be a shorter way of doing the same assignment, as in the previous example!


__Source:__

```python

@CountCalls
def say_woof(dog_name):
    print("Woof! says:", dog_name)

print("say_woof is a variable of type", type(say_woof) )

say_woof("Snoopy")

```

__Result:__

```
>> say_woof is a variable of type <class '__main__.CountCalls'>
>> Calling: say_woof #call: 1 positional-arguments: Snoopy keyword-arguments:
>> Woof! says: Snoopy
>> Return from: say_woof #call: 1 return-value: None
```

Another example: the inc\_me function receives an integer, and returns the increment of the argument.
This process is again logged by the @CountCall decorator.


__Source:__

```python

@CountCalls
def inc_me(number_argument):
    return number_argument + 1

inc_me( inc_me( 1 ) )

# inc_me is a variable of type CountCalls, so let's access the call count directly!
print("number of calls ", inc_me.num_calls)


```

__Result:__

```
>> Calling: inc_me #call: 1 positional-arguments: 1 keyword-arguments:
>> Return from: inc_me #call: 1 return-value: 2
>> Calling: inc_me #call: 2 positional-arguments: 2 keyword-arguments:
>> Return from: inc_me #call: 2 return-value: 3
>> number of calls  2
```


### <a id='s1-1-3' />Decorators that can receive parameters

Lets look at the configurabl LimitCalls decorator, it can be used in different scenarios, it receives the following configuration parameters:
- log\_calls - a boolean, it logs the call if set to True
- max\_calls - the maximum number of calls, if decorator raises an error and does not forward the call to the original function, when the limit on the number of calls has been reached.

The class \_LimitCalls starts with an underscore, to show that this is a private class, that is not supposed to be exported from a module.


__Source:__

```python

class _LimitCalls:
    def __init__(self, function, max_hits, log_calls):

        # Copy the __name__, ___qualname_, __doc__, __module__, __module__, __annotations__ attributes of the function argument into _LimitCalls instance,
        # the _LimitCalls instance also gets a __wrapped__ attribute, which points to the wrapped function supplied by the func constructor argument.
        # as well as all entries in __dict__ of the wrapped function are copied into  __dict__ member of the  instance.
        # this is in order ot make the wrapper look the same as the wrapped function.
        functools.update_wrapper(self, function)

        # the forwarded function and decorator arguments are passed as arguments to __init__
        self.function = function
        self.max_hits = max_hits
        self.log_calls = log_calls

        # set the state variable, the number of calls, that is update upon each call.
        self.num_calls = 0

    def __call__(self, *args, **kwargs):

        self.num_calls += 1

        if self.num_calls > self.max_hits:
            raise ValueError(f"function {self.function.__name__} number of call limit {self.max_hits} has been exceeded")

        if self.log_calls:
            print("Calling:",self.function.__name__,"#call:", self.num_calls, "positional-arguments:", *args, "keyword-arguments:", **kwargs)

        fun = self.function
        value = fun(*args,**kwargs)

        if self.log_calls:
            print("Return from:", self.function.__name__, "#call:", self.num_calls, "return-value:", value)

        return value

# This function creates the decorator
def LimitCalls(function=None, max_hits=3, log_calls=False):
    print("LimitCalls function:", function, "max_hits:", max_hits, "log_calls:", log_calls)
    if function:
        return _LimitCalls(function, max_hits, log_calls)

    def wrapper(function):
        print("wrapper function:", function)
        return _LimitCalls(function, max_hits, log_calls)

    return wrapper

```
Lets use the LimitCalls decorator, here the defauls values for the parameters of the decorator are used. the LimitCalls function is called and it receives the square\_me function as parameter, this results in an instantion of the internal \_LimitsCalls object, in the same call.


__Source:__

```python

@LimitCalls
def square_me(arg_num):
    ''' return a square of the argument '''
    return arg_num * arg_num

# square_me is a variable of type _LimitCalls
print("square_me type: ", type(square_me))

for idx in range(1, 4):
    print("idx:", idx)
    got_value_error = False
    try:
        print("call #", idx, "returns: ", square_me(idx+1))
    except ValueError:
        got_value_error = True
    if idx == 4:
        assert got_value_error

```

__Result:__

```
>> LimitCalls function: <function square_me at 0x104633740> max_hits: 3 log_calls: False
>> square_me type:  <class '__main__._LimitCalls'>
>> idx: 1
>> call # 1 returns:  4
>> idx: 2
>> call # 2 returns:  9
>> idx: 3
>> call # 3 returns:  16
```

Setting non default value for the decorator parameters.
first the LimitCalls function is called with function=None, and maxhits=4, log\_calls=True
The first call returns the internal function wrapper, then function wrapper is called with the function parameter set to cube\_me, this returns the \_LimitCall2 object.


__Source:__

```python

@LimitCalls(max_hits=4, log_calls=True)
def cube_me(arg_num):
    ''' return a cube of the argument '''
    return arg_num * arg_num * arg_num

```

__Result:__

```
>> LimitCalls function: None max_hits: 4 log_calls: True
>> wrapper function: <function cube_me at 0x104633ba0>
```

cube\_me is a variable of type \_LimitCalls


__Source:__

```python

print("cube_me type:", type(cube_me))

for idx in range(1, 6):
    print("idx:", idx)
    got_value_error = False
    try:
        print("call #", idx, "returns: ", cube_me(idx+1))
    except ValueError:
        got_value_error = True
    if idx == 5:
        assert got_value_error

```

__Result:__

```
>> cube_me type: <class '__main__._LimitCalls'>
>> idx: 1
>> Calling: cube_me #call: 1 positional-arguments: 2 keyword-arguments:
>> Return from: cube_me #call: 1 return-value: 8
>> call # 1 returns:  8
>> idx: 2
>> Calling: cube_me #call: 2 positional-arguments: 3 keyword-arguments:
>> Return from: cube_me #call: 2 return-value: 27
>> call # 2 returns:  27
>> idx: 3
>> Calling: cube_me #call: 3 positional-arguments: 4 keyword-arguments:
>> Return from: cube_me #call: 3 return-value: 64
>> call # 3 returns:  64
>> idx: 4
>> Calling: cube_me #call: 4 positional-arguments: 5 keyword-arguments:
>> Return from: cube_me #call: 4 return-value: 125
>> call # 4 returns:  125
>> idx: 5
```

Can we use the @LimitCalls decorator with a class declaration? Lets try.
Only the \_\_init\_\_ method gets intercepted, when adding the annotation before the class,


__Source:__

```python

@LimitCalls(max_hits=1, log_calls=True)
class Foo:
    def __init__(self):
        print("inside Foo.__init__")
        self = 42

    def do_something(self):
        print("do_something in Foo")


foo = Foo()
foo.do_something()

```

__Result:__

```
>> LimitCalls function: None max_hits: 1 log_calls: True
>> wrapper function: <class '__main__.Foo'>
>> Calling: Foo #call: 1 positional-arguments: keyword-arguments:
>> inside Foo.__init__
>> Return from: Foo #call: 1 return-value: <__main__.Foo object at 0x104627c50>
>> do_something in Foo
```

Now the following doesn't work.
We can't use this to decorate an instance member, this results in the following error;
"missing 1 required positional argument: 'self'"
The reason is, that the \_\_call\_\_ method of the \_LimitCalls class is not passed the self reference of foo2.


__Source:__

```python

#
#class Foo2:
#    def __init__(self):
#        print("inside Foo2.__init__")
#        self = 42
#
#    @LimitCalls(log_calls=True)
#    def do_something(self):
#        print("do_something in Foo2")
#
#
#foo2 = Foo2()
#foo2.do_something()
#

```

## <a id='s1-2' />Decorators with first class functions/Closures


### <a id='s1-2-1' />First class functions/Closures in Python

The following example shows the use of a function create\_function\_as\_value, that returns a function object nested\_function as a return value.
Note that the returned function can still access all of the variables and parameters of its parent function, these values are said to be 'captured' in the returned function object.


__Source:__

```python

def create_function_as_value(name):
    def nested_function():
        print("captured variable:", name)
        return name
    return nested_function

function_as_value1 = create_function_as_value("Wall-e")
function_as_value2 = create_function_as_value("Pooh")

print("show the captured variable function_as_value1():", function_as_value1())
print("show the captured variable function_as_value2():", function_as_value2())


```

__Result:__

```
>> captured variable: Wall-e
>> show the captured variable function_as_value1(): Wall-e
>> captured variable: Pooh
>> show the captured variable function_as_value2(): Pooh
```

There is a saying [Closures are the poor mans objects](https://stackoverflow.com/questions/2497801/closures-are-poor-mans-objects-and-vice-versa-what-does-this-mean), don't know who the poor man is, some languages, like Haskell, do without object systems at all. I think, it means that both objects and closures are equivalent means of storing state.
Let's see, how this concept is put to use with decorators

### <a id='s1-2-2' />Decorators by means of first class functions/closures

Time to examine other options. Python people like to do decorators with first class functions, that means lots of closures and functions returning closures/function values.
In my book that is a bit of a brain damage, but let's go for it, real pythonistas are not afraid of brain damage! (i think that's quotable ;-))

You have a very good tutorial in the [Primer on Python Decorators by Geir Arne Hjelle](https://realpython.com/primer-on-python-decorators) 
This one here is a bit more condensed.

Lets do the LimitCalls decorator in this style:
if the decorator is called with default arguments, then the \_func argument is set,


__Source:__

```python

def LimitCalls2(_func = None, *,  max_hits = 3, log_calls = False):

    print("LimitCalls2 _func:", _func, "max_hits:", max_hits, "Log_calls:", log_calls)

    # forward_func_call : this inner function is a closure, that receives the function that is to be wrapped/extended by the decorator
    # all parameters of the decorator are visible within the forward_func_call closure, and it's inner function (which does the forwarding/extending)
    def forward_func_call(func):
        print("LimitCalls in nested forward_func_call. func:", func)

        # similar to functool.update_wrapper
        # the __name__ and __doc__ string of the wrapped function is forwarded to the decorator.
        # the decorator also gets a __wrapped__ attribute, which points to the original function that is being wrapped.
        # full list of forwarded attributes (right now) is __name__, ___qualname_, __doc__, __module__, __module__, __annotations__ 
        # also all entries of __dict__ of the wrapped function are updated into the __dict__ of the decorator.
        @functools.wraps(func)

        # the wrapper function call the function that is wrapped/extended by the decorator.
        # Here you can add some action before and after the call of the wrapped function
        # this function is the return value of the forward_func_call closure.
        def wrapper(*args, **kwargs):

            # num_calls is a member of the wrapper function object, see code after this nested function, where this member is initialised. (brain hurts, i know...)
            # and PyLint complaints about such usage...
            wrapper.num_calls += 1

            # max_hits is not a member of the wraper function object, we use the captured argument from the outer function (two levels nesting)
            if wrapper.num_calls > max_hits:
                raise ValueError(f"function {func.__name__} number of call limit {max_hits} has been exceeded")

            if log_calls:
                print("Calling:", func.__name__,"#call:", wrapper.num_calls, "positional-arguments:", *args, "keyword-arguments:", **kwargs)


            value = func(*args, **kwargs)

            if log_calls:
                print("Return from:", func.__name__, "#call:", wrapper.num_calls, "return-value:", value)
            return value

        # state: the wrapper function is an object, it has a __dict__ member, so you can add members, just like with a regular object.
        wrapper.num_calls = 0

        # forward_func_call really returns the inner wrapper function (the wraper function forwards the call to the function that is wrapped by the decorator)
        return wrapper

    # back another nested function nesting...
    if _func is None:
        return forward_func_call

    return forward_func_call(_func)

```
Calling without parameters: this declaration first calls the LimitCalls2 function with function argument set to the argument function dec\_three\_from\_me.
LimitCalls2 then calls the nested function forward\_fun\_call, and returns the initialised wrapper, which is then assigned to dec\_three\_from\_me variable.


__Source:__

```python

@LimitCalls2
def dec_three_from_me(arg_num):
    return arg_num - 1

print("type(dec_three_from_me) : ", type(dec_three_from_me))
print("dec_three_from_me.__name__ : ", dec_three_from_me.__name__)
print("dec_three_from_me.__doc__ : ", dec_three_from_me.__doc__)

for idx in range(1, 5):
    print("idx:", idx)
    got_value_error = False
    try:
        print("call #", idx, "returns: ", dec_three_from_me(idx))
    except ValueError:
        got_value_error = True
    if idx == 4:
        assert got_value_error

```

__Result:__

```
>> LimitCalls2 _func: <function dec_three_from_me at 0x104641760> max_hits: 3 Log_calls: False
>> LimitCalls in nested forward_func_call. func: <function dec_three_from_me at 0x104641760>
>> type(dec_three_from_me) :  <class 'function'>
>> dec_three_from_me.__name__ :  dec_three_from_me
>> dec_three_from_me.__doc__ :  None
>> idx: 1
>> call # 1 returns:  0
>> idx: 2
>> call # 2 returns:  1
>> idx: 3
>> call # 3 returns:  2
>> idx: 4
```

The next example uses the @LimitCalls2 decorator with configuration parameters set.
This declaration first calls the LimitCalls2 function with function argument set to None, but with the other decorator arguments (max\_hits and log\_calls) set.
The LimitCalls2 function returns a reference to the nested closure forward\_func\_call
The Python runtime then calls forward\_func\_call, which returns the still nested closure wrapper, the wrapper has captured the decoator configuration parameters (max\_hits and log\_calls).

The result: it works, but poor programmer will probably need a drink here.


__Source:__

```python

@LimitCalls2(max_hits=2, log_calls=True)
def dec_me(arg_num):
    return arg_num - 1

for idx in range(1, 4):
    print("idx:", idx)
    got_value_error = False
    try:
        print("call #", idx, "returns: ", dec_me(idx))
    except ValueError:
        got_value_error = True
    if idx == 3:
        assert got_value_error

```

__Result:__

```
>> LimitCalls2 _func: None max_hits: 2 Log_calls: True
>> LimitCalls in nested forward_func_call. func: <function dec_me at 0x104641da0>
>> idx: 1
>> Calling: dec_me #call: 1 positional-arguments: 1 keyword-arguments:
>> Return from: dec_me #call: 1 return-value: 0
>> call # 1 returns:  0
>> idx: 2
>> Calling: dec_me #call: 2 positional-arguments: 2 keyword-arguments:
>> Return from: dec_me #call: 2 return-value: 1
>> call # 2 returns:  1
>> idx: 3
```

Lets add the decorator the class declaration. It captures the class \_\_init\_\_ method.


__Source:__

```python

@LimitCalls2(max_hits=1, log_calls=True)
class Foo3:
    def __init__(self):
        print("inside Foo3.__init__")
        self = 42

    def do_something(self):
        print("do_something in Foo3")


foo = Foo3()
foo.do_something()

```

__Result:__

```
>> LimitCalls2 _func: None max_hits: 1 Log_calls: True
>> LimitCalls in nested forward_func_call. func: <class '__main__.Foo3'>
>> Calling: Foo3 #call: 1 positional-arguments: keyword-arguments:
>> inside Foo3.__init__
>> Return from: Foo3 #call: 1 return-value: <__main__.Foo3 object at 0x104645090>
>> do_something in Foo3
```

This time. the decorator even works on an instance method!
the extra effort was worth it!
Three cheers for python!


__Source:__

```python

class Foo4:
    def __init__(self):
        print("inside Foo4.__init__")
        self = 42

    @LimitCalls2(log_calls=True)
    def do_something(self):
        print("do_something in Foo4")

foo = Foo4()
foo.do_something()

```

__Result:__

```
>> LimitCalls2 _func: None max_hits: 3 Log_calls: True
>> LimitCalls in nested forward_func_call. func: <function Foo4.do_something at 0x1046428e0>
>> inside Foo4.__init__
>> Calling: do_something #call: 1 positional-arguments: <__main__.Foo4 object at 0x104645510> keyword-arguments:
>> do_something in Foo4
>> Return from: do_something #call: 1 return-value: None
```


## <a id='s1-3' />Decorators in the python standard library


### <a id='s1-3-1' />@staticmethod and @classmethod

@staticmethod and @classmethod are built-in decorators, you don't have to import any package in order to use them

A method that is declared with the @staticmethod decorator, does not have a self parameter. 
This means, that it can't access the objects instance members. 
You can use this feature to add static functions to a class, that do not require access to the the objects state.

[documentation](https://docs.python.org/3/library/functions.html#staticmethod) 



__Source:__

```python

class Math:
    @staticmethod
    def abs(num_arg):
        ''' return the absolute of a number'''
        if num_arg < 0:
            return -num_arg
        return num_arg
    
    @staticmethod
    def random():
        ''' return a random number betweeen 0 and 1'''
        import random
        return random.uniform(0, 1)


# call the Math.abs method - you need to specify the class name in the call        
print("absolute of a number: ", Math.abs(-3))
print("random number between 0 and 1", Math.random())

# you can also call a static method, given a object of the class.
math_obj = Math()
print("random number between 0 and 1", math_obj.random())

```

__Result:__

```
>> absolute of a number:  3
>> random number between 0 and 1 0.6358851206415842
>> random number between 0 and 1 0.6791998526131846
```

A method that is declared with the @classmthod decorator, here the first parameter is the class object. Note that a method like this doesn't have a self parameter.
A method like this can access all the static data of the class, however the instance data can't be accessed, as there is no self parameter.

This feature can be used to address a limitation of the python syntax, In Python you can have only one \_\_init\_\_ method, that means there  one constructor available.
This feature allows you to add additional constructors, or factory methods. like the from\_name class method in the following example:


__Source:__

```python


class Colour:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    # calling this method as Colour.from_name, will pass the clas Colour as the first parameter
    @classmethod
    def from_name(cls, colour_name):
        named_colours = { 'black' : (0,0,0), 'white' : (255,255,255), 'red' : (255, 0, 0, 0) }

        # using the class parameter in order to create the colour instance
        rgb = named_colours[ colour_name ]
        return cls( rgb[0], rgb[1], rgb[2] )

colour_red = Colour.from_name('red')
print("color red: ", colour_red , "red:", colour_red.red , "green:", colour_red.green, "blue:", colour_red.blue)

```

__Result:__

```
>> color red:  <__main__.Colour object at 0x104650c90> red: 255 green: 0 blue: 0
```

At first it doesn't make an awfull lot of sense, but lets derive the ColourWithAlphaChannel class from Colour.
Nnow you can create a ColourWithAlphaChannel object, by means of the same same constructor/factory method from\_name
It calls the correct \_\_init\_\_ method, based on the class instance passed to the from\_name class method



__Source:__

```python

class ColourWithAlphaChannel(Colour):
    def __init__(self, red, green, blue, alpha):
        self.alpha = alpha
        super().__init__(red, green, blue)

    @classmethod
    def from_name(cls_, colour_name, alpha):
        cval = Colour.from_name(colour_name) 
        return cls_(cval.red, cval.green, cval.blue, alpha)

# now you can create a ColourWithAlphaChannel object, by means of the same same constructor/factory method from_name
#It calls the correct __init__ method, based on the class instance passed to the from_name class method

colour_red = ColourWithAlphaChannel.from_name( "red", 1.0)
print("color red: ", colour_red , "red:", colour_red.red , "green:", colour_red.green, "blue:", colour_red.blue, "alpha:", colour_red.alpha)

```

__Result:__

```
>> color red:  <__main__.ColourWithAlphaChannel object at 0x104650e10> red: 255 green: 0 blue: 0 alpha: 1.0
```

Other examples of alternate constructors in the standard library: 
- [classmethod dict.fromkeys](https://docs.python.org/3/library/stdtypes.html#dict.fromkeys)  Create a new dictionary with keys from iterable and values set to value.
- [classmethod int.from\_bytes](https://docs.python.org/3/library/stdtypes.html#int.from\_bytes) Return the integer represented by the given array of bytes.



### <a id='s1-3-2' />The functools library

The [functools library](https://docs.python.org/3/library/functools.html) comes as part of the python standard library.
his library comes with some interesting decorators. 

Please look at the [documentation](https://docs.python.org/3/library/functools.html) for the full set of decorators, provided by this library, this text doesn't cover it all.

The decorator [@functools.cache](https://docs.python.org/3/library/functools.html#functools.cache) will cache the return value of a function, based on the arguments of the call.
Let's use is with the fibonacci function, the fib function is invoced exactly once for each argument.
Without this decorator, it woulld have been called over and over again.
The @functool.cache turns the fib function into a dynamic programming solution. 
You can try that as an answer at a job interview, let me know if this approach worked ;-)


__Source:__

```python

import functools

@functools.cache
def fib(arg_num):
    print("fib arg_num:", arg_num)
    if arg_num<2:
        return arg_num
    return fib(arg_num-1) + fib(arg_num-2)

print("computing the fibonacci number of fib(30): ", fib(30))

```

__Result:__

```
>> fib arg_num: 30
>> fib arg_num: 29
>> fib arg_num: 28
>> fib arg_num: 27
>> fib arg_num: 26
>> fib arg_num: 25
>> fib arg_num: 24
>> fib arg_num: 23
>> fib arg_num: 22
>> fib arg_num: 21
>> fib arg_num: 20
>> fib arg_num: 19
>> fib arg_num: 18
>> fib arg_num: 17
>> fib arg_num: 16
>> fib arg_num: 15
>> fib arg_num: 14
>> fib arg_num: 13
>> fib arg_num: 12
>> fib arg_num: 11
>> fib arg_num: 10
>> fib arg_num: 9
>> fib arg_num: 8
>> fib arg_num: 7
>> fib arg_num: 6
>> fib arg_num: 5
>> fib arg_num: 4
>> fib arg_num: 3
>> fib arg_num: 2
>> fib arg_num: 1
>> fib arg_num: 0
>> computing the fibonacci number of fib(30):  832040
```

A few word of caution: the @functools.cache decorator will not work, if the decorated function has side effects.
Also beware that the cache size is not limited, this can result in a huge memory consumption, if the cache is not cleared.
There is also a way to show the cache usage statistics:


__Source:__

```python

#calling the functions of the decorator, to get cache statistics.
print("cache statistics:",fib.cache_info())
print("clearing the cache")
fib.cache_clear()
print("cache statistics after cache_clear:",fib.cache_info())

```

__Result:__

```
>> cache statistics: CacheInfo(hits=28, misses=31, maxsize=None, currsize=31)
>> clearing the cache
>> cache statistics after cache_clear: CacheInfo(hits=0, misses=0, maxsize=None, currsize=0)
```

Some more words of caution: The key that is used to map the function argument to the return value is used [as follows](https://github.com/python/cpython/blob/f6648e229edf07a1e4897244d7d34989dd9ea647/Lib/functools.py#L448) : it makes a tuple that consists of all function arguments, and computes the hash of that tuple.
Now you have a problem with keyword arguments, as the tuple from these two function calls will result in different hash values: foo(a=1, b=2) and foo(b=2, a=1). 
The comments in the code mention, that a previous version was sorting the keyword argument by name, before doing the hash; however this was considered to be too slow.
Here you get your trade offs...

There is also a least recently used cache [@functools.lru\_cache](https://docs.python.org/3/library/functools.html#functools.lru\_cache), of limited size.
Note that you get the same number of cache hits for the bounded cache, on the fibonacci function  (author is scratching his head)
This happens, of course, as only the last two results are needed for the fibonacci sequence!


__Source:__

```python

@functools.lru_cache(maxsize=5)
def fib2(arg_num):
    print("fib2 arg_num:", arg_num)
    if arg_num<2:
        return arg_num
    return fib2(arg_num-1) + fib2(arg_num-2)

print("computing the fibonacci number of fib2(30): ", fib2(30))
print("cache statistics:",fib2.cache_info())

```

__Result:__

```
>> fib2 arg_num: 30
>> fib2 arg_num: 29
>> fib2 arg_num: 28
>> fib2 arg_num: 27
>> fib2 arg_num: 26
>> fib2 arg_num: 25
>> fib2 arg_num: 24
>> fib2 arg_num: 23
>> fib2 arg_num: 22
>> fib2 arg_num: 21
>> fib2 arg_num: 20
>> fib2 arg_num: 19
>> fib2 arg_num: 18
>> fib2 arg_num: 17
>> fib2 arg_num: 16
>> fib2 arg_num: 15
>> fib2 arg_num: 14
>> fib2 arg_num: 13
>> fib2 arg_num: 12
>> fib2 arg_num: 11
>> fib2 arg_num: 10
>> fib2 arg_num: 9
>> fib2 arg_num: 8
>> fib2 arg_num: 7
>> fib2 arg_num: 6
>> fib2 arg_num: 5
>> fib2 arg_num: 4
>> fib2 arg_num: 3
>> fib2 arg_num: 2
>> fib2 arg_num: 1
>> fib2 arg_num: 0
>> computing the fibonacci number of fib2(30):  832040
>> cache statistics: CacheInfo(hits=28, misses=31, maxsize=5, currsize=5)
```

And now for an examples, where decorators are being used as [metaprogramming tools](https://en.wikipedia.org/wiki/Metaprogramming), as tools that transform programs, in a sense similar to lisp macros. The [@functools.total\_ordering](https://docs.python.org/3/library/functools.html#functools.total\_ordering) decorator is applied to a class, this makes it intercept the \_\_init\_\_ method of the decorated class, as we saw earlier. This gives it the opportunity to add methods to the class.

The decroated class must support two operator function, it must support the \_\_eq\_\_ method and also define either oneone of the following: \_\_lt\_\_(), \_\_le\_\_(), \_\_gt\_\_(), or \_\_ge\_\_()
The [@functools.total\_ordering](https://docs.python.org/3/library/functools.html#functools.total\_ordering) decorator then adds all the other missing comparison operators.


__Source:__

```python


@functools.total_ordering
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __eq__(self, other):
        return (self.first_name, other.last_name) == (self.first_name, other.last_name)

    def __lt__(self, other):
        return (self.first_name, self.last_name) < (other.first_name, other.last_name)
            
person_a = Person("Jack", "Bean")
person_b = Person("Patricia", "Donovan")

print("person_a.__dict__ : ", person_a.__dict__)
print("person_b.__dict__ : ", person_b.__dict__)

assert person_a == person_b
assert person_a < person_b
# the added operators
assert not person_a != person_b
assert person_a <= person_b
assert not person_a > person_b
assert not person_a >= person_b

```

__Result:__

```
>> person_a.__dict__ :  {'first_name': 'Jack', 'last_name': 'Bean'}
>> person_b.__dict__ :  {'first_name': 'Patricia', 'last_name': 'Donovan'}
```


### <a id='s1-3-3' />dataclasses

Dataclasses can be used as an alternative to tuples. It makes it easier to create classes that hold a defined set of named properties.
The @dataclass decorator is applied to the class declaration, this allows the decorator to add the missing methods to the class.



__Source:__

```python


import dataclasses

@dataclasses.dataclass
class Person:
    first_name: str
    last_name: str
    rank: int

person = Person('Roy', 'Mustang', 1)
print("Person:", person)

```

__Result:__

```
>> Person: Person(first_name='Roy', last_name='Mustang', rank=1)
```

More documentation is available [here](https://docs.python.org/3/library/dataclasses.html)

### <a id='s1-3-4' />contextlib

This decorator helps to create contextmanager classes, these are classes that acquire and release resources and are used implicitly by the python with statement.
- Python calls an \_\_enter\_\_ method of a context manager instance, when entering a block nested within a with statement, in order to acquire a resource.
- Python calls the \_\_exit\_\_ method on a context manager instance, when exiting a block nested within a with statement, in order to release a resource. 

More on context managers and the with statment in [PEP-0343](https://www.python.org/dev/peps/pep-0343/)  

The contextlib.contextmanager decorator helps to simplify matters. It uses python generators for the trick, the resource is acquired before the yield statement, and released upon returning from the yield statement.

In this example, the resource is acquired by opening a file and obtaining a lock on tha file. The resource is released by releasing the file lock and closing the file.


__Source:__

```python


import contextlib
import fcntl

@contextlib.contextmanager
def writable_file_with_lock_exclusive(file_path):
    print("opening file for writing and locking file exclusively:", file_path)
    file = open(file_path, mode="w")
    fcntl.lockf(file.fileno(), fcntl.LOCK_EX)
    try:
        print("calling yield...")
        yield file
        print("returning from yield...")
    finally:
        print("unlocking and closing file:", file_path)
        fcntl.lockf(file.fileno(), fcntl.LOCK_UN)
        file.close()

@contextlib.contextmanager
def readable_file_with_lock_shared(file_path):
    print("opening file for reading and locking file shared:", file_path)
    file = open(file_path, mode="r")
    fcntl.lockf(file.fileno(), fcntl.LOCK_SH)
    try:
        print("calling yield...")
        yield file
        print("returning from yield...")
    finally:
        print("unlocking and closing file:", file_path)
        fcntl.lockf(file.fileno(), fcntl.LOCK_UN)
        file.close()

```
Using the resulting decorator

__Source:__

```python


with writable_file_with_lock_exclusive("hello.txt") as file:
    print("writing to the file...")
    file.write("hello.txt")

print("reading the file")

with readable_file_with_lock_shared("hello.txt") as file:
    lines = file.readlines()
    print("the file:", lines)


```

__Result:__

```
>> opening file for writing and locking file exclusively: hello.txt
>> calling yield...
>> writing to the file...
>> returning from yield...
>> unlocking and closing file: hello.txt
>> reading the file
>> opening file for reading and locking file shared: hello.txt
>> calling yield...
>> the file: ['hello.txt']
>> returning from yield...
>> unlocking and closing file: hello.txt
```

More documentation is available [here](https://docs.python.org/3/reference/datamodel.html#context-managers)
        

*** eof tutorial ***

