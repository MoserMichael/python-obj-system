#!/usr/bin/env python3
from mdformat import *
import pprintex


header_md("""Python object primer for Python3 / meta classes""" )

header_md("""Introduction""",  nesting = 2)

print_md("""
Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta classes](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system. The purpose of this text is to figure out, how the python object system ticks.
""")

header_md("""The Python object system""", nesting=2)

header_md("""How objects are represented""", nesting=3)

print_md("""

Lets look at a simple python class Foo with a single base class Base, and see how objects are created and represented in memory
""")

eval_and_quote("""

# The base class. All Python3 classes have the base class of type object.
# The long form is therefore
#   class Base(object):
# However Pylint will tell you, that this long form is redundant


class Base:

    # Class variables are shared between all instances of the class Base, and declared like this:
    base_class_var = "Base"

    # The object constructor/init method, Note the first 'self' argument, which refers to the object instance.
    def __init__(self):
        print("calling Base.__init__")
        # Object variables are specific to a given instance of Base
        # Each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)
        self.obj_var_base = 10

    # An object method - needs to access the object instance, which is passed as first 'self' argument.
    def show_base(self):
        print_md("obj_var_base: ", self.obj_var_base)

    # A class method/static method is called without an object instance.
    @staticmethod
    def make_base():
        return Base()

# class Foo with a base class Base
class Foo(Base):

    # Class variables are shared between all instances of the class Foo, and declared like this:
    class_var = 42
    class_var2 = 43

    # The object constructor/init method, Note the first 'self' argument, which is the object instance.
    def __init__(self):
        # When not calling the base class __init__ method: the base class object variables are not added  to the object !!!
        # The base class __init__ adds the 'obj_var_base' member to the __dict__ member of this object instance.
        # By convention: you first init the base classes, before initialising the derived class.
        super().__init__()

        print("calling Foo.__init__")

        # Object variables are specific to a given instance of Foo
        # Each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)

        # Define object variable: obj_var_a
        self.obj_var_a=42

        # Define object variable: obj_var_b
        self.obj_var_b="name"

    # An object method - needs to access the object instance, which is passed as first 'self' argument.
    def show_derived(self):
        print_md("obj_var_a:", self.obj_var_a, "obj_var_b:", self.obj_var_b)

    # A class method/static method is called without an object instance.
    @staticmethod
    def make_foo():
        return Foo()

# Make a new object instance of type Foo class.
foo_obj=Foo()

""")

print_md("The memory address of object foo_obj is returned by the [id built-in](https://docs.python.org/3/library/functions.html#id)")

eval_and_quote('print("id(foo_obj) : ", id(foo_obj))')

print_md("If two variables have the same object id value, then they both refer to the very same object/instance!")

print_md("""
Each user defined object has a __dict__ attribute, this is a dictionary that lists all the object instance variables.
This also includes instance members that were added by the __init__ method of the base class !!
""")

eval_and_quote("""print("foo_obj.__dict__ : ", foo_obj.__dict__)""")


print_md("""
So you see that the following is exactly the same thing:
""")

eval_and_quote("""assert id(foo_obj.obj_var_a) == id( foo_obj.__dict__['obj_var_a'] ) """)

print_md("""
Wait, but where does the __dict__ attribute come from?
The [built-in getattr](https://docs.python.org/3/library/functions.html#getattr) function can return this built-in __dict__ attribute!
Interesting: the python notation object.member_name can mean different things:
  1) for built-in attributes it means a call to getattr
  2) for object instances (assigned in the __init__ method of the class) it means a call to retrieve the __dict__ attribute, and then a lookup of the variable name in that dictionary.
""")

print_md( """foo_obj.__dict__ and getattr(foo_obj,'__dict__',None) is the same thing! """)

eval_and_quote("""assert id(foo_obj.__dict__) == id( getattr(foo_obj,'__dict__',None) )""")

print_md("""
The getattr builtin function has a good part, its return value can be checked for None. This can be used, in order to check if the argument is an object with a __dict__ attribute.
""")

eval_and_quote("""base_obj = object()""")

print_md("An object of built-in type ", type(base_obj), " doesn't have a __dict__ member")
eval_and_quote("""assert getattr(base_obj, '__dict__', None) is None""")

eval_and_quote("""int_obj = 42""")

print_md("An object of built-in type ", type(int_obj), " doesn't have a __dict__ member")

