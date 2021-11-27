#!/usr/bin/env python3
import inspect
import sys
import pprintex

# The base class. All python3 classes have the base class of type object.
# the long form is therefore
# class Base(object):
# but pylint will tell you that this long form is redundant

class Base:

    # class variables are shared between all instances of the class Base, and declared like this:
    base_clas_var = "Base"

    # the object constructor/init method, Note the first 'self' argument, which is the object instance.
    def __init__(self):
        # object variables are specific to a given instance of Base
        # each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)
        self.obj_var_base = 10

    # an object method - needs an object instance, which is passed as first 'self' argument.
    def show_base(self):
        print("obj_var_base: ", self.obj_var_base)

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

        # object variables are specific to a given instance of Foo
        # each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)

        # define object variable: obj_var_a
        self.obj_var_a=42

        # define object variable: obj_var_b
        self.obj_var_b="name"

        # when not calling the base class __init__ method: the base class object variables are not added  to the object !!!
        # but then it is called. the 'obj_var_base' member is added to the __dict__ member of this object instance.
        super().__init__()

    # an object method - needs an object instance, which is passed as first 'self' argument.
    def show_derived(self):
        print("obj_var_a:", self.obj_var_a, "obj_var_b:", self.obj_var_b)

    # a class method/static method is called without an object instance.
    @staticmethod
    def make_foo():
        return Foo()

# make a new object instance of type Foo class.
foo_obj=Foo()

print("Memory address where object foo_obj is stored is returned by id built-in")
print("id(foo_obj) : ", id(foo_obj))
print("If two variables have the same object id value, then they both refer to the very same object!")
        
# now this is the same as: (the Foo class has a static method __call__ that makes for the shorthand call.
foo_obj = Foo.__call__()

print("""
each object has a __dict__ attribute, this is a dictionary that lists all the object instance variable.
This includes instance members added by baseclass too!!
""")

# result:
#    foo_obj.__dict__ :  {'obj_var_a': 42, 'obj_var_b': 'name', 'obj_var_base': 10}
print("foo_obj.__dict__ : ", foo_obj.__dict__)

# this uses my pretty printer from here: (and it prints the object id too)
# result:
#    foo instance <class '__main__.Foo'> at 0x7ffbc3521fa0 fields: {
#      'obj_var_a' : 42,
#      'obj_var_b' : 'name',
#      'obj_var_base' : 10
#    }
pprintex.dprint('foo instance', foo_obj)
print("")

print("""
Wait, but where does the __dict__ attribute come from?
The built-in getattr function can return this built-in __dict__ attribute!
Interesting: the python notation object.member_name can mean different things:
  1) for built-in attributes it means a call to getattr
  2) for object instances it mesans a call to retrieve __dict__ attribute, and then a lookup in that dictionary.
""")

print("foo_obj.__dict__ and getattr(foo_obj,'__dict__',None) is the same thing!")
assert id(foo_obj.__dict__) == id( getattr(foo_obj,'__dict__',None) )

# The getattr builtin has good part, it return None, if the argument is not an object with a __dict__ attribute. 
# Tthat can actually happen, for example if you create a object of the following form: obj = object()
#
base_obj = object()
print("a base object of type ", type(base_obj), " doesn't have a __dict__ member")
assert getattr(base_obj, '__dict__', None) == None

int_obj = 42
print("an object of built-in type  ", type(int_obj), " also doesn't have a __dict__ member")
assert getattr(int_obj, '__dict__', None) == None

print("""
The dir builtin function https://docs.python.org/3/library/functions.html#dir
it does different things, depending on the argument,
for regular objects it returns a  "list that contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes."
all this sorted alphabetically.
""")

# result:
#    dir(foo_obj) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'obj_var_a', 'obj_var_b', 'obj_var_base', 'show_base', 'show_derived']

print("dir(foo_obj) : ", dir(foo_obj))

# doesn't have __slots__, how odd.
#print("foo_obj.__slots__ : ", foo_obj.__slots__)

print("""
The class of an object is held in the __class__ attribute of the object.
Note that the name of the class includes the module name, __main__ if the class is defined in the file given as argument to the python interpreter.
""")

#
# result:
#    foo_obj.__class__ : <class '__main__.Foo'>
#

print("""
Also note that the type built-in of type(foo_obj) is really the same as: str(foo_obj.__class__) (for python3)
""")

print("foo_obj.__class__ :", foo_obj.__class__)
print("type(foo_obj) :", type(foo_obj) )


print("""
Again, the built in attribute __class__ can also be accessed with the getattr built-in function.
""")

