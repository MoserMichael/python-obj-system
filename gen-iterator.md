* [Generating sequences dynamically](#s1)
  * [Iterators](#s1-1)
      * [Iterator example](#s1-1-1)
        * [Iterable objects](#s1-1-1-1)
        * [Iterator objects used with for loops](#s1-1-1-2)
        * [Iterator objects that return an iterable over a range of values](#s1-1-1-3)
      * [Built-in range function, for iterating over a range of values](#s1-1-2)
  * [Generators](#s1-2)
      * [A generator in action](#s1-2-1)
      * [What is going on here?](#s1-2-2)
  * [Summing it up, so far](#s1-3)
* [AsyncIO, there is much more!](#s2)
  * [Introducing the concept of concurrent programming in Python](#s2-1)


# <a id='s1' />Generating sequences dynamically

Both iterators and generators are two ways of generating a sequence of values, in a dynamic fashion. 
There is always the possibility of creating a list, that includes all the members of a desired sequence, even if you only need the current value of the sequence. However that may take a lot of time and memory, also you may end up needing only half of the produced items, it is often much more practical to create the elements of a sequence upon demand, right when they are needed. That's exactly what is done by both iterators and generators.


__Source:__

```

# wasteful example to compute the five ten squares - get us a list of input numbers
range_list = [x for x in range(1, 6) ]        

print(range_list)

for num in range_list:
    print(f"(wasteful) the square of {num} is {num*num}")

# what you really need is just the right value from the range, upon each iteration of the loop!
for num in range(1, 6):
    print(f"(correct way) the square of {num} is {num*num}")

```

__Result:__

```
>> [1, 2, 3, 4, 5]
>> (wasteful) the square of 1 is 1
>> (wasteful) the square of 2 is 4
>> (wasteful) the square of 3 is 9
>> (wasteful) the square of 4 is 16
>> (wasteful) the square of 5 is 25
>> (correct way) the square of 1 is 1
>> (correct way) the square of 2 is 4
>> (correct way) the square of 3 is 9
>> (correct way) the square of 4 is 16
>> (correct way) the square of 5 is 25
```

Actually this is an advantage of python3 over python2; the range function used to return a full list in python2, so that the first case used occur frequently.

```
Python 2.7.16 (default, Jun  5 2020, 22:59:21)
>>> val=range(1,10)
>>> print(val)
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> print(type(val))
<type 'list'>

>>> # to be fair, you had the xrange function, this used to return an iterator object that returned the desired value upon demand.
>>> # contractors had an easier job back then, they just had to point this out to their customers, in order to achieve a wow effect. 
>>> # (nowaday you need to write a full book for that...)
>>> val=xrange(1,10)
>>> print(val)
xrange(1, 10)
>>> print(type(val))
<type 'xrange'>
```

## <a id='s1-1' />Iterators


### <a id='s1-1-1' />Iterator example


#### <a id='s1-1-1-1' />Iterable objects

An iterable object is one that returns a sequence of values. the next value of the sequence is returned by the  [\_\_next\_\_](https://docs.python.org/3/library/stdtypes.html#iterator.\_\_next\_\_) member of the iterable object, this member function is called implicitly by the built-in function [next](https://docs.python.org/3/library/functions.html#next).
The following example returns the first ten fibonacci numbers. The object of type FibIterable knows how to return the current fibonacci number, and how to prepare the value that will be returned upon the next iteration. All these values are stored as member of the iterable object.


__Source:__

```

class FibIterable:
    def __init__(self):
        self.a = 0
        self.b = 1

    def __next__(self):
        ret_val = self.b

        next_val = self.a + self.b
        self.a = self.b
        self.b = next_val

        return ret_val

fib_iter = FibIterable()

# note that we are calling next(fib_iter) exactly ten times, in order to produce ten fibonacci numbers. 
# It works, but this way of iterating is a bit awkward.
for _ in range(1,11):
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
>> 55
```


#### <a id='s1-1-1-2' />Iterator objects used with for loops

We want an iterator object that is usable with the for statement. Here we need to implement the \_\_iter\_\_ method, this is a factory method for returning an iterable object, this factory method is required by the for statement. 

In this example, the for loop first calls the \_\_iter\_\_ method of InfiniteFibSequence implicitly on the iterator object, in order to produce the iterable.
It then calls the next built-in implicitly on the iterable, and repeats this upon each cycle of the loop.

__Source:__

```

class InfiniteFibSequence:
    def __init__(self):
        pass

    def __iter__(self):
        return FibIterable()
       
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

Why do we have this distinction between iterator factories and iterable objects? One advantage is to have an independent sequence of objects for each occurence of a for loop. This distinction helps to prevents accidents that would happen, if the same iterator factory object instance is used in more than one for loop.


#### <a id='s1-1-1-3' />Iterator objects that return an iterable over a range of values

An even better example: we want an to create an iterable object, that returns a given number of fibonacci numbers, then stops the iteration, once all values have been returned.

A StopIteration exception is raised, once the last element of the sequence has been returned. I was surprised, that python is using exceptions, as part of regular control flow! But it makes sence: raising an exception is different, and can't be confused with returning a regular return value. 

As an alternative, they could have returned an additional return value, to indicate if the iteration should continue. However this would have been significant only for the last iteration cycle.



__Source:__

```

class LimitedFibIterable:
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
        return LimitedFibIterable(self.range_size)

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

The built-in [range](https://docs.python.org/3/library/functions.html#func-range) function returns an object of built-in iterator type [range](https://docs.python.org/3/library/stdtypes.html#range) - it can be used to return a consecutive sequence of numbers. The range object is actually not a generator, the range object returns an iterator, it has an \_\_iter\_\_ function that returns an iterator object.

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
>> id(range_iter): 140264668809904 id(range_iter2): 140264668810576
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

Note that built-in type [range](https://docs.python.org/3/library/stdtypes.html#range) has additional features, besides being an iterator. It has a [\_\_getitem\_\_](https://docs.python.org/3/reference/datamodel.html#object.\_\_getitem\_\_) method, this is called by python when used with a subscript syntax, in order to access an arbitrary values by its index. It implements the built-in [\_\_len\_\_](https://docs.python.org/3/reference/datamodel.html#object.\_\_len\_\_) method that returns the number of elements in the sequnce, this is called by built-in function [len](https://docs.python.org/3/library/functions.html#len), lots of goodies here.

The built-in range is also a reversible iterator, you can call the built-in [reversed](https://docs.python.org/3/library/functions.html#reversed) function to get a range o number in decreasing order

__Source:__

```


range_iter = range(1, 10)
print(type(range_iter))

reverse_range_val = reversed(range_iter)
print("type(reverse_range_val):", type(reverse_range_val))

# turn the iterator into a list object
reverse_range = [ x for x in reverse_range_val ]

print("reverse_range:", reverse_range)

```

__Result:__

```
>> <class 'range'>
>> type(reverse_range_val): <class 'range_iterator'>
>> reverse_range: [9, 8, 7, 6, 5, 4, 3, 2, 1]
```

The revesed built-in can be used with an iterator, if it does one of the following

- implements both the \_\_getitem\_\_ and \_\_len\_\_ methods
- implements a \_\_reversed\_\_ method that returns an iterable object, where the \_\_next\_\_ method returns all items in reverse order.

Now the range type has all of them, it has \_\_getitem\_\_, \_\_len\_\_ but it also has a \_\_reversed\_\_ method. I can't explain, why it is implementing both options, though one would have been sufficient

__Source:__

```

print("dir(range(1,10))", dir(range(1,10)))

```

__Result:__

```
>> dir(range(1,10)) ['__bool__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index', 'start', 'step', 'stop']
```


## <a id='s1-2' />Generators


### <a id='s1-2-1' />A generator in action

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
>> type(not_a_generator): <function not_a_generator at 0x7f91e9cdb0d0>
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

What is happening here? Both the generator function and it's caller are running as part of the same operating system thread, that is hosting the python bytecode interpreter. The interpreter is running both the generator function and its caller.

Now the python bytecode interpreter maintains two separate stack [frame object](https://docs.python.org/3/reference/datamodel.html), one for the generator function and one for its caller. The stack frame object has a field for the local variables maintained by the function (see f\_locals dictionary member of the frame object) and the current bytecode instruction that is being executed within the function/generator (see f\_lasti member of the frame object). The generator object is put into 'suspended' state, once the generator has called the yield statement, with the aim to return a value to the caller. The generator is later resumed upon calling the next built-in function (next(fib\_gen) in our case), and resumes execution from the bytecode instruction referred to by f\_lasti, with the local variable values referred to by the f\_locals dictionary of the frame object. (are you still with me?)

The interaction between the caller and generator are an example of [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative\_multitasking), here you have multiple logical threads, but there is only one of them active at a given time. When the active thread/generator has finished, it calls the yield statement, and that's where the other thread is activated, while the generator is put to sleep. Each of the cooperative threads is maintaining its own separate stack, this stack is only used when the thread is running.



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
>> caller of generator operating system thread_id: 4482489792
>> inspect.getgeneratorstate(fib_gen): GEN_CREATED
>> (generator) fib_generator operating system thread_id: 4482489792
>> (generator) type(fib_gen.gi_frame): <class 'frame'> fib_gen.gi_frame:  <frame at 0x7f91e9b7b9a0, file '<string>', line 10, code fib_generator>
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

This is a very large API, and it has undergone many changes since it was introduced. I probably will not be able to present the whole asyncio api here, instead i will focus on a few of the more interesting use cases. 

AsyncIO is a feature, that has reached a more or less mature state, beginning with python 3.7, so let us therefore check, that we are runnng on the correct python interpreter.



__Source:__

```

import sys

major_python_version = sys.version_info[0]
minor_python_version = sys.version_info[1] 

assert (major_python_version == 3 and minor_python_version >=7) or (major_python_version > 3)
print("This python interpreter supports asyncio")

```

__Result:__

```
>> This python interpreter supports asyncio
```


## <a id='s2-1' />Introducing the concept of concurrent programming in Python

AsyncIO is a generalization of the generator feature, with generators the flow of control is strictly switching back and forth, between the caller and the generator function, AsyncIo is much more flexible in that respect.

A short overview of the main AsyncIO concepts:
- Each asyncIO task object stands for a concurrent task, each task is either suspended or currently running. Each task object has its own coroutine function, a coroutine is a regular python function that has an additional async keyword standing right before the def keyword. If a task object is in running state, then its coroutine function is running. More [here](https://docs.python.org/3/library/asyncio-task.html)
- An event loop is hosting a set of task object. One single task is running at any given moment. All the other task objects are in suspended state, while that task is running. The event loop is running behind the scene, most of the action is dealing implicitly with this entity.
- The currently running task stops running, when it is either waiting for the completion of networking IO, waiting for the [completion of another concurrent task](https://docs.python.org/3/library/asyncio-task.html#waiting-primitives) or when the running task has called the [asyncio sleep api](https://docs.python.org/3/library/asyncio-task.html#sleeping). If any one of these events happened, then the event loop is picking another currently suspended task, and running it instead of the currently running task.
- [Streams](https://docs.python.org/3/library/asyncio-stream.html) are special wrappers for network connections. The purpose here is to deactivate the currently running task when a network request cant be completed immediately, and the currently active task would otherwise have to wait for the completion of the network request.

The main use case for all of this is a program, that is doing networking and multiplexing between several network connections, this is a paradigm, that comes from the world of Unix system programming in C. Concurrent networking in the C programming language is handled by a loop, that is calling any one of following system calls on each iteration of the loop - [select](https://www.man7.org/linux/man-pages/man2/select.2.html)/[poll](https://www.man7.org/linux/man-pages/man2/poll.2.html)/[epoll](https://man7.org/linux/man-pages/man7/epoll.7.html), this system call is waiting on a set of socket file descriptors. The system call returns, when an event of interest happened on a subset of the socket file descriptors that were passed to the select/poll/epoll call. The event loop will then have to react on this event, which may be either one of the following: a new socket connection has been established and you can get it by calling the [accept](https://www.man7.org/linux/man-pages/man2/accept.2.html) system call on a listening socket, data that is available to be [received](https://www.man7.org/linux/man-pages/man2/recv.2.html) over a socket, a [send](https://www.man7.org/linux/man-pages/man2/send.2.html) system call has previously blocked, the data has been sent, and the socket is now ready for action, the peer has closed a connection, or an error occured. A C program like this will often be implemented as a very long loop, where all of the network connections are handled by a complex state machine, reacting to any of the events that could occur on ony one of the handled socket descriptors.

The Python AsyncIO api is designed to write a program like this in a much more pleasent style. A set of logically related socket descriptors will be handled by a single coroutine/async IO task. The logic for handling all this will be local to the coroutine function, this is a very big improvement over the approach described in the previous paragraph.

*** eof tutorial ***

