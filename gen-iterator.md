  * [iterators](#s0-1)
  * [generators](#s0-2)
  * [built-in range function, for iterating over a range of values](#s0-3)


## <a id='s0-1' />iterators


## <a id='s0-2' />generators

Let's examine how generators differ from regular functions. Calling a regular function, will execute the statements of the function, and return the return value of the function

__Source:__

```

def not_a_generator(from_val, to_val):
    return from_val + to_val

print("type(not_a_generator):", not_a_generator)

no_gen_ret_val = not_a_generator(10, 20)
print("type(no_gen_ret_val):", type(no_gen_ret_val))

```

__Result:__

```
>> type(not_a_generator): <function not_a_generator at 0x7f9903de0d30>
>> type(no_gen_ret_val): <class 'int'>
```

Let's look at a generator function, it has a yield statement in its body

__Source:__

```

def my_range(from_val, to_val):
    print("(generator) my_range from_val:", from_val, "to_val:", to_val)

    while from_val < to_val:

        print("(generator) The generator instance is in running state, computes the next value to be returned by the yield statement")
        print("(generator) inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))

        print("(generator) before yield from_val:", from_val)
        yield from_val
        from_val += 1

    print("(generator) leaving the generator function, iteration is finished")

```
A function that has a yield statement, is is still a function objct.

__Source:__

```

print("type(my_range):", type(my_range))

```

__Result:__

```
>> type(my_range): <class 'function'>
```

You can tell, if a function has a yield statement, or not, the function object owns a \_\_code\_\_ attribute, which has a flag set, if it includes a yield statment, that's what inspect.isgeneratorfunction is checking.

__Source:__

```

import inspect 

assert inspect.isgeneratorfunction(my_range)
assert not inspect.isgeneratorfunction(not_a_generator)


```
Digression: the \_\_code\_\_ attribute of a function object stands for the compiled byte code of a function. (but that's another rabbit hole)

__Source:__

```

print("type(my_range.__code__):", type(my_range.__code__))
print("dir(my_range.__code__):", dir(my_range.__code__))

```

__Result:__

```
>> type(my_range.__code__): <class 'code'>
>> dir(my_range.__code__): ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_posonlyargcount', 'co_stacksize', 'co_varnames', 'replace']
```

Attention! Calling the generator function does not execute any of the statements in the body of the function! (you won't see the print at the start of my\_range), instead it returns a generator object. 

__Source:__

```

print("calling: my_range(10,20)")
range_generator = my_range(10,12)
print("type(range_generator):", type(range_generator))

```

__Result:__

```
>> calling: my_range(10,20)
>> type(range_generator): <class 'generator'>
```

The generator has not been invoked yet, it is in created state

__Source:__

```

print("inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator)) 

```

__Result:__

```
>> inspect.getgeneratorstate(range_generator): GEN_CREATED
```

Let's examine the generator object. Generators are iterators, they have the special \_\_iter\_\_ and \_\_next\_\_ attribute. Additional special attributes of generator objects: 'close', 'gi\_code', 'gi\_frame', 'gi\_running', 'gi\_yieldfrom', 'send', 'throw' 

__Source:__

```

print("dir(range_generator):", dir(range_generator))
print("dir(type(range_generator):", dir(type(range_generator)))

```

__Result:__

```
>> dir(range_generator): ['__class__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__next__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom', 'send', 'throw']
>> dir(type(range_generator): ['__class__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__next__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom', 'send', 'throw']
```

Using the generator as an iterator: calling next(range\_generator)...

__Source:__

```

val = next(range_generator)
print("return value of next(range_generator):", val)

```

__Result:__

```
>> (generator) my_range from_val: 10 to_val: 12
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 10
>> return value of next(range_generator): 10
```

The generator is in suspended state, after having returned it's value via the yield statement

__Source:__

```

print("inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))

```

__Result:__

```
>> inspect.getgeneratorstate(range_generator): GEN_SUSPENDED
```

Calling built-in next(range\_generator) is the same as calling range\_generator.\_\_next\_\_() ...

__Source:__

```

val = range_generator.__next__()
print("return value of next(range_generator):", val)

```

__Result:__

```
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 11
>> return value of next(range_generator): 11
```

When the generator function is exiting: a StopIteration exception is raised. I was surprised, that python is using exceptions, as part of regular control flow!
But it makes sence: raising an exception is different, and can't be confused with returning a regular return value

__Source:__

```

has_stop_iter_ex = False
try:
    val = range_generator.__next__()
except StopIteration as stop_iter:
    print("Upon leaving the generator function, received exception of type(stop_iter):", type(stop_iter))
    has_stop_iter_ex = True

assert has_stop_iter_ex

```

__Result:__

```
>> (generator) leaving the generator function, iteration is finished
>> Upon leaving the generator function, received exception of type(stop_iter): <class 'StopIteration'>
```

The gnerator object is in closed state, upon having completed its iteration

__Source:__

```

print("inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))

```

__Result:__

```
>> inspect.getgeneratorstate(range_generator): GEN_CLOSED
```

Using an generator in a for loop, The for loop uses it as an iterator

__Source:__

```

range_generator = my_range(0,7)
for num in range_generator:
    print("num:", num)

```

__Result:__

```
>> (generator) my_range from_val: 0 to_val: 7
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 0
>> num: 0
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 1
>> num: 1
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 2
>> num: 2
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 3
>> num: 3
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 4
>> num: 4
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 5
>> num: 5
>> (generator) The generator instance is in running state, computes the next value to be returned by the yield statement
>> (generator) inspect.getgeneratorstate(range_generator): GEN_RUNNING
>> (generator) before yield from_val: 6
>> num: 6
>> (generator) leaving the generator function, iteration is finished
```


## <a id='s0-3' />built-in range function, for iterating over a range of values

built in range function returns an object of built-in type range, the range object is not a generator, the range object returns an iterator, it has an \_\_iter\_\_ function that returns an iterator object. It makes sense to avoid generators for the built-in range function: generators are slower, as they need to switch the stack back and forth between the generator function and the for loop that is using it

__Source:__

```

range_value = range(1,10)
print("type(range_value):", type(range_value))
assert not inspect.isgenerator(range_value)
print("dir(range_value):", dir(range_value))

```

__Result:__

```
>> type(range_value): <class 'range'>
>> dir(range_value): ['__bool__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index', 'start', 'step', 'stop']
```

Each call to the \_\_iter\_\_() member of the range type will return a distinct value of type range\_iterator, here the \_\_next\_\_ member is implemented. 

__Source:__

```

range_iter = range_value.__iter__()
print("type(range_iter):", type(range_iter))
print("dir(range_iter):", dir(range_iter))
assert not inspect.isgenerator(range_iter)

range_iter2 = range_value.__iter__()
print("id(range_iter):", id(range_iter), "id(range_iter2):", id(range_iter2))
assert id(range_iter) != id(range_iter2)

```

__Result:__

```
>> type(range_iter): <class 'range_iterator'>
>> dir(range_iter): ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__length_hint__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__']
>> id(range_iter): 140295171661760 id(range_iter2): 140295171661712
```

Returning a separate range\_iter object on each call to \_\_iter\_\_ makes sense: 
You can use the same range object in different for loops, each time an independent sequence of values is returned!

__Source:__

```

range_val = range(1,3)
for val in range_val:
    print("iteration1:", val)
for val in range_val:
    print("iteration2:", val)

```

__Result:__

```
>> iteration1: 1
>> iteration1: 2
>> iteration2: 1
>> iteration2: 2
```

*** eof lesson ***

