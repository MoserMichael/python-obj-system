#!/usr/bin/env python3

from mdformat import *


header_md("Iterators", nesting=2)

header_md("Generators", nesting=2)

header_md("a generator in action", nesting=3)

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

header_md("stop, what is cooperative threading all about?", nesting=3)

print_md("""What is happening here? Both the generator function and it's caller are running as part of the same operating system thread, this thread is hosting the python bytecode interpeter, which is executing both the generator function and its caller.

        
Now the python bytecode interpreter maintains two separate stack frame entity, one for the generator and one for its caller, A stack [frame object](https://docs.python.org/3/reference/datamodel.html) represents the current function or generator in the python bytecode interpreter. It has a field for the local variables maintained by the function (see f_locals dictionary member of the frame object) and the current bytecode instruction that is being executed within the function/generator (see f_lasti member of the frame object). The generator object is put into 'suspended' state, once the generator has called the yield statement, with the aim to return a value to the caller. The generator is later resumed upon calling the next built-in function (next(fib_gen) in our case), and resumes execution from the bytecode instruction referred to by f_lasti, with the local variable values referred to by the f_locals dictionary of the frame object. (are you still with me?)


See the following example:
""")



eval_and_quote("""

import traceback
import threading

def fib_generator():
    a=0
    b=1

    print("(generator) fib_generator operating system thread_id:", threading.get_ident())

    while True:
        print("(generator) type(fib_gen.gi_frame):", type(fib_gen.gi_frame), "fib_gen.gi_frame: ", fib_gen.gi_frame, "fib_gen.gi_frame.f_locals:", fib_gen.gi_frame.f_locals) 
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

header_md("built-in range function, for iterating over a range of values", nesting=2)

print_md("""built in range function returns an object of built-in type range, the range object is not a generator, the range object returns an iterator, it has an __iter__ function that returns an iterator object.""")


eval_and_quote("""
range_value = range(1,10)
print("type(range_value):", type(range_value))
assert not inspect.isgenerator(range_value)
print("dir(range_value):", dir(range_value))
""")

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

print("*** eof tutorial ***")