eval_and_quote("""assert getattr(int_obj, '__dict__', None) is None""")

print_md("""
The [dir builtin](https://docs.python.org/3/library/functions.html#dir) function does different things, depending on the argument,
for regular objects it returns a  "list that contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes.",
all this is sorted alphabetically.
""")

eval_and_quote("""print("dir(foo_obj) : ", dir(foo_obj))""")

# doesn't have __slots__, how odd.
#print_md("foo_obj.__slots__ : ", foo_obj.__slots__)

header_md("""How classes are represented""", nesting=3)

print_md("""The built-in function [type](https://docs.python.org/3/library/functions.html#type), is returning the class of an object, when applied to a variable (to be more exact: type is a built-in class, and not a built-in function, more on that later)""")

eval_and_quote("""
# Make a new object instance of type Foo class.
foo_obj=Foo()

print("class of object foo_obj - type(foo_obj): ", type(foo_obj))

# That's the same as showing the __class__ member of the variable (in Python3)
print("foo_obj.__class__ :", foo_obj.__class__)
""")

print_md("""
The class is an object, it's purpose is to hold the static data that is shared between all object instances.

Each object has a built-in __class__ attribute, that refers to this class object.

Note that the name of the class includes the module name, __main__ if the class is defined in the file given as argument to the python interpreter.
Also note that the type built-in of type(foo_obj) is really the same as: str(foo_obj.__class__) (for Python3)
""")

print_md("""
Again, the built in attribute __class__ can also be accessed with the getattr built-in function.
""")

eval_and_quote( """
print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!")
assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) )
""")

print_md("""The __name__ and __qualname__ built-in attributes return the name of the class, without the module name """)

eval_and_quote( """
print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)""" )


print_md("""
To get the immediate base class list as declared in that particular class.
""")

eval_and_quote( """print("foo_obj.__class__.__bases__ :", foo_obj.__class__.__bases__)""")


print_md("""
The __mro__ member is a list of types that stands for 'method resoultion order', when searching for an instance method, this list is searched in order to resolve the method name.
The Python runtime creates this lists by enumerating all of its base classes recursively, in depth first traversal order. For each class it follows the base classes, from the left ot the right

This list is used to resolve a member function 'member_function' of an object, when you call it via: obj_ref.member_function()
""")

eval_and_quote( """print("foo_obj.__class__.__mro__ :", foo_obj.__class__.__mro__) """ )

print_md("Computing the method resolution order by hand")

eval_and_quote("""

# function to a class hierarchy, in depth first search order (like what you get in MRO - method resolution order)
def show_type_hierarchy(type_class):

    def show_type_hierarchy_imp(type_class, nesting):
        if  len(type_class.__bases__) == 0:
            return

        prefix = "\t" * nesting
        print( prefix + "type:", type_class.__name__ , "base types:", ",".join( map( lambda ty : ty.__name__, type_class.__bases__) ) )
        #print( prefix + "str(",  type_class.__name__ , ").__dict__ : ",  type_class.__dict__ )
        for base in type_class.__bases__:
            show_type_hierarchy_imp(base, nesting+1)

    if not inspect.isclass(type_class):
        print("object ", str(type_class), " is not class")
        return

    print("show type hierarchy of class:")
    show_type_hierarchy_imp(type_class, 0)

class LevelOneFirst:
    pass

class LevelOneSecond:
    pass

class LevelOneThird:
    pass

class LevelTwoFirst(LevelOneFirst, LevelOneSecond):
    pass

class LevelThree(LevelTwoFirst,LevelOneThird):
    pass

show_type_hierarchy(LevelThree)

print("LevelThree.__mro__:", LevelThree.__mro__)
""")

eval_and_quote("""
print("*** mro in detail:")
for cls in foo_obj.__class__.__mro__:
    print_md("\tclass-in-mro: ", str(cls), "id:", id(cls), "cls.__dict__: ", cls.__dict__)
print("*** eof mro in detail")
""")

print_md("""
The class object has a __dict__ too - here you will see all the class variables (for Foo these are class_var and class_var2) and class methods (defined with @staticmethod), but also the object methods (with the self parameter)
""")


eval_and_quote( """print("foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)""" )

# doen't have slots, how odd.
#print_md("foo_obj.__class__.__slots__ : ", foo_obj.__class__.__slots__)