print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!")
assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) )

print(""" the __name__ abd __qualname__ built-in attributes return the name of the class, without the module name """)

# result:
#    foo_boj.__class__.__name__ :  Foo
#    foo_boj.__class__.__qualname__ :  Foo
#
print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)


print("to get the immedeate base class list as declared in that particular class.")
# result:
#    foo_obj.__class__.__bases__ : (<class '__main__.Base'>,)
print("foo_obj.__class__.__bases__ :", foo_obj.__class__.__bases__)


print("""
mro stands for 'method resultion order'. This is ;
to get the base class list: this includes all of the base class, on all levels, in depth first traversion order.
This list is used to resolve a member function of an object, when you call it via: obj_ref.member_function()
""")
# result;
#    foo_obj.__class__.__mro__ : (<class '__main__.Foo'>, <class '__main__.Base'>, <class 'object'>)
print("foo_obj.__class__.__mro__ :", foo_obj.__class__.__mro__)


# show each class that appears in the mro 'method resulution order'
# result:
#   *** mro in detail:
#        class-in-mro:  <class '__main__.Foo'> id: 140324357869776 dir(cls):  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
#        class-in-mro:  <class '__main__.Base'> id: 140324357868832 dir(cls):  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'make_base', 'show_base']
#        class-in-mro:  <class 'object'> id: 4493945776 dir(cls):  ['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
#    *** eof mro in detail

print("")
print("*** mro in detail:")
for cls in foo_obj.__class__.__mro__:
    print("\tclass-in-mro: ", str(cls), "id:", id(cls), "dir(cls): ", dir(cls))
print("*** eof mro in detail")
print("")


print("""
the class object has a __dict__ too - here you will see all the class variables! (for Foo these are class_var and class_var2)
""")

# result:
#    foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7f9fcfd28a60>, 'show_derived': <function Foo.show_derived at 0x7f9fcfd28af0>, 'make_foo': <staticmethod object at 0x7f9fcfd21f70>, '__doc__': None}

print("foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)

# doen't have slots, how odd.
#print("foo_obj.__class__.__slots__ : ", foo_obj.__class__.__slots__)

print("""
the right way of accessing this info of the class is the built-in dir method.
Again, this built-in function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
""")

# result:
#   dir(foo_obj) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'obj_var_a', 'obj_var_b', 'obj_var_base', 'show_base', 'show_derived']

print("dir(foo_obj) : ", dir( foo_obj ) )

print( """
Now there is much more. there is the inspect module that returns it all, a kind of rosetta stone of the python object model!  
inspect.getmembers returns everything! and it is accessible here: https://github.com/python/cpython/blob/3.10/Lib/inspect.py
""")
#result:
#   inspect.getmembers(foo_obj):  [('__class__', <class '__main__.Foo'>), ('__delattr__', <method-wrapper '__delattr__' of Foo object at 0x7f9bb0d214c0>), ('__dict__', {'obj_var_a': 42, 'obj_var_b': 'name', 'obj_var_base': 10}), ('__dir__', <built-in method __dir__ of Foo object at 0x7f9bb0d214c0>), ('__doc__', None), ('__eq__', <method-wrapper '__eq__' of Foo object at 0x7f9bb0d214c0>), ('__format__', <built-in method __format__ of Foo object at 0x7f9bb0d214c0>), ('__ge__', <method-wrapper '__ge__' of Foo object at 0x7f9bb0d214c0>), ('__getattribute__', <method-wrapper '__getattribute__' of Foo object at 0x7f9bb0d214c0>), ('__gt__', <method-wrapper '__gt__' of Foo object at 0x7f9bb0d214c0>), ('__hash__', <method-wrapper '__hash__' of Foo object at 0x7f9bb0d214c0>), ('__init__', <bound method Foo.__init__ of <__main__.Foo object at 0x7f9bb0d214c0>>), ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x7f9bb0a5a680>), ('__le__', <method-wrapper '__le__' of Foo object at 0x7f9bb0d214c0>), ('__lt__', <method-wrapper '__lt__' of Foo object at 0x7f9bb0d214c0>), ('__module__', '__main__'), ('__ne__', <method-wrapper '__ne__' of Foo object at 0x7f9bb0d214c0>), ('__new__', <built-in method __new__ of type object at 0x10f6c5bb0>), ('__reduce__', <built-in method __reduce__ of Foo object at 0x7f9bb0d214c0>), ('__reduce_ex__', <built-in method __reduce_ex__ of Foo object at 0x7f9bb0d214c0>), ('__repr__', <method-wrapper '__repr__' of Foo object at 0x7f9bb0d214c0>), ('__setattr__', <method-wrapper '__setattr__' of Foo object at 0x7f9bb0d214c0>), ('__sizeof__', <built-in method __sizeof__ of Foo object at 0x7f9bb0d214c0>), ('__str__', <method-wrapper '__str__' of Foo object at 0x7f9bb0d214c0>), ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x7f9bb0a5a680>), ('__weakref__', None), ('base_clas_var', 'Base'), ('class_var', 42), ('class_var2', 43), ('make_base', <function Base.make_base at 0x7f9bb0dd60d0>), ('make_foo', <function Foo.make_foo at 0x7f9bb0dd6280>), ('obj_var_a', 42), ('obj_var_b', 'name'), ('obj_var_base', 10), ('show_base', <bound method Base.show_base of <__main__.Foo object at 0x7f9bb0d214c0>>), ('show_derived', <bound method Foo.show_derived of <__main__.Foo object at 0x7f9bb0d214c0>>)]

print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))


