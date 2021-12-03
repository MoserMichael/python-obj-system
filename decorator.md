" Set text width as 72.


# Python decorator walkthrough


## Callable objects

A class is callable, if an object of the class can be called as a function.
This requires us to define a \_\_call\_\_ instance method
Let's look at an example:


__Source:__
```

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

This examples show a callbable object that accepts additional parameters, like a real function.
Here we need to add parameters to the \_\_call\_\_ method.


__Source:__
```

class CallableObject2:
    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, x, y):
        print(type(self), self.prefix, "x:", x, "y:", y)

callable_obj = CallableObject2("callable with arguments")
callable_obj(2,3)

```

__Result:__
```
>> <class '__main__.CallableObject2'> callable with arguments x: 2 y: 3
```


## Simple decorators

Function decorators take a given function, and intercept the call to that function. They act as a kind of proxy for calls of a given function.
This gives them the chance to add the following behavior:
  - add code that is run before calling the intercepted function, it can also possibly alter the arguments of the function call
  - add code that is run after calling the intercepted function, it can also alter the return value of the original function, before it is returned to the caller.
A function decorator therefore acts as a kind of 'smart proxy' around a given python function.

Lets start with an interceptor class, the class receives the wrapped function as an argument to its \_\_init\_\_ method;
The class is a callable object, and it calls the original function in its \_\_call\_\_ method.
The style of doing it as a class has a big plus: you can easily instance variables to the decorator.

Here is the decorator class, that intercepts the calls to an argument function:


__Source:__
```

class CountCalls:

    # init method, gets the original function reference,
    # the CountCalls decorator forwards arguments to this original function, and it does so with style...
    def __init__(self, func):

        # copy the __name__, ___qualname_, __doc__, __module__, __module__, __annotations__ attributes of the function argument into _LimitCalls instance,
        # as well as all entries in __dict__ into this instance __dict__ member.
        # this is in order ot make the wrapper look the same as the wrapped function.
        functools.update_wrapper(self, func)

        # the forwarded function is copied, so that __call__ will be able to forward the call.
        self.func = func

        # set the state variable, the number of calls, that is update upon each call.
        self.num_calls = 0

    # the __call__ function is called, when an instance of the CounCalls class is used as a function.
    # gets both positional arguments *args and keyword arguments **kwargs, these are all forwarded to the original function.
    def __call__(self, *args, **kwargs):

        # count the number of invocations.
        self.num_calls += 1

        # log that we are about to forward the call to the original function
        print("Calling:", self.func.__name__, "#call:", self.num_calls, "positional-arguments:", *args, "keyword-arguments:", **kwargs)

        # forward the call.
        ret_val = self.func(*args, **kwargs)

        # log the event, that we returned from the original function. Also log the return value of the original function
        print("Return from:", self.func.__name__, "#call:", self.num_calls, "return-value:", ret_val)

        # return the value of the original function call is returned to the caller
        return ret_val

```
Lets intercept the say\_miau function.


__Source:__
```

def say_miau():
    ''' docstring: print the vocalization of a Felis Catus, also known as cat '''
    print("Miau!")

# the global variable say_miau  now refers to an object, that wraps the original say_miau function.
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
```

# the type of the wrapped object is CountCalls
print("type(say_miau) : ", type(say_miau))

# but the name and docstring are copied from the wrapped object, because of the call to functools.update_wrapper
# This way, the decorated function appears as the original function, despite it having been wrapped.
print("say_miau.__name__ : ", say_miau.__name__)
print("say_miau.__doc__ : ", say_miau.__doc__)

```

__Result:__
```
>> type(say_miau) :  <class '__main__.CountCalls'>
>> say_miau.__name__ :  say_miau
>> say_miau.__doc__ :   docstring: print the vocalization of a Felis Catus, also known as cat
```

Attention!
Here is the equivalent way of setting up the decorator instance! just as the previous case, only for the say\_woof method.
the @ syntax is supposed to be a shorter way of doing it.


