#!/usr/bin/env python3
from mdformat import *
import pprintex

# function to show a class hierarchy, in depth first search order (like what you get in mro - method resolution order)
def show_type_hierarchy(type_class):

    def show_type_hierarchy_imp(type_class, nesting):
        if  len(type_class.__bases__) == 0:
            return

        prefix = "\t" * nesting
        print_md( prefix + "type:", type_class.__name__ , "base types:", ",".join( map( lambda ty : ty.__name__, type_class.__bases__) ) )
        #print_md( prefix + "str(",  type_class.__name__ , ").__dict__ : ",  type_class.__dict__ )
        for base in type_class.__bases__:
            show_type_hierarchy_imp(base, nesting+1)

    if not inspect.isclass(type_class):
        print_md("object ", str(type_class), " is not classs")
        return

    print_md("show type hierarchy of class:")
    show_type_hierarchy_imp(type_class, 0)


header_md("""Python object primer for python3 / meta classes""" )

header_md("""Introduction""",  nesting = 2)

print_md("""
Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand how [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta classes](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system, after having failed to understand meta classes. The purpose of this text is to figure out, how the python object system ticks.
""")

header_md("""The Python object system""", nesting=2)

header_md("""How objects are represented""", nesting=3)

print_md("""

Lets look at a simple python class Foo with a single base class, and see how objects are created and represented in memory
""")

eval_and_quote("""

# The base class. All python3 classes have the base class of type object.
# the long form is therefore
# class Base(object):
# but pylint will tell you that this long form is redundant

class Base:

    # class variables are shared between all instances of the class Base, and declared like this:
    base_clas_var = "Base"

    # the object constructor/init method, Note the first 'self' argument, which is the object instance.
    def __init__(self):
        print("calling Base.__init__")
        # object variables are specific to a given instance of Base
        # each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)
        self.obj_var_base = 10

    # an object method - needs to access the object instance, which is passed as first 'self' argument.
    def show_base(self):
        print_md("obj_var_base: ", self.obj_var_base)

    # a class method/static method is called without an object instance.
    @staticmethod
    def make_base():
        return Base()

# class Foo with a base class Base
class Foo(Base):

    # class variables are shared between all instances of the class Foo, and declared like this:
    class_var = 42
    class_var2 = 43

    # the object constructor/init method, Note the first 'self' argument, which is the object instance.
    def __init__(self):
        # when not calling the base class __init__ method: the base class object variables are not added  to the object !!!
        # but then it is called. the 'obj_var_base' member is added to the __dict__ member of this object instance.
        # by convention: you first init the base classes, before initialising the derived class.
        super().__init__()

        print("calling Foo.__init__")

        # object variables are specific to a given instance of Foo
        # each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)

        # define object variable: obj_var_a
        self.obj_var_a=42

        # define object variable: obj_var_b
        self.obj_var_b="name"

    # an object method - needs to access the object instance, which is passed as first 'self' argument.
    def show_derived(self):
        print_md("obj_var_a:", self.obj_var_a, "obj_var_b:", self.obj_var_b)

    # a class method/static method is called without an object instance.
    @staticmethod
    def make_foo():
        return Foo()

# make a new object instance of type Foo class.
foo_obj=Foo()

""")

print_md("Memory address where object foo_obj is stored is returned by the [id built-in](https://docs.python.org/3/library/functions.html#id)")

eval_and_quote('print("id(foo_obj) : ", id(foo_obj))')

print_md("If two variables have the same object id value, then they both refer to the very same object/instance!")

print_md("""
each user defined object has a __dict__ attribute, this is a dictionary that lists all the object instance variable.
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
The getattr builtin function has good part, its return value can be checked for None, to check, if the argument is not an object with a __dict__ attribute.
""")

eval_and_quote("""base_obj = object()""")

print_md("An object of built-in type ", type(base_obj), " doesn't have a __dict__ member")
eval_and_quote("""assert getattr(base_obj, '__dict__', None) is None""")

eval_and_quote("""int_obj = 42""")

print_md("An object of built-in type ", type(int_obj), " doesn't have a __dict__ member")

