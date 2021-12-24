#!/usr/bin/env python3

from mdformat import *

header_md("Generating sequences dynamically", nesting=1)

print_md("""Both iterators and generators are two ways of generating a sequence of values, in a dynamic fashion. 
There is always the possibility of creating a list, that includes all the members of a desired sequence, even if you only need the current value of the sequence. However that may take a lot of time and memory, also you may end up needing only half of the produced items, it is often much more practical to create the elements of a sequence upon demand, right when they are needed. That's exactly what is done by both iterators and generators.
""")

eval_and_quote("""
# wasteful example to compute the five ten squares - get us a list of input numbers
range_list = [x for x in range(1, 6) ]        

print(range_list)

for num in range_list:
    print(f"(wasteful) the square of {num} is {num*num}")

# what you really need is just the right value from the range, upon each iteration of the loop!
for num in range(1, 6):
    print(f"(correct way) the square of {num} is {num*num}")
""")

print_md("""Actually this is an advantage of python3 over python2; the range function used to return a full list in python2, so that the first case used occur frequently.""")

print("""```
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
```""")

header_md("Iterators", nesting=2)

header_md("Iterator example", nesting=3)

header_md("Iterable objects", nesting=4)

print_md("""An iterable object is one that returns a sequence of values. the next value of the sequence is returned by the  [__next__](https://docs.python.org/3/library/stdtypes.html#iterator.__next__) member of the iterable object, this member function is called implicitly by the built-in function [next](https://docs.python.org/3/library/functions.html#next).
The following example returns the first ten fibonacci numbers. The object of type FibIterable knows how to return the current fibonacci number, and how to prepare the value that will be returned upon the next iteration. All these values are stored as member of the iterable object.
""")

eval_and_quote("""
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
""") 

header_md("Iterator objects used with for loops", nesting=4)

print_md("""We want an iterator object that is usable with the for statement. Here we need to implement the __iter__ method, this is a factory method for returning an iterable object, this factory method is required by the for statement. 

In this example, the for loop first calls the __iter__ method of InfiniteFibSequence implicitly on the iterator object, in order to produce the iterable.
It then calls the next built-in implicitly on the iterable, and repeats this upon each cycle of the loop.""")

eval_and_quote("""
class InfiniteFibSequence:
    def __init__(self):
        pass

    def __iter__(self):
        return FibIterable()
       
for num in InfiniteFibSequence():
    if num > 100:
        break
    print("fibonacci number:", num)
""")

print_md("""Why do we have this distinction between iterator factories and iterable objects? One advantage is to have an independent sequence of objects for each occurence of a for loop. This distinction helps to prevents accidents that would happen, if the same iterator factory object instance is used in more than one for loop.
""")        

header_md("Iterator objects that return an iterable over a range of values", nesting=4)

print_md("""An even better example: we want an to create an iterable object, that returns a given number of fibonacci numbers, then stops the iteration, once all values have been returned.

A StopIteration exception is raised, once the last element of the sequence has been returned. I was surprised, that python is using exceptions, as part of regular control flow! But it makes sence: raising an exception is different, and can't be confused with returning a regular return value. 

As an alternative, they could have returned an additional return value, to indicate if the iteration should continue. However this would have been significant only for the last iteration cycle.

""")

eval_and_quote("""
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
""")
 
header_md("Built-in range function, for iterating over a range of values", nesting=3)

print_md("""The built-in [range](https://docs.python.org/3/library/functions.html#func-range) function returns an object of built-in iterator type [range](https://docs.python.org/3/library/stdtypes.html#range) - it can be used to return a consecutive sequence of numbers. The range object is actually not a generator, the range object returns an iterator, it has an __iter__ function that returns an iterator object.""")


eval_and_quote("""
range_value = range(1,10)
print("type(range_value):", type(range_value))
assert not inspect.isgenerator(range_value)
print("dir(range_value):", dir(range_value))
""")