__Source:__
```

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
```

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


## Decorators that can receive parameters

Lets look at the LimitCalls decorator, it can be used in different scenarios, it receives the following arguments 
  - log\_calls - a boolean, it logs the call if set. 
  - max\_calls - the maximum number of calls, if decorator does not forward the call to the original function, when the limit on the number of calls has been reached.

The class \_LimitCalls starts with an underscore, to show that this is a private class, that is not supposed to be exported from a module.


__Source:__
```

class _LimitCalls:
    def __init__(self, function, max_hits, log_calls):

        # copy the __name__, ___qualname_, __doc__, __module__, __module__, __annotations__ attributes of the function argument into _LimitCalls instance,
        # as well as all entries in __dict__ into this instance __dict__ member.
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
        return _LimitCalls(function, max_hits, log_calls)

    return wrapper

```
Lets use the LimitCalls decorator
The defauls values for the parameters of the decorator are used. the LimitCalls function is called gets the the square\_me function as parameter


__Source:__
```

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
>> LimitCalls function: <function square_me at 0x7fac7fdd6c10> max_hits: 3 log_calls: False
>> square_me type:  <class '__main__._LimitCalls'>
>> idx: 1
>> call # 1 returns:  4
>> idx: 2
>> call # 2 returns:  9
>> idx: 3
>> call # 3 returns:  16
```

setting non default value for the decorator parameters.
first the LimitCalls function is called with function=None, and maxhits=4, log\_calls=True
The first call returns the internal function wrapper.
then function wrapper iscalled with the function parameter set to cube\_me. this returns the \_LimitCall2 object.


__Source:__
```

@LimitCalls(max_hits=4, log_calls=True)
def cube_me(arg_num):
    ''' return a cube of the argument '''
    return arg_num * arg_num * arg_num

```

__Result:__
```
>> LimitCalls function: None max_hits: 4 log_calls: True
```

cube\_me is a variable of type \_LimitCalls


__Source:__
```

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

Can we use the @LimitCalls decorator with a class method? lets try.
Adding the annotation before the class, only the \_\_init\_\_ method gets intercepted.


__Source:__
```

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
>> Calling: Foo #call: 1 positional-arguments: keyword-arguments:
>> inside Foo.__init__
>> Return from: Foo #call: 1 return-value: <__main__.Foo object at 0x7fac7fde0d00>
>> do_something in Foo
```

Now the following doesn't work.
We can't use this to decorate an instance member, this results in the following error;
"missing 1 required positional argument: 'self'"
The reason is, that the \_\_call\_\_ method of the \_LimitCalls class is not passed the self reference of foo2.


__Source:__
```

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

## Decorators by means of first class functions/closures

Time to examine other options. Python people like to do decorators with first class functions, that means lots of closures and functions returning closures/function values.
In my book that is a bit of a brain damage, but let's go for it, real pythonistas are not afraid of brain damage! (i think that's quotable ;-))
You have a very good tutorial here: https://realpython.com/primer-on-python-decorators/#decorating-classes (though it is a bit long wound, in my opinion)
This one here is more condensed.

Lets do the LimitCalls decorator in this style:
if the decorator is called with default arguments, then the \_func argument is set,


__Source:__
```

def LimitCalls2(_func = None, *,  max_hits = 3, log_calls = False):

    print("LimitCalls2 _func:", _func, "max_hits:", max_hits, "Log_calls:", log_calls)

    # forward_func_call : this inner function is a closure, that receives the function that is to be wrapped/extended by the decorator
    # all parameters of the decorator are visible within the forward_func_call closure, and it's inner function (which does the forwarding/extending)
    def forward_func_call(func):
        print("LimitCalls in nested forward_func_call. func:", func)

        # similar to functool.update_wrapper
        # the __name__ and __doc__ string of the wrapped function is forwarded to the decorator.
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
calling without parameters
this declaration first calls the LimitCalls2 function with function argument set to dec\_three\_from\_me
LimitCalls2 then calls the nested function forward\_fun\_call, and returns the initialised wrapper, which is then assigned to dec\_three\_from\_me variable.


__Source:__
```

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
>> LimitCalls2 _func: <function dec_three_from_me at 0x7fac7fde3d30> max_hits: 3 Log_calls: False
>> LimitCalls in nested forward_func_call. func: <function dec_three_from_me at 0x7fac7fde3d30>
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