print_md("""
Again, the [dir](https://docs.python.org/3/library/functions.html#dir) built-in function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
That means it displays both the names of static variables, and the names of the static functions, for the class and it's base classes.
Note that the names are sorted.
""")


eval_and_quote("""print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )""")

print_md("""
The class object derives from built-in class type, you can check if an object is a class by checking if it is an instance of class 'type'!
""")

# check that foo_obj.__class__ is a type - it is derived from built-in class type
eval_and_quote("""
assert isinstance(foo_obj.__class__, type)
# same thing as
assert inspect.isclass(foo_obj.__class__)

# an object is not derived from class type.
assert not isinstance(foo_obj, type)
# same thng as 
assert not inspect.isclass(foo_obj)
""")

print_md( """
Now there is much more: there is the inspect module that returns it all, a kind of rosetta stone of the python object model.
inspect.getmembers returns everything! You can see the source of inspect.getmembers [here](https://github.com/python/cpython/blob/3.10/Lib/inspect.py)
""")

eval_and_quote("""print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))""")


print_md("""
Attention!
the type of the object is the class of the object (remember: the classes is an object, where the __dict__ member holds the class variables)
""")

eval_and_quote("""
print("type(foo_obj) : ", type(foo_obj))
# same thing in python3
print("str(foo_obj.__class__) : ", str(foo_obj.__class__) )""")

print_md("""

Let's look at both the type and identity of all these objects:

""")

eval_and_quote("""print("id(foo_obj) : ", id(foo_obj), " str(foo_obj) : ", str(foo_obj))""")

print_md("""
The following expressions refer to the same thing: the type of the object foo_obj, also known as the class of foo_obj
""")

eval_and_quote("""
print("type(foo_obj)            :", type(foo_obj), " id(type(foo_obj))             :", id(type(foo_obj)), " type(foo_obj).__name__ : ", type(foo_obj).__name__ )
print("str(foo_obj.__class__)   :", str(foo_obj.__class__), " id(foo_obj.__class__)         :", id(foo_obj.__class__), "foo_obj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("str(Foo)                 :", str(Foo), " id(Foo)                       :", id( Foo ), "Foo.__name__ :", Foo.__name__)

assert id(Foo) == id(type(foo_obj))
assert id(type(foo_obj)) == id(foo_obj.__class__)
""")

print_md("""
    The Foo class members
""")

eval_and_quote("""
print("foo_obj.__class__.__dict__   :", foo_obj.__class__.__dict__)
print("Foo.__dict__                 :", Foo.__dict__)
# everything accessible form the class
print("dir(foo_obj.__class__)       :", dir( foo_obj.__class__))
""")


print_md("""
The following expressions refer to the same thing: the meta-type of the foo_obj.
""")


eval_and_quote("""
print("type(foo_obj.__class__.__class__):", type(foo_obj.__class__.__class__), " id( foo_obj.__class__.__class__ ) :" , id( foo_obj.__class__.__class__ ) , "foo_obj.__class__.__class__.__name__ : ", foo_obj.__class__.__class__.__name__ )
print("type(Foo)                        :", type(Foo), " id(type(Foo)) : ", id( type( Foo ) ), " Foo.__class__.__name__ :", Foo.__class__.__name__)
print("type(Foo.__class__)              :", type(Foo.__class__), " id(type(Foo.__class__)) : ", id( type( Foo.__class__ ) ), " Foo.__class__.__name__ :", Foo.__class__.__name__)
print("type(Foo.__class__.__class__)    :", type(Foo.__class__.__class__), " id(type(Foo.__class__.__class__)) :", id( type( Foo.__class__.__class__ ) ) )

assert type(Foo) == type(Foo.__class__)
assert type(Foo.__class__) == type(Foo.__class__.__class__)
""")


print_md("""
The type of the type is the metaclass - the metaclass constructs the Class object! (the class of an object is also an object!)
""")

eval_and_quote("""
print("type( type( foo_obj ) )              :", type( type( foo_obj ) ) )
print("str( foo_obj.__class__.__class__ )   :", str(foo_obj.__class__.__class__) )
""")


# result:

eval_and_quote("""
print(" metaclass members: foo_obj.__class__.__class__.__dict__ : ", foo_obj.__class__.__class__.__dict__)
print(" everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) : ", dir( foo_obj.__class__.__class__) )
""")