print_md("""The [inspect module](https://docs.python.org/3/library/inspect.html) actually does not have a function that checks, if an object is an iterator, one would look as follows:""")

eval_and_quote('''
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
''')
        

print_md("""Each call to the __iter__() member of the range type will return a distinct value of type range_iterator, here the __next__ member is implemented. """)

eval_and_quote("""
range_iter = range_value.__iter__()
print("type(range_iter):", type(range_iter))
print("dir(range_iter):", dir(range_iter))
assert not inspect.isgenerator(range_iter)

range_iter2 = range_value.__iter__()
print("id(range_iter):", id(range_iter), "id(range_iter2):", id(range_iter2))
assert id(range_iter) != id(range_iter2)
""")

print_md("""Returning a separate range_iter object on each call to __iter__ makes sense:
You can use the same range object in different for loops, each time an independent sequence of values is returned!""")

eval_and_quote("""
range_val = range(1,3)
for val in range_val:
    print("iteration1:", val)
for val in range_val:
    print("iteration2:", val)
""")

print_md("""Note that built-in type [range](https://docs.python.org/3/library/stdtypes.html#range) has additional features, besides being an iterator. It has a [__getitem__](https://docs.python.org/3/reference/datamodel.html#object.__getitem__) method, this is called by python when used with a subscript syntax, in order to access an arbitrary values by its index. It implements the built-in [__len__](https://docs.python.org/3/reference/datamodel.html#object.__len__) method that returns the number of elements in the sequnce, this is called by built-in function [len](https://docs.python.org/3/library/functions.html#len), lots of goodies here.
""")

print_md("""The built-in range is also a reversible iterator, you can call the built-in [reversed](https://docs.python.org/3/library/functions.html#reversed) function to get a range o number in decreasing order""")

eval_and_quote("""

range_iter = range(1, 10)
print(type(range_iter))

reverse_range_val = reversed(range_iter)
print("type(reverse_range_val):", type(reverse_range_val))

# turn the iterator into a list object
reverse_range = [ x for x in reverse_range_val ]

print("reverse_range:", reverse_range)
""")

print_md("""The revesed built-in can be used with an iterator, if it does one of the following

- implements both the __getitem__ and __len__ methods
- implements a __reversed__ method that returns an iterable object, where the __next__ method returns all items in reverse order.

Now the range type has all of them, it has __getitem__, __len__ but it also has a __reversed__ method. I can't explain, why it is implementing both options, though one would have been sufficient""")

eval_and_quote("""
print("dir(range(1,10))", dir(range(1,10)))
""")

header_md("Generators", nesting=2)

header_md("A generator in action", nesting=3)

print_md("""Let's examine how generator functions differ from regular functions. Calling a regular function, will execute the statements of the function, and return the return value of the function""")

eval_and_quote("""
def not_a_generator(from_val, to_val):
    return from_val + to_val

print("type(not_a_generator):", not_a_generator)

no_gen_ret_val = not_a_generator(10, 20)
print("type(no_gen_ret_val):", type(no_gen_ret_val))
""")

print_md("""Let's look at a generator function, it has a yield statement in its body""")

eval_and_quote("""
def my_range(from_val, to_val):
    print("(generator) my_range from_val:", from_val, "to_val:", to_val)

    while from_val < to_val:

        print("(generator) The generator instance is in running state, computes the next value to be returned by the yield statement")
        print("(generator) inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))

        print("(generator) before yield from_val:", from_val)
        yield from_val
        from_val += 1

    print("(generator) leaving the generator function, iteration is finished")
""")

print_md("""A function that has a yield statement, is is technically still a function objct.""")
eval_and_quote("""
print("type(my_range):", type(my_range))
""")

print_md("""You can tell, if a function has a yield statement, or not, the function object owns a __code__ attribute, which has a flag set, if it includes a yield statment, that's what [inspect.isgeneratorfunction](https://docs.python.org/3/library/inspect.html#inspect.isgeneratorfunction) is checking.""")