eval_and_quote("""assert getattr(int_obj, '__dict__', None) is None""")

print_md("""
The [dir builtin](https://docs.python.org/3/library/functions.html#dir) function
does different things, depending on the argument,
for regular objects it returns a  "list that contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes."
all this sorted alphabetically.
""")

eval_and_quote("""print("dir(foo_obj) : ", dir(foo_obj))""")

# doesn't have __slots__, how odd.
#print_md("foo_obj.__slots__ : ", foo_obj.__slots__)

print_md("""
The class is an object, it's purpose is to hold the static data that is shared between all object instances.

Each object has a built-in __class__ attribute, that refers to this class object.

Note that the name of the class includes the module name, __main__ if the class is defined in the file given as argument to the python interpreter.
Also note that the type built-in of type(foo_obj) is really the same as: str(foo_obj.__class__) (for python3)
""")


eval_and_quote( """print("foo_obj.__class__ :", foo_obj.__class__)""")


eval_and_quote( """print("type(foo_obj) :", type(foo_obj) )""" )


print_md("""
Again, the built in attribute __class__ can also be accessed with the getattr built-in function.
""")

eval_and_quote( """
print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!")
assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) )
""")

print_md(""" the __name__ and __qualname__ built-in attributes return the name of the class, without the module name """)

eval_and_quote( """
print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)""" )


print_md("""
to get the immedeate base class list as declared in that particular class.
""")

eval_and_quote( """print("foo_obj.__class__.__bases__ :", foo_obj.__class__.__bases__)""")


print_md("""
mro stands for 'method resultion order'. This is ;
to get the base class list: this includes all of the base class, recursively traversing all base classes, in depth first traversion order.
This list is used to resolve a member function 'member_function' of an object, when you call it via: obj_ref.member_function()
""")

eval_and_quote( """print("foo_obj.__class__.__mro__ :", foo_obj.__class__.__mro__) """ )

eval_and_quote("""
print("*** mro in detail:")
for cls in foo_obj.__class__.__mro__:
    print_md("\tclass-in-mro: ", str(cls), "id:", id(cls), "dir(cls): ", dir(cls))
print("*** eof mro in detail")
""")

print_md("""
the class object has a __dict__ too - here you will see all the class variables (for Foo these are class_var and class_var2) and class methods (defined with @staticmethod), but also  the object methods with the self parameter
""")


eval_and_quote( """print("foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)""" )

# doen't have slots, how odd.
#print_md("foo_obj.__class__.__slots__ : ", foo_obj.__class__.__slots__)

print_md("""
Again, the [dir](https://docs.python.org/3/library/functions.html#dir) built-in dir function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
That means it displays both the names of static variables, and the names of the static functions, for the class and it's base classes.
Note that the names are sorted.
""")


eval_and_quote("""print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )""")

print_md("""
The class object derives from built-in class type, you can chekck if an object is a type by checking if it is an instance of type !
""")

# check that foo_obj.__class__ is a type - it is derived from built-in class type
eval_and_quote("""
assert isinstance(foo_obj.__class__, type)
# same thing as
assert inspect.isclass(foo_obj.__class__)""")

print_md( """
Now there is much more. there is the inspect module that returns it all, a kind of rosetta stone of the python object model.
inspect.getmembers returns everything! You can see the source of inspect.getmembers here: https://github.com/python/cpython/blob/3.10/Lib/inspect.py
""")

eval_and_quote("""print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))""")