print_md("""
Wow, any class can tell all of its derived classes! I wonder how that works...
""")

eval_and_quote("""print("Base.__subclasses__() : ", Base.__subclasses__())""")


header_md("""Object creation""", nesting=3)

print_md("""

Objects recap:
    The object instance holds the __dict__ attribute of the object instance, it's value is a dictionary that holds the object instance members.
    The class is an object that is shared between all object instances, and it holds the static data (class variables, class methods)

What happens upon: foo = Foo() ?

Take the type of Foo - the metaclass of Foo, the metaclass both knows how to create an instance of the class Foo, and the object instances.
A metaclass is derived from built-in class 'type', The 'type' constructor with three argument creates a new class object. [see reference](https://docs.python.org/3/library/functions.html#type)

    class_obj = Foo

The metaclass is used as a 'callable' - it has a __call__ method, and can therefore be called as if it were a function (see more about callables in the course on [decorators](https://github.com/MoserMichael/python-obj-system/blob/master/decorator.md))

Now this __call__ method creates and initialises the object instance.
The implementation of __call__ now does two steps:
   - Class creation is done in the [__new__](https://docs.python.org/3/reference/datamodel.html#object.__new__) method of the metaclass.  The __new__ method creates the Foo class, it is called exactly once, upon class declaration (you will see this shortly, in the section on custom meta classes)
   - It uses the Foo class and calls its to create and initialise the object (call the __new__ method of the Foo class, in order to create an instance of Foo, then calls the __init__ instance method of the Foo class, on order to initialise it). This all done by the __call__ method of the metaclass.
     instance_of_foo = meta_class_obj.__call__()

(actually that was a bit of a simplification...
)
""")
eval_and_quote("""
# same as: foo_obj = Foo()
foo_obj = Foo.__call__()

print("foo_obj : ", foo_obj)
print("foo_obj.__dict__ : ", foo_obj.__dict__)
""")

print_md("This is the same as:")

eval_and_quote("""
class_obj = Foo
instance_of_foo = class_obj()

print("instance_of_foo : ", instance_of_foo)
print("instance_of_foo.__dict__ : ", instance_of_foo.__dict__)
""")

header_md("""Custom metaclasses""",  nesting = 2)

header_md("""Metaclasses for implementing singleton objects""",  nesting = 3)

print_md("""
An object can define a different way of creating itself, it can define a custom metaclass, which will do exactly the same object creation steps described in the last section.

Let's examine a custom metaclass for creating singleton objects.
""")


eval_and_quote("""

# metaclass are always derived from the type class. 
# the type class has functions to create class objects
# the type class has also a default implementation of the __call__ method, for creating object instances.
class Singleton_metaclass(type):

    # invoked to create the class object instance (for holding static data)
    # this function is called exactly once, in order to create the class instance!
    def __new__(meta_class, name, bases, cls_dict, **kwargs):

        print("Singleton_metaclass: __new__ meta_class:", meta_class, "name:", name, "bases:", bases, "cls_dict:", cls_dict, f'kwargs: {kwargs}')

        class_instance = super().__new__(meta_class, name, bases, cls_dict)
        print("Singleton_metaclass: __new__ return value: ", class_instance, "type(class_instance):", type(class_instance))

        # the class class variable __singleton_instance__ will hold a reference to the one an only object instance of this class.
        class_instance.__singleton_instance__ = None

        return class_instance
 
    def __call__(cls, *args, **kwargs):
        # we get here to create an object instance. the class object has already been created.
        print("Singleton_metaclass: __call__ args:", *args, f'kwargs: {kwargs}')

        # check if the singleton has already been created.
        if cls.__singleton_instance__ is None:

            # create the one an only instance object.
            instance = cls.__new__(cls)

            # initialise the one and only instance object
            instance.__init__(*args, **kwargs)

            # store the singleton instance object in the class variable __singleton_instance__
            cls.__singleton_instance__ = instance

        # return the singleton instance
        return cls.__singleton_instance__
        
 
import math
 
# the metaclass specifier tells python to use the Singleton_metaclass, for the creation of an instance of type SquareRootOfTwo
class SquareRootOfTwo(metaclass=Singleton_metaclass):
    
    # the __init__ method is called exactly once, when the first instance of the singleton is created.
    # the square root of two is computed exactly once.
    def __init__(self):
        self.value = math.sqrt(2)
        print("SquareRootOfTwo.__init__  self:", self)
 
print("creating the objects instances...")

sqrt_root_two_a = SquareRootOfTwo()
print("sqrt_two_a id(sqrt_root_two_a):", id(sqrt_root_two_a), "type(sqrt_root_two_a):", type(sqrt_root_two_a), "sqrt_root_two_a.value:", sqrt_root_two_a.value)

sqrt_root_two_b = SquareRootOfTwo()

print("sqrt_two_b id(sqrt_root_two_b)", id(sqrt_root_two_b), "type(sqrt_root_two_b):", type(sqrt_root_two_b), "sqrt_root_two_b.value:", sqrt_root_two_b.value)

# all singleton objects of the same class are referring to the same object
assert id(sqrt_root_two_a) == id(sqrt_root_two_b)
""")