eval_and_quote("""
import inspect

assert inspect.isgeneratorfunction(my_range)
assert not inspect.isgeneratorfunction(not_a_generator)
""")

print_md("""Digression: the __code__ attribute of a function object stands for the compiled byte code of a function. (but that's another rabbit hole)""")

eval_and_quote("""
print("type(my_range.__code__):", type(my_range.__code__))
print("dir(my_range.__code__):", dir(my_range.__code__))
""")

print_md("""Attention! Calling the generator function does not execute any of the statements in the body of the function! (you won't see the print at the start of my_range), instead it returns a generator object. """)

eval_and_quote("""
print("calling: my_range(10,20)")
range_generator = my_range(10,12)
print("type(range_generator):", type(range_generator))
""")

print_md("The generator has not been invoked yet, it is in created state")
eval_and_quote("""
print("inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))
""")

print_md("""Let's examine the generator object. Generators are iterators, they have the special __iter__ and __next__ attribute. Additional special attributes of generator objects: 'close', 'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom', 'send', 'throw' """)

# generator are built-in objects that do not do not have a __dict__ member
# print("range_generator.__dict__ :", range_generator.__dict__)
# but dir built-in will show its attributes

eval_and_quote("""
print("dir(range_generator):", dir(range_generator))
print("dir(type(range_generator):", dir(type(range_generator)))
""")

print_md("Using the generator as an iterator: calling next(range_generator)...")

eval_and_quote("""
val = next(range_generator)
print("return value of next(range_generator):", val)
""")

print_md("""The generator is in suspended state, after having returned it's value via the yield statement""")

eval_and_quote("""
print("inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))
""")

print_md("Calling built-in next(range_generator) is the same as calling range_generator.__next__() ...")
eval_and_quote("""
val = range_generator.__next__()
print("return value of next(range_generator):", val)
""")

print_md("""When the generator function is exiting: a StopIteration exception is raised. I was surprised, that python is using exceptions, as part of regular control flow!
But it makes sence: raising an exception is different, and can't be confused with returning a regular return value""")

eval_and_quote("""
has_stop_iter_ex = False
try:
    val = range_generator.__next__()
except StopIteration as stop_iter:
    print("Upon leaving the generator function, received exception of type(stop_iter):", type(stop_iter))
    has_stop_iter_ex = True

assert has_stop_iter_ex
""")

print_md("""The gnerator object is in closed state, upon having completed its iteration""")

eval_and_quote("""
print("inspect.getgeneratorstate(range_generator):", inspect.getgeneratorstate(range_generator))
""")

print_md("""Using an generator in a for loop, The for loop uses it as an iterator""")

eval_and_quote("""
range_generator = my_range(0,7)
for num in range_generator:
    print("num:", num)
""")

header_md("What is going on here?", nesting=3)

print_md("""What is happening here? Both the generator function and it's caller are running as part of the same operating system thread, that is hosting the python bytecode interpreter. The interpreter is running both the generator function and its caller.

Now the python bytecode interpreter maintains two separate stack [frame object](https://docs.python.org/3/reference/datamodel.html), one for the generator function and one for its caller. The stack frame object has a field for the local variables maintained by the function (see f_locals dictionary member of the frame object) and the current bytecode instruction that is being executed within the function/generator (see f_lasti member of the frame object). The generator object is put into 'suspended' state, once the generator has called the yield statement, with the aim to return a value to the caller. The generator is later resumed upon calling the next built-in function (next(fib_gen) in our case), and resumes execution from the bytecode instruction referred to by f_lasti, with the local variable values referred to by the f_locals dictionary of the frame object. (are you still with me?)

The interaction between the caller and generator are an example of [cooperative multitasking](https://en.wikipedia.org/wiki/Cooperative_multitasking), here you have multiple logical threads, but there is only one of them active at a given time. When the active thread/generator has finished, it calls the yield statement, and that's where the other thread is activated, while the generator is put to sleep. Each of the cooperative threads is maintaining its own separate stack, this stack is only used when the thread is running.

""")