print("""
Attention!
the type of the object is the Class of the object (remember: the classes is an object, where the __dict__ member holds the class variables)
""")

# Result:
#
#    type(foo_obj) :  <class '__main__.Foo'>
#    str(foo_obj.__class__) :  <class '__main__.Foo'>
#    type( type( foo_obj ) ) :  <class 'type'>
#    str( foo_obj.__class__.__class__ ) :  <class 'type'>

print("type(foo_obj) : ", type(foo_obj))
print("str(foo_obj.__class__) : ", str(foo_obj.__class__) )


print("""
The type of the type is the metaclass - the metaclass constructs the Class object! (the class of an object is also an object!)
""")

print("type( type( foo_obj ) ) : ", type( type( foo_obj ) ) )
print("str( foo_obj.__class__.__class__ ) : ", str(foo_obj.__class__.__class__) )

# this gets the classes attributes, as well as that of the class of the class (that one is the metaclass)
# result
#   dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )

# the full, unsanitized story is more than expected:
# result:
#   metaclass members: foo_obj.__class__.__class__.__dict__ :  {'__repr__': <slot wrapper '__repr__' of 'type' objects>, '__call__': <slot wrapper '__call__' of 'type' objects>, '__getattribute__': <slot wrapper '__getattribute__' of 'type' objects>, '__setattr__': <slot wrapper '__setattr__' of 'type' objects>, '__delattr__': <slot wrapper '__delattr__' of 'type' objects>, '__init__': <slot wrapper '__init__' of 'type' objects>, '__new__': <built-in method __new__ of type object at 0x10bdc2d48>, 'mro': <method 'mro' of 'type' objects>, '__subclasses__': <method '__subclasses__' of 'type' objects>, '__prepare__': <method '__prepare__' of 'type' objects>, '__instancecheck__': <method '__instancecheck__' of 'type' objects>, '__subclasscheck__': <method '__subclasscheck__' of 'type' objects>, '__dir__': <method '__dir__' of 'type' objects>, '__sizeof__': <method '__sizeof__' of 'type' objects>, '__basicsize__': <member '__basicsize__' of 'type' objects>, '__itemsize__': <member '__itemsize__' of 'type' objects>, '__flags__': <member '__flags__' of 'type' objects>, '__weakrefoffset__': <member '__weakrefoffset__' of 'type' objects>, '__base__': <member '__base__' of 'type' objects>, '__dictoffset__': <member '__dictoffset__' of 'type' objects>, '__mro__': <member '__mro__' of 'type' objects>, '__name__': <attribute '__name__' of 'type' objects>, '__qualname__': <attribute '__qualname__' of 'type' objects>, '__bases__': <attribute '__bases__' of 'type' objects>, '__module__': <attribute '__module__' of 'type' objects>, '__abstractmethods__': <attribute '__abstractmethods__' of 'type' objects>, '__dict__': <attribute '__dict__' of 'type' objects>, '__doc__': <attribute '__doc__' of 'type' objects>, '__text_signature__': <attribute '__text_signature__' of 'type' objects>}

print("metaclass members: foo_obj.__class__.__class__.__dict__ : ", foo_obj.__class__.__class__.__dict__)

print("""
Wow, any class can tell all of its derived classes! I wonder how that works...
""")

# result:
#    Base.__subclasses__() :  [<class '__main__.Foo'>]
#
print("Base.__subclasses__() : ", Base.__subclasses__())

print("*** eof tutorial ***")