The next example uses the @LimitCalls2 decorator with on a function with arguments.
This declaration first calls the LimitCalls2 function with function argument set to None, but with the other decorator arguments (max\_hits and log\_calls) set.
The LimitCalls2 function returns a reference to closure forward\_func\_call
The Python runtime then calls forward\_func\_call, which returns the still nested closure wrapper has captured the other decorator arguments (max\_hits and log\_calls).
The result: it works, but poor programmer will probably need a drink here.


__Source:__
```

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
>> LimitCalls in nested forward_func_call. func: <function dec_me at 0x7fac7fde5310>
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

Lets add the decorator the function declaration. It captures the class \_\_init\_\_ method.


__Source:__
```

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
>> Return from: Foo3 #call: 1 return-value: <__main__.Foo3 object at 0x7fac7fde1040>
>> do_something in Foo3
```

This time. the decorator even works on instance methods!!! 
the extra effort was worth it!
Three cheers for python!


__Source:__
```

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
>> LimitCalls in nested forward_func_call. func: <function Foo4.do_something at 0x7fac7fde5f70>
>> inside Foo4.__init__
>> Calling: do_something #call: 1 positional-arguments: <__main__.Foo4 object at 0x7fac7fde1d30> keyword-arguments:
>> do_something in Foo4
>> Return from: do_something #call: 1 return-value: None
```


## Decorators in the python standard library


### @staticmethod and @classmethod

@staticmethod and @classmethod are built-in decorators, you don't have to import any package in order to use them

@staticmethod -  a method that is annotated with @staticmethod does not have a self parameter. 
That means it can't access the objects instance members. 
You can use this feature to add functions to a class, that do not require access to the state of any object of the class.

[documentation](https://docs.python.org/3/library/functions.html#staticmethod) 



__Source:__
```

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

```

__Result:__
```
>> absolute of a number:  3
>> random number between 0 and 1 0.9926990641412625
```

@classmethod - a method that is annotated with the @staticmethod. It does not have a self parameter, but it has a parameter of the class object.

A method like this can access all the static data of it's class, but no instance data can be accessed, as there is no self parameter.

This feature can be used to address a limitation of the python syntax, In Python you can have only one \_\_init\_\_ method, that means there  one constructor available.
This feature allows you to add additional constructors, or factory methods. like the from\_name class method in the following example:


__Source:__
```


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
>> color red:  <__main__.Colour object at 0x7fac7fdeafa0> red: 255 green: 0 blue: 0
```

At first it doesn't make an awfull lot of sense, but lets derive the ColourWithAlphaChannel class from Colour


__Source:__
```

class ColourWithAlphaChannel(Colour):
    def __init__(self, red, green, blue, alpha):
        self.alpha = alpha
        super().__init__(red, green, blue)

    @classmethod
    def from_name(cls_, colour_name, alpha):
        cval = Colour.from_name(colour_name) 
        return cls_(cval.red, cval.green, cval.blue, alpha)

# now you can create a named colour with the same factory method from_name
# It calls the correct method, based on the class name of the call ColourWithAlphaChannel.from_name( "red", 1.0)

colour_red = ColourWithAlphaChannel.from_name( "red", 1.0)
print("color red: ", colour_red , "red:", colour_red.red , "green:", colour_red.green, "blue:", colour_red.blue, "alpha:", colour_red.alpha)

```

__Result:__
```
>> color red:  <__main__.ColourWithAlphaChannel object at 0x7fac7fde0c70> red: 255 green: 0 blue: 0 alpha: 1.0
```

*** eof tutorial ***