eval_and_quote("""
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
""")

header_md("Summing it up, so far", nesting=2)

print_md("""
Both iteraters and generators are means of producing a sequence of objects; iterators are an object based pattern, whereas generators are a more functional pattern.
There seems to be an analogy with decorators, these can also be object oriented, based on callbable objects vs the functional way of doing it with closures.
So that there always seem to be these two orthogonal approaches of looking at the same problem, one based on objects and the other based on closures.

To me it seems, that the object oriented way of doing things is achieving the same aims, at the expense of introducing less entities, however the functional way may be adding a slightly more succinct notation, which may be occasionally preferrable.

""")

header_md("AsyncIO, there is much more!", nesting=1)

print_md("""
This is a very large API, and it has undergone many changes since it was introduced. I probably will not be able to present the whole asyncio api here, instead i will focus on a few of the more interesting use cases. 

AsyncIO is a feature, that has reached a more or less mature state, beginning with python 3.7, so let us therefore check, that we are runnng on the correct python interpreter.

""")

eval_and_quote("""
import sys

major_python_version = sys.version_info[0]
minor_python_version = sys.version_info[1] 

assert (major_python_version == 3 and minor_python_version >=7) or (major_python_version > 3)
print("This python interpreter supports asyncio")
""")

header_md("Introducing the concept of concurrent programming in Python", nesting=2)

print_md("""

AsyncIO is a generalization of the generator feature, with generators the flow of control is strictly switching back and forth, between the caller and the generator function, AsyncIo is much more flexible in that respect.

A short overview of the main AsyncIO concepts:
- Each asyncIO task object stands for a concurrent task, each task is either suspended or currently running. Each task object has its own coroutine function, a coroutine is a regular python function that has an additional async keyword standing right before the def keyword. If a task object is in running state, then its coroutine function is running.
- An event loop is hosting a set of task object. One single task is running at any given moment. All the other task objects are in suspended state, while that task is running.
- The currently running task stops running, when it is either waiting for the completion of networking IO, waiting for the completion of another concurrent task or calling the asyncio sleep api. If any one of these events happened, then the event loop is picking another currently suspended task, and running it instead of the prviously currently running task.

The main use case for all of this is a program, that is doing networking and multiplexing between several network connections, this is a paradigm, that comes from the world of Unix system programming in C. Concurrent networking in the C programming language is handled by a loop, that is calling any one of following system calls on each iteration of the loop - [select](https://www.man7.org/linux/man-pages/man2/select.2.html)/[poll](https://www.man7.org/linux/man-pages/man2/poll.2.html)/[epoll](https://man7.org/linux/man-pages/man7/epoll.7.html), this system call is waiting on a set of socket file descriptors. The system call returns, when an event of interest happened on a subset of the socket file descriptors that were passed to the select/poll/epoll call. The event loop will then have to react on this event, which may be either one of the following: a new socket connection has been established and you can get it by calling the [accept](https://www.man7.org/linux/man-pages/man2/accept.2.html) system call on a listening socket, data that is available to be [received](https://www.man7.org/linux/man-pages/man2/recv.2.html) over a socket, a [send](https://www.man7.org/linux/man-pages/man2/send.2.html) system call has previously blocked, the data has been sent, and the socket is now ready for action, etc. A C program like this will often be implemented as a very long loop, where all of the network connections are handled by a complex state machine, reacting to any of the possible events that occur on ony one of the handled socket descriptors.

The Python AsyncIO api is designed to write a program like this in a much more pleasent style. A set of logically related socket descriptors will be handled by a single coroutine/async IO task. The logic for handling all this will be local to the coroutine function, this is a very big improvement over the approach described in the previous section.
""")


print("*** eof tutorial ***")



