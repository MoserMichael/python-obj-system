* [Generating sequences dynamically](#s1)
  * [Iterators](#s1-1)
      * [Iterator example](#s1-1-1)
      * [Built-in range function, for iterating over a range of values](#s1-1-2)
  * [Generators](#s1-2)
      * [a generator in action](#s1-2-1)
      * [What is going on here?](#s1-2-2)
  * [Summing it up, so far](#s1-3)
* [AsyncIO, there is much more!](#s2)


# <a id='s1' />Generating sequences dynamically

Both iterators and generators are two ways of generating sequences, in a dynamic fashion. 
There is always the possibility of creating a list, that includes all the members of a desired sequnce. However that may take a lot of time and memory, also you may end up needing only half of the produced items, it is often more practical to create the elements of a sequence upon demand, that's exactly what is done by both iterators and generators.


## <a id='s1-1' />Iterators


### <a id='s1-1-1' />Iterator example

An iterator object is one that returns a sequence of values. the next value of the sequence is returned by the  \_\_next\_\_ member of the iterator object.
The following example returns the first ten fibonacci numbers. The object of type FibIter knows how to compute the current fibonacci number, and to compute the next one.


__Source:__

```


class FibIter:
    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        ret_val = self.b

        next_val = self.a + self.b
        self.a = self.b
        self.b = next_val

        return ret_val


fib_iter = FibIter()

# note that we are calling next(fib_iter) exactly ten times, in order to produce ten fibonacci numbers. 
# It works, but this way of iterating is a bit awkward.
for _ in range(1,10):
    # calling the next built-in function with iterator argument is calling the __next__ member of the iterator object.
    fib_num = next(fib_iter)
    print(fib_num)


```

__Result:__

```
>> 1
>> 1
>> 2
>> 3
>> 5
>> 8
>> 13
>> 21
>> 34
```

We want an iterator object that is usable with the for statement. Here we need to  implement the \_\_iter\_\_ method, this is a factory method for returning an iterator object, this factory method is required by the for statement

__Source:__

```

class InfiniteFibSequence:
    def __init__(self):
        pass

    def __iter__(self):
        return FibIter()
        
for num in InfiniteFibSequence():
    if num > 100:
        break
    print("fibonacci number:", num)

```

__Result:__

```
>> fibonacci number: 1
>> fibonacci number: 1
>> fibonacci number: 2
>> fibonacci number: 3
>> fibonacci number: 5
>> fibonacci number: 8
>> fibonacci number: 13
>> fibonacci number: 21
>> fibonacci number: 34
>> fibonacci number: 55
>> fibonacci number: 89
```

An even better example: we want an iterator object, that returns a given number of fibonacci numbers, then stops the iteration, once all values have been returned.

A StopIteration exception is raised, once the last element of the sequence has been returned. I was surprised, that python is using exceptions, as part of regular control flow! But it makes sence: raising an exception is different, and can't be confused with returning a regular return value.

__Source:__

```


class LimitedFibIter:
    def __init__(self, range_size):
        self.a = 0
        self.b = 1
        self.range_size = range_size
        self.cur_range = 0

    def __next__(self):
        self.cur_range += 1
        if self.cur_range > self.range_size:
            raise StopIteration()
        ret_val = self.b

        next_val = self.a + self.b
        self.a = self.b
        self.b = next_val

        return ret_val

class LimitedFibRange:
    def __init__(self, range_size):
        self.range_size = range_size
        
    def __iter__(self):
        return LimitedFibIter(self.range_size)

for num in LimitedFibRange(10):
    print("fib number:", num)

```

__Result:__

```
>> fib number: 1
>> fib number: 1
>> fib number: 2
>> fib number: 3
>> fib number: 5
>> fib number: 8
>> fib number: 13
>> fib number: 21
>> fib number: 34
>> fib number: 55
```


### <a id='s1-1-2' />Built-in range function, for iterating over a range of values

built in range function returns an object of built-in type [range](https://docs.python.org/3/library/stdtypes.html#range) - it can be used to return a consecutive sequence of numbers. The range object is actually not a generator, the range object returns an iterator, it has an \_\_iter\_\_ function that returns an iterator object.

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

The [inspect module](https://docs.python.org/3/library/inspect.html) actually does not have a function that checks, if an object is an iterator, one would look as follows:

__Source:__

```


import types
import inspect


def isiterator(arg_obj):
    """check if argument object supports the iterator protocol"""
   
    for mem in inspect.getmembers(arg_obj): 
        #ups, the type of 'method-wrapper' appears for stuff written in c. Too much crap to check, in python3...
        #print(mem,type(mem[1]))

        if mem[0] == "__iter__":
            return True
    return False

assert isiterator(range_value)


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
>> id(range_iter): 140463740665312 id(range_iter2): 140463740665360
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


## <a id='s1-2' />Generators


### <a id='s1-2-1' />a generator in action

Let's examine how generator functions differ from regular functions. Calling a regular function, will execute the statements of the function, and return the return value of the function

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
>> type(not_a_generator): <function not_a_generator at 0x7fc0435ed310>
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
A function that has a yield statement, is is technically still a function objct.

__Source:__

```

print("type(my_range):", type(my_range))

```

__Result:__

```
>> type(my_range): <class 'function'>
```

You can tell, if a function has a yield statement, or not, the function object owns a \_\_code\_\_ attribute, which has a flag set, if it includes a yield statment, that's what [inspect.isgeneratorfunction](https://docs.python.org/3/library/inspect.html#inspect.isgeneratorfunction) is checking.

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


### <a id='s1-2-2' />What is going on here?

What is happening here? Both the generator function and it's caller are running as part of the same operating system thread, this thread is hosting the python bytecode interpeter, which is executing both the generator function and its caller.


Now the python bytecode interpreter maintains two separate stack frame entity, one for the generator and one for its caller, A stack [frame object](https://docs.python.org/3/reference/datamodel.html) represents the current function or generator in the python bytecode interpreter. It has a field for the local variables maintained by the function (see f\_locals dictionary member of the frame object) and the current bytecode instruction that is being executed within the function/generator (see f\_lasti member of the frame object). The generator object is put into 'suspended' state, once the generator has called the yield statement, with the aim to return a value to the caller. The generator is later resumed upon calling the next built-in function (next(fib\_gen) in our case), and resumes execution from the bytecode instruction referred to by f\_lasti, with the local variable values referred to by the f\_locals dictionary of the frame object. (are you still with me?)


See the following example:


__Source:__

```


import traceback
import threading

def fib_generator():
    a=0
    b=1

    print("(generator) fib_generator operating system thread_id:", threading.get_ident())
    print("(generator) type(fib_gen.gi_frame):", type(fib_gen.gi_frame), "fib_gen.gi_frame: ", fib_gen.gi_frame)

    while True:
        print("(generator) fib_gen.gi_frame.f_locals:", fib_gen.gi_frame.f_locals)
        yield b
        a,b= b,a+b

print("caller of generator operating system thread_id:", threading.get_ident())

fib_gen = fib_generator()

print("inspect.getgeneratorstate(fib_gen):", inspect.getgeneratorstate(fib_gen))

for num in fib_gen:
    if num > 100:
        break
    print("fibonacci number:", num)

print("inspect.getgeneratorstate(fib_ben):", inspect.getgeneratorstate(fib_gen))


```

__Result:__

```
>> caller of generator operating system thread_id: 4544990656
>> inspect.getgeneratorstate(fib_gen): GEN_CREATED
>> (generator) fib_generator operating system thread_id: 4544990656
>> (generator) type(fib_gen.gi_frame): <class 'frame'> fib_gen.gi_frame:  <frame at 0x7fc04355e040, file '<string>', line 11, code fib_generator>
>> (generator) fib_gen.gi_frame.f_locals: {'a': 0, 'b': 1}
>> fibonacci number: 1
>> (generator) fib_gen.gi_frame.f_locals: {'a': 1, 'b': 1}
>> fibonacci number: 1
>> (generator) fib_gen.gi_frame.f_locals: {'a': 1, 'b': 2}
>> fibonacci number: 2
>> (generator) fib_gen.gi_frame.f_locals: {'a': 2, 'b': 3}
>> fibonacci number: 3
>> (generator) fib_gen.gi_frame.f_locals: {'a': 3, 'b': 5}
>> fibonacci number: 5
>> (generator) fib_gen.gi_frame.f_locals: {'a': 5, 'b': 8}
>> fibonacci number: 8
>> (generator) fib_gen.gi_frame.f_locals: {'a': 8, 'b': 13}
>> fibonacci number: 13
>> (generator) fib_gen.gi_frame.f_locals: {'a': 13, 'b': 21}
>> fibonacci number: 21
>> (generator) fib_gen.gi_frame.f_locals: {'a': 21, 'b': 34}
>> fibonacci number: 34
>> (generator) fib_gen.gi_frame.f_locals: {'a': 34, 'b': 55}
>> fibonacci number: 55
>> (generator) fib_gen.gi_frame.f_locals: {'a': 55, 'b': 89}
>> fibonacci number: 89
>> (generator) fib_gen.gi_frame.f_locals: {'a': 89, 'b': 144}
>> inspect.getgeneratorstate(fib_ben): GEN_SUSPENDED
```


## <a id='s1-3' />Summing it up, so far

Both iteraters and generators are means of producing a sequence of objects; iterators are an object based pattern, whereas generators are a more functional pattern.
There seems to be an analogy with decorators, these can also be object oriented, based on callbable objects vs the functional way of doing it with closures.
So that there always seem to be these two orthogonal approaches of looking at the same problem, one based on objects and the other based on closures.

To me it seems, that the object oriented way of doing things is achieving the same aims, at the expense of introducing less entities, however the functional way may be adding a slightly more succinct notation, which may be occasionally preferrable.



# <a id='s2' />AsyncIO, there is much more!

tbd
*** eof tutorial ***