header_md("""Passing arguments to metaclasses""",  nesting = 3)

print_md(""""
Lets extend the previous singleton creating metaclass, so that it can pass parameters to the __init__ method of the object, these parameters are defined together with the metaclass specifier.
""")

eval_and_quote("""

# metaclass are always derived from the type class. 
# The type class has functions to create class objects
# The type class has also a default implementation of the __call__ method, for creating object instances.
class Singleton_metaclass_with_args(type):

    # invoked to create the class object instance (for holding static data)
    # this function is called exactly once, in order to create the class instance!
    def __new__(meta_class, name, bases, cls_dict, **kwargs):

        print("Singleton_metaclass_with_args: __new__ meta_class:", meta_class, "name:", name, "bases:", bases, "cls_dict:", cls_dict, f'kwargs: {kwargs}')

        class_instance = super().__new__(meta_class, name, bases, cls_dict)
        print("Singleton_metaclass_with_args: __new__ return value: ", class_instance, "type(class_instance):", type(class_instance))

        # the class class variable __singleton_instance__ will hold a reference to the one an only object instance of this class.
        class_instance.__singleton_instance__ = None
        
        # the keywords that have been specified, are passed into the class creation method __new__. 
        # save them as a class variable, so as to pass them to the object constructor!
        class_instance.__kwargs__ = kwargs

        return class_instance
 
    def __call__(cls, *args, **kwargs):
        # we get here to create an object instance. the class object has already been created.
        print("Singleton_metaclass_with_args: __call__ args:", *args, f'kwargs: {kwargs}')

        # check if the singleton has already been created.
        if cls.__singleton_instance__ is None:

            # create the one an only instance object.
            instance = cls.__new__(cls)

            # initialise the one and only instance object
            # pass it the keyword parameters specified for the class!
            instance.__init__(*args, **cls.__kwargs__)

            # store the singleton instance object in the class variable __singleton_instance__
            cls.__singleton_instance__ = instance

        # return the singleton instance
        return cls.__singleton_instance__
        
 
import math

class AnySquareRoot:
    def __init__(self, arg_val):
        self.value = math.sqrt(arg_val)
  
 
# the metaclass specifier tells python to use the Singleton_metaclass, for the creation of an instance of type SquareRootOfTwo
class SquareRootOfTwo(AnySquareRoot, metaclass=Singleton_metaclass_with_args, arg_num=2):
    # the init method is called with arg_num specified in the class definition (value of 2)
    def __init__(self, arg_num):
        super().__init__(arg_num)

class SquareRootOfThree(AnySquareRoot, metaclass=Singleton_metaclass_with_args, arg_num=3):
    # the init method is called with arg_num specified in the class definition (value of 3)
    def __init__(self, arg_num):
        super().__init__(arg_num)


print("creating the objects instances...")

sqrt_root_two_a = SquareRootOfTwo()
print("sqrt_two_a id(sqrt_root_two_a):", id(sqrt_root_two_a), "type(sqrt_root_two_a):", type(sqrt_root_two_a), "sqrt_root_two_a.value:", sqrt_root_two_a.value)

sqrt_root_two_b = SquareRootOfTwo()
print("sqrt_two_b id(sqrt_root_two_b)", id(sqrt_root_two_b), "type(sqrt_root_two_b):", type(sqrt_root_two_b), "sqrt_root_two_b.value:", sqrt_root_two_b.value)

# all singleton objects of the same class are referring to the same object
assert id(sqrt_root_two_a) == id(sqrt_root_two_b)

sqrt_root_three_a = SquareRootOfThree()
print("sqrt_three_a id(sqrt_root_three_a):", id(sqrt_root_three_a), "type(sqrt_root_three_a):", type(sqrt_root_three_a), "sqrt_root_three_a.value:", sqrt_root_three_a.value)

sqrt_root_three_b = SquareRootOfThree()
print("sqrt_three_b id(sqrt_root_three_b)", id(sqrt_root_three_b), "type(sqrt_root_three_b):", type(sqrt_root_three_b), "sqrt_root_three_b.value:", sqrt_root_three_b.value)

# all singleton objects of the same class are referring to the same object
assert id(sqrt_root_three_a) == id(sqrt_root_three_b)

""")