print_md("""
Attention!
the type of the object is the Class of the object (remember: the classes is an object, where the __dict__ member holds the class variables)
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

take the type of Foo - the metaclass of Foo. (the metaclass knows how to create an instance of the class, and instances of the object)
    class_obj = Foo

The metaclass is used as a 'callable' - it has a __call__ method, and can therefore be called as if it were a function
Now this __call__ method creates and initialises the object instance.
The implementation of __call__ now does two steps:
   - Class creation is done in the [__new__](https://docs.python.org/3/reference/datamodel.html#object.__new__) method of the metaclass. It does a lookup for the Foo class object, remember that this object holds all of the static data. It creates the Foo class instance, if it does not yet exist, upon the first call, otherwise the existing class object is used.
   - It uses the Foo class and calls its to create and initialise the object (call it's __init__ method). This all done by the __call__ method of the class object.
     instance_of_foo = class_obj.__call__()

actually that was a bit of a simplification...
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

print_md("""
An object can define a different way of creating itself, it can define a custom metaclass, which will do exactly the same object creation steps described in the last section.

Let's examine a custom metaclass for creating singleton objects.
""")


eval_and_quote("""

# metaclass are always derived from the type class. 
# the type class has functions to create class objects.
class Singleton_metaclass(type):

    # invoked to create the class object instance (for holding static data)
    # this function is called exactly once, in order to create the class instance!
    def __new__(cls, name, bases, cls_dict):

        print("Singleton_metaclass: __new__ cls:", cls, "name:", name, "bases:", bases, "cls_dict:", cls_dict)
        class_instance = super().__new__(cls, name, bases, cls_dict)
        print("Singleton_metaclass: __new__ return value: ", class_instance, "type(class_instance):", type(class_instance))

        # the class class variable __singleton_instance__ will hold a reference to the one an only object of this class.
        cls.__singleton_instance__ = None

        return class_instance
 
    def __call__(cls, *args, **kwargs):
        # we get here to create an object instance. the class object has already been created.
        print("Singleton_metaclass: __call__ args:", *args, "kwargs:", **kwargs)

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
        print("SquareRootOfTwo.__init__  self:", self)
        self.value = math.sqrt(2)

sqrt_root_two_a = SquareRootOfTwo()
print("sqrt_two_a, id(sqrt_root_two_a):", id(sqrt_root_two_a), "type(sqrt_root_two_a):", type(sqrt_root_two_a), "value:", sqrt_root_two_a.value)

sqrt_root_two_b = SquareRootOfTwo()
print("sqrt_two_b, id(sqrt_root_two_b)", id(sqrt_root_two_b), "type(sqrt_root_two_b):", type(sqrt_root_two_b), "value:", sqrt_root_two_b.value)

# all singleton objects of the same class are referring to the same object
assert id(sqrt_root_two_a) == id(sqrt_root_two_b)
""")

header_md("""Metaclasses in the python3 standard library""", nesting=2)

print_md("""
This section lists examples of metaclasses in the python standard library. Looking at the standard library of a language is often quite usefull, when learning about the intricacies of a programming language.
""")

header_md("""ABCMeta class""", nesting=3)

print_md("""The purpose of this metaclass is to define abstract base classes (also known as ABC's), as defined in [PEP 3119](https://www.python.org/dev/peps/pep-3119/), the documentation for the metaclass [ABCMeta class](https://docs.python.org/3/library/abc.html#abc.ABCMeta).

A python metaclass imposes a different behavior for builtin function [isinstance](https://docs.python.org/3/library/functions.html#isinstance) and [issubclass](https://docs.python.org/3/library/functions.html#issubclass) Only classes that are [registered](https://docs.python.org/3/library/abc.html#abc.ABCMeta.register) with the metaclass, are reported as being subclasses of the given metaclass. The referenced PEP explains, why this is needed, i didn't quite understand the explanation. Would be helpful if the reader can clarify this issue.
""")

header_md("""Enum classes""", nesting=3)

print_md("""Python has support for [enum classes](https://docs.python.org/3/library/enum.html). An enum class lists a set of integer class variables, these variables can then be accessed both by their name, and by their integer value.

An example usage: Note that the class doesn't have a constructor, everything is being taken care of by the baseclass [enum.Enum](https://docs.python.org/3/library/enum.html#enum.Enum) which is making use of a metaclass in he definition of the Enum class [here](https://docs.python.org/3/library/enum.html), this metaclass [EnumMeta source code](https://github.com/python/cpython/blob/f6648e229edf07a1e4897244d7d34989dd9ea647/Lib/enum.py#L161)  then creates a behind the scene dictionary, that maps the integer values to their constant names.

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

print_md("*** eof tutorial ***")