header_md("""Metaclasses in the Python3 standard library""", nesting=2)

print_md("""
This section lists examples of meta-classes in the python standard library. Looking at the standard library of a language is often quite useful, when learning about the intricacies of a programming language.
""")

header_md("""ABCMeta class""", nesting=3)

print_md("""The purpose of this metaclass is to define abstract base classes (also known as ABC's), as defined in [PEP 3119](https://www.python.org/dev/peps/pep-3119/), the documentation for the metaclass [ABCMeta class](https://docs.python.org/3/library/abc.html#abc.ABCMeta).

A python metaclass imposes a different behavior for builtin function [isinstance](https://docs.python.org/3/library/functions.html#isinstance) and [issubclass](https://docs.python.org/3/library/functions.html#issubclass) Only classes that are [registered](https://docs.python.org/3/library/abc.html#abc.ABCMeta.register) with the metaclass, are reported as being subclasses of the given metaclass. The referenced PEP explains, why this is needed, i didn't quite understand the explanation. Would be helpful if the reader can clarify this issue.
""")

header_md("""Enum classes""", nesting=3)

print_md("""Python has support for [enum classes](https://docs.python.org/3/library/enum.html). An enum class lists a set of integer class variables, these variables can then be accessed both by their name, and by their integer value.

An example usage: Note that the class doesn't have a constructor, everything is being taken care of by the baseclass [enum.Enum](https://docs.python.org/3/library/enum.html#enum.Enum) which is making use of a meta-class in he definition of the Enum class [here](https://docs.python.org/3/library/enum.html), this metaclass [EnumMeta source code](https://github.com/python/cpython/blob/f6648e229edf07a1e4897244d7d34989dd9ea647/Lib/enum.py#L161)  then creates a behind the scene dictionary, that maps the integer values to their constant names.

The advantage is, that you get an exception, when accessing an undefined constant, or name. There are also more things there, please refer to the linked [documentation](https://docs.python.org/3/library/enum.html)

""")

eval_and_quote("""

import enum

class Rainbow(enum.Enum):
    RED=1
    ORANGE=2
    YELLOW=3
    GREEN=4
    BLUE=5
    INDIGO=6
    VIOLET=7

color=Rainbow.GREEN

print("type(Rainbow.GREEN):", type(Rainbow.GREEN))
print("The string rep Rainbow.Green.name:", Rainbow.GREEN.name, "type(Rainbow.GREEN.name):", type(Rainbow.GREEN.name))
print("The integer rep Rainbow.GREEN.value: ", Rainbow.GREEN.value, "type(Rainbow.GREEN.value):", type(Rainbow.GREEN.value))
print("Access by name: Rainbow['GREEN']:", Rainbow['GREEN'])
print("Access by value: Rainbow(4):", Rainbow(4))

# which is the same thing
assert id(Rainbow['GREEN']) == id(Rainbow(4))

""")

header_md("""Conclusion""", nesting=2)

print_md("""
Python meta-classes and decorators are very similar in their capabilities.
Both are tools for [metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming), tools for modifying the program text, and treating and modifying code, as if it were data.

I would argue, that decorators are most often the easiest way of achieving the same goal.
However some things, like hooking the classification of classes and objects (implementing class methods [__instancecheck__ and __subclasscheck__](https://docs.python.org/3/reference/datamodel.html#customizing-instance-and-subclass-checks), can only be done with meta-classes.

I hope, that this course has given you a better understanding, of what is happening under the hood, which would be a good thing.
""")

print_md("*** eof tutorial ***")
