* [Python object primer for Python3 / meta classes](#s1)
  * [Introduction](#s1-1)
  * [The Python object system](#s1-2)
      * [How objects are represented](#s1-2-1)
      * [How classes are represented](#s1-2-2)
      * [Object creation](#s1-2-3)
  * [Custom metaclasses](#s1-3)
      * [Metaclasses for implementing singleton objects](#s1-3-1)
      * [Passing arguments to metaclasses](#s1-3-2)
  * [Metaclasses in the Python3 standard library](#s1-4)
      * [ABCMeta class](#s1-4-1)
      * [Enum classes](#s1-4-2)
  * [Conclusion](#s1-5)


# <a id='s1' />Python object primer for Python3 / meta classes


## <a id='s1-1' />Introduction

Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta classes](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system. The purpose of this text is to figure out, how the python object system ticks.


## <a id='s1-2' />The Python object system


### <a id='s1-2-1' />How objects are represented

Lets look at a simple python class Foo with a single base class Base, and see how objects are created and represented in memory


__Source:__

```python


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


```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
```

The memory address of object foo\_obj is returned by the [id built-in](https://docs.python.org/3/library/functions.html#id)

__Source:__

```python
print("id(foo_obj) : ", id(foo_obj))
```

__Result:__

```
>> id(foo_obj) :  140509317024208
```

If two variables have the same object id value, then they both refer to the very same object/instance!
Each user defined object has a \_\_dict\_\_ attribute, this is a dictionary that lists all the object instance variables.
This also includes instance members that were added by the \_\_init\_\_ method of the base class !!


__Source:__

```python
print("foo_obj.__dict__ : ", foo_obj.__dict__)
```

__Result:__

```
>> foo_obj.__dict__ :  {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}
```

So you see that the following is exactly the same thing:


__Source:__

```python
assert id(foo_obj.obj_var_a) == id( foo_obj.__dict__['obj_var_a'] ) 
```
Wait, but where does the \_\_dict\_\_ attribute come from?
The [built-in getattr](https://docs.python.org/3/library/functions.html#getattr) function can return this built-in \_\_dict\_\_ attribute!
Interesting: the python notation object.member\_name can mean different things:
  1) for built-in attributes it means a call to getattr
  2) for object instances (assigned in the \_\_init\_\_ method of the class) it means a call to retrieve the \_\_dict\_\_ attribute, and then a lookup of the variable name in that dictionary.

foo\_obj.\_\_dict\_\_ and getattr(foo\_obj,'\_\_dict\_\_',None) is the same thing! 

__Source:__

```python
assert id(foo_obj.__dict__) == id( getattr(foo_obj,'__dict__',None) )
```
The getattr builtin function has a good part, its return value can be checked for None. This can be used, in order to check if the argument is an object with a \_\_dict\_\_ attribute.


__Source:__

```python
base_obj = object()
```
An object of built-in type  <class 'object'>  doesn't have a \_\_dict\_\_ member

__Source:__

```python
assert getattr(base_obj, '__dict__', None) is None
```

__Source:__

```python
int_obj = 42
```
An object of built-in type  <class 'int'>  doesn't have a \_\_dict\_\_ member

__Source:__

```python
assert getattr(int_obj, '__dict__', None) is None
```
The [dir builtin](https://docs.python.org/3/library/functions.html#dir) function does different things, depending on the argument,
for regular objects it returns a  "list that contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes.",
all this is sorted alphabetically.


__Source:__

```python
print("dir(foo_obj) : ", dir(foo_obj))
```

__Result:__

```
>> dir(foo_obj) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_class_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'obj_var_a', 'obj_var_b', 'obj_var_base', 'show_base', 'show_derived']
```


### <a id='s1-2-2' />How classes are represented

The built-in function [type](https://docs.python.org/3/library/functions.html#type), is returning the class of an object, when applied to a variable (to be more exact: type is a built-in class, and not a built-in function, more on that later)

__Source:__

```python

# Make a new object instance of type Foo class.
foo_obj=Foo()

print("class of object foo_obj - type(foo_obj): ", type(foo_obj))

# That's the same as showing the __class__ member of the variable (in Python3)
print("foo_obj.__class__ :", foo_obj.__class__)

```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
>> class of object foo_obj - type(foo_obj):  <class '__main__.Foo'>
>> foo_obj.__class__ : <class '__main__.Foo'>
```

The class is an object, it's purpose is to hold the static data that is shared between all object instances.

Each object has a built-in \_\_class\_\_ attribute, that refers to this class object.

Note that the name of the class includes the module name, \_\_main\_\_ if the class is defined in the file given as argument to the python interpreter.
Also note that the type built-in of type(foo\_obj) is really the same as: str(foo\_obj.\_\_class\_\_) (for Python3)

Again, the built in attribute \_\_class\_\_ can also be accessed with the getattr built-in function.


__Source:__

```python

print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!")
assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) )

```

__Result:__

```
>> foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!
```

The \_\_name\_\_ and \_\_qualname\_\_ built-in attributes return the name of the class, without the module name 

__Source:__

```python

print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)
```

__Result:__

```
>> foo_boj.__class__.__name__ :  Foo
>> foo_boj.__class__.__qualname__ :  Foo
```

To get the immediate base class list as declared in that particular class.


__Source:__

```python
print("foo_obj.__class__.__bases__ :", foo_obj.__class__.__bases__)
```

__Result:__

```
>> foo_obj.__class__.__bases__ : (<class '__main__.Base'>,)
```

The \_\_mro\_\_ member is a list of types that stands for 'method resoultion order', when searching for an instance method, this list is searched in order to resolve the method name.
The Python runtime creates this lists by enumerating all of its base classes recursively, in depth first traversal order. For each class it follows the base classes, from the left ot the right

This list is used to resolve a member function 'member\_function' of an object, when you call it via: obj\_ref.member\_function()


__Source:__

```python
print("foo_obj.__class__.__mro__ :", foo_obj.__class__.__mro__) 
```

__Result:__

```
>> foo_obj.__class__.__mro__ : (<class '__main__.Foo'>, <class '__main__.Base'>, <class 'object'>)
```

Computing the method resolution order by hand

__Source:__

```python


# function to a class hierarchy, in depth first search order (like what you get in MRO - method resolution order)
def show_type_hierarchy(type_class):

    def show_type_hierarchy_imp(type_class, nesting):
        if  len(type_class.__bases__) == 0:
            return

        prefix = "	" * nesting
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

```

__Result:__

```
>> show type hierarchy of class:
>> type: LevelThree base types: LevelTwoFirst,LevelOneThird
>> 	type: LevelTwoFirst base types: LevelOneFirst,LevelOneSecond
>> 		type: LevelOneFirst base types: object
>> 		type: LevelOneSecond base types: object
>> 	type: LevelOneThird base types: object
>> LevelThree.__mro__: (<class '__main__.LevelThree'>, <class '__main__.LevelTwoFirst'>, <class '__main__.LevelOneFirst'>, <class '__main__.LevelOneSecond'>, <class '__main__.LevelOneThird'>, <class 'object'>)
```


__Source:__

```python

print("*** mro in detail:")
for cls in foo_obj.__class__.__mro__:
    print_md("	class-in-mro: ", str(cls), "id:", id(cls), "cls.__dict__: ", cls.__dict__)
print("*** eof mro in detail")

```

__Result:__

```
>> *** mro in detail:
>> class-in-mro:  <class '\_\_main\_\_.Foo'> id: 140509314099168 cls.\_\_dict\_\_:  {'\_\_module\_\_': '\_\_main\_\_', 'class\_var': 42, 'class\_var2': 43, '\_\_init\_\_': <function Foo.\_\_init\_\_ at 0x7fcadfedf160>, 'show\_derived': <function Foo.show\_derived at 0x7fcadfedf1f0>, 'make\_foo': <staticmethod object at 0x7fcadfedcbe0>, '\_\_doc\_\_': None}
>> class-in-mro:  <class '\_\_main\_\_.Base'> id: 140509314098224 cls.\_\_dict\_\_:  {'\_\_module\_\_': '\_\_main\_\_', 'base\_class\_var': 'Base', '\_\_init\_\_': <function Base.\_\_init\_\_ at 0x7fcadfed5f70>, 'show\_base': <function Base.show\_base at 0x7fcadfedf040>, 'make\_base': <staticmethod object at 0x7fcadfedcdc0>, '\_\_dict\_\_': <attribute '\_\_dict\_\_' of 'Base' objects>, '\_\_weakref\_\_': <attribute '\_\_weakref\_\_' of 'Base' objects>, '\_\_doc\_\_': None}
>> class-in-mro:  <class 'object'> id: 4471696304 cls.\_\_dict\_\_:  {'\_\_repr\_\_': <slot wrapper '\_\_repr\_\_' of 'object' objects>, '\_\_hash\_\_': <slot wrapper '\_\_hash\_\_' of 'object' objects>, '\_\_str\_\_': <slot wrapper '\_\_str\_\_' of 'object' objects>, '\_\_getattribute\_\_': <slot wrapper '\_\_getattribute\_\_' of 'object' objects>, '\_\_setattr\_\_': <slot wrapper '\_\_setattr\_\_' of 'object' objects>, '\_\_delattr\_\_': <slot wrapper '\_\_delattr\_\_' of 'object' objects>, '\_\_lt\_\_': <slot wrapper '\_\_lt\_\_' of 'object' objects>, '\_\_le\_\_': <slot wrapper '\_\_le\_\_' of 'object' objects>, '\_\_eq\_\_': <slot wrapper '\_\_eq\_\_' of 'object' objects>, '\_\_ne\_\_': <slot wrapper '\_\_ne\_\_' of 'object' objects>, '\_\_gt\_\_': <slot wrapper '\_\_gt\_\_' of 'object' objects>, '\_\_ge\_\_': <slot wrapper '\_\_ge\_\_' of 'object' objects>, '\_\_init\_\_': <slot wrapper '\_\_init\_\_' of 'object' objects>, '\_\_new\_\_': <built-in method \_\_new\_\_ of type object at 0x10a88abb0>, '\_\_reduce\_ex\_\_': <method '\_\_reduce\_ex\_\_' of 'object' objects>, '\_\_reduce\_\_': <method '\_\_reduce\_\_' of 'object' objects>, '\_\_subclasshook\_\_': <method '\_\_subclasshook\_\_' of 'object' objects>, '\_\_init\_subclass\_\_': <method '\_\_init\_subclass\_\_' of 'object' objects>, '\_\_format\_\_': <method '\_\_format\_\_' of 'object' objects>, '\_\_sizeof\_\_': <method '\_\_sizeof\_\_' of 'object' objects>, '\_\_dir\_\_': <method '\_\_dir\_\_' of 'object' objects>, '\_\_class\_\_': <attribute '\_\_class\_\_' of 'object' objects>, '\_\_doc\_\_': 'The base class of the class hierarchy.\n\nWhen called, it accepts no arguments and returns a new featureless\ninstance that has no instance attributes and cannot be given any.\n'}
>> *** eof mro in detail
```

The class object has a \_\_dict\_\_ too - here you will see all the class variables (for Foo these are class\_var and class\_var2) and class methods (defined with @staticmethod), but also the object methods (with the self parameter)


__Source:__

```python
print("foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)
```

__Result:__

```
>> foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fcadfedf160>, 'show_derived': <function Foo.show_derived at 0x7fcadfedf1f0>, 'make_foo': <staticmethod object at 0x7fcadfedcbe0>, '__doc__': None}
```

Again, the [dir](https://docs.python.org/3/library/functions.html#dir) built-in function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
That means it displays both the names of static variables, and the names of the static functions, for the class and it's base classes.
Note that the names are sorted.


__Source:__

```python
print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )
```

__Result:__

```
>> dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_class_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
```

The class object derives from built-in class type, you can check if an object is a class by checking if it is an instance of class 'type'!


__Source:__

```python

assert isinstance(foo_obj.__class__, type)
# same thing as
assert inspect.isclass(foo_obj.__class__)

# an object is not derived from class type.
assert not isinstance(foo_obj, type)
# same thng as 
assert not inspect.isclass(foo_obj)

```
Now there is much more: there is the inspect module that returns it all, a kind of rosetta stone of the python object model.
inspect.getmembers returns everything! You can see the source of inspect.getmembers [here](https://github.com/python/cpython/blob/3.10/Lib/inspect.py)


__Source:__

```python
print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))
```

__Result:__

```
>> inspect.getmembers(foo_obj):  [('__class__', <class '__main__.Foo'>), ('__delattr__', <method-wrapper '__delattr__' of Foo object at 0x7fcadfec4cd0>), ('__dict__', {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}), ('__dir__', <built-in method __dir__ of Foo object at 0x7fcadfec4cd0>), ('__doc__', None), ('__eq__', <method-wrapper '__eq__' of Foo object at 0x7fcadfec4cd0>), ('__format__', <built-in method __format__ of Foo object at 0x7fcadfec4cd0>), ('__ge__', <method-wrapper '__ge__' of Foo object at 0x7fcadfec4cd0>), ('__getattribute__', <method-wrapper '__getattribute__' of Foo object at 0x7fcadfec4cd0>), ('__gt__', <method-wrapper '__gt__' of Foo object at 0x7fcadfec4cd0>), ('__hash__', <method-wrapper '__hash__' of Foo object at 0x7fcadfec4cd0>), ('__init__', <bound method Foo.__init__ of <__main__.Foo object at 0x7fcadfec4cd0>>), ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x7fcadfc127e0>), ('__le__', <method-wrapper '__le__' of Foo object at 0x7fcadfec4cd0>), ('__lt__', <method-wrapper '__lt__' of Foo object at 0x7fcadfec4cd0>), ('__module__', '__main__'), ('__ne__', <method-wrapper '__ne__' of Foo object at 0x7fcadfec4cd0>), ('__new__', <built-in method __new__ of type object at 0x10a88abb0>), ('__reduce__', <built-in method __reduce__ of Foo object at 0x7fcadfec4cd0>), ('__reduce_ex__', <built-in method __reduce_ex__ of Foo object at 0x7fcadfec4cd0>), ('__repr__', <method-wrapper '__repr__' of Foo object at 0x7fcadfec4cd0>), ('__setattr__', <method-wrapper '__setattr__' of Foo object at 0x7fcadfec4cd0>), ('__sizeof__', <built-in method __sizeof__ of Foo object at 0x7fcadfec4cd0>), ('__str__', <method-wrapper '__str__' of Foo object at 0x7fcadfec4cd0>), ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x7fcadfc127e0>), ('__weakref__', None), ('base_class_var', 'Base'), ('class_var', 42), ('class_var2', 43), ('make_base', <function Base.make_base at 0x7fcadfedf0d0>), ('make_foo', <function Foo.make_foo at 0x7fcadfedf280>), ('obj_var_a', 42), ('obj_var_b', 'name'), ('obj_var_base', 10), ('show_base', <bound method Base.show_base of <__main__.Foo object at 0x7fcadfec4cd0>>), ('show_derived', <bound method Foo.show_derived of <__main__.Foo object at 0x7fcadfec4cd0>>)]
```

Attention!
the type of the object is the class of the object (remember: the classes is an object, where the \_\_dict\_\_ member holds the class variables)


__Source:__

```python

print("type(foo_obj) : ", type(foo_obj))
# same thing in python3
print("str(foo_obj.__class__) : ", str(foo_obj.__class__) )
```

__Result:__

```
>> type(foo_obj) :  <class '__main__.Foo'>
>> str(foo_obj.__class__) :  <class '__main__.Foo'>
```

Let's look at both the type and identity of all these objects:



__Source:__

```python
print("id(foo_obj) : ", id(foo_obj), " str(foo_obj) : ", str(foo_obj))
```

__Result:__

```
>> id(foo_obj) :  140509316926672  str(foo_obj) :  <__main__.Foo object at 0x7fcadfec4cd0>
```

The following expressions refer to the same thing: the type of the object foo\_obj, also known as the class of foo\_obj


__Source:__

```python

print("type(foo_obj)            :", type(foo_obj), " id(type(foo_obj))             :", id(type(foo_obj)), " type(foo_obj).__name__ : ", type(foo_obj).__name__ )
print("str(foo_obj.__class__)   :", str(foo_obj.__class__), " id(foo_obj.__class__)         :", id(foo_obj.__class__), "foo_obj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("str(Foo)                 :", str(Foo), " id(Foo)                       :", id( Foo ), "Foo.__name__ :", Foo.__name__)

assert id(Foo) == id(type(foo_obj))
assert id(type(foo_obj)) == id(foo_obj.__class__)

```

__Result:__

```
>> type(foo_obj)            : <class '__main__.Foo'>  id(type(foo_obj))             : 140509314099168  type(foo_obj).__name__ :  Foo
>> str(foo_obj.__class__)   : <class '__main__.Foo'>  id(foo_obj.__class__)         : 140509314099168 foo_obj.__class__.__name__ :  Foo
>> str(Foo)                 : <class '__main__.Foo'>  id(Foo)                       : 140509314099168 Foo.__name__ : Foo
```

The Foo class members


__Source:__

```python

print("foo_obj.__class__.__dict__   :", foo_obj.__class__.__dict__)
print("Foo.__dict__                 :", Foo.__dict__)
# everything accessible form the class
print("dir(foo_obj.__class__)       :", dir( foo_obj.__class__))

```

__Result:__

```
>> foo_obj.__class__.__dict__   : {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fcadfedf160>, 'show_derived': <function Foo.show_derived at 0x7fcadfedf1f0>, 'make_foo': <staticmethod object at 0x7fcadfedcbe0>, '__doc__': None}
>> Foo.__dict__                 : {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fcadfedf160>, 'show_derived': <function Foo.show_derived at 0x7fcadfedf1f0>, 'make_foo': <staticmethod object at 0x7fcadfedcbe0>, '__doc__': None}
>> dir(foo_obj.__class__)       : ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_class_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
```

The following expressions refer to the same thing: the meta-type of the foo\_obj.


__Source:__

```python

print("type(foo_obj.__class__.__class__):", type(foo_obj.__class__.__class__), " id( foo_obj.__class__.__class__ ) :" , id( foo_obj.__class__.__class__ ) , "foo_obj.__class__.__class__.__name__ : ", foo_obj.__class__.__class__.__name__ )
print("type(Foo)                        :", type(Foo), " id(type(Foo)) : ", id( type( Foo ) ), " Foo.__class__.__name__ :", Foo.__class__.__name__)
print("type(Foo.__class__)              :", type(Foo.__class__), " id(type(Foo.__class__)) : ", id( type( Foo.__class__ ) ), " Foo.__class__.__name__ :", Foo.__class__.__name__)
print("type(Foo.__class__.__class__)    :", type(Foo.__class__.__class__), " id(type(Foo.__class__.__class__)) :", id( type( Foo.__class__.__class__ ) ) )

assert type(Foo) == type(Foo.__class__)
assert type(Foo.__class__) == type(Foo.__class__.__class__)

```

__Result:__

```
>> type(foo_obj.__class__.__class__): <class 'type'>  id( foo_obj.__class__.__class__ ) : 4471696712 foo_obj.__class__.__class__.__name__ :  type
>> type(Foo)                        : <class 'type'>  id(type(Foo)) :  4471696712  Foo.__class__.__name__ : type
>> type(Foo.__class__)              : <class 'type'>  id(type(Foo.__class__)) :  4471696712  Foo.__class__.__name__ : type
>> type(Foo.__class__.__class__)    : <class 'type'>  id(type(Foo.__class__.__class__)) : 4471696712
```

The type of the type is the metaclass - the metaclass constructs the Class object! (the class of an object is also an object!)


__Source:__

```python

print("type( type( foo_obj ) )              :", type( type( foo_obj ) ) )
print("str( foo_obj.__class__.__class__ )   :", str(foo_obj.__class__.__class__) )

```

__Result:__

```
>> type( type( foo_obj ) )              : <class 'type'>
>> str( foo_obj.__class__.__class__ )   : <class 'type'>
```


__Source:__

```python

print(" metaclass members: foo_obj.__class__.__class__.__dict__ : ", foo_obj.__class__.__class__.__dict__)
print(" everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) : ", dir( foo_obj.__class__.__class__) )

```

__Result:__

```
>> metaclass members: foo_obj.__class__.__class__.__dict__ :  {'__repr__': <slot wrapper '__repr__' of 'type' objects>, '__call__': <slot wrapper '__call__' of 'type' objects>, '__getattribute__': <slot wrapper '__getattribute__' of 'type' objects>, '__setattr__': <slot wrapper '__setattr__' of 'type' objects>, '__delattr__': <slot wrapper '__delattr__' of 'type' objects>, '__init__': <slot wrapper '__init__' of 'type' objects>, '__new__': <built-in method __new__ of type object at 0x10a88ad48>, 'mro': <method 'mro' of 'type' objects>, '__subclasses__': <method '__subclasses__' of 'type' objects>, '__prepare__': <method '__prepare__' of 'type' objects>, '__instancecheck__': <method '__instancecheck__' of 'type' objects>, '__subclasscheck__': <method '__subclasscheck__' of 'type' objects>, '__dir__': <method '__dir__' of 'type' objects>, '__sizeof__': <method '__sizeof__' of 'type' objects>, '__basicsize__': <member '__basicsize__' of 'type' objects>, '__itemsize__': <member '__itemsize__' of 'type' objects>, '__flags__': <member '__flags__' of 'type' objects>, '__weakrefoffset__': <member '__weakrefoffset__' of 'type' objects>, '__base__': <member '__base__' of 'type' objects>, '__dictoffset__': <member '__dictoffset__' of 'type' objects>, '__mro__': <member '__mro__' of 'type' objects>, '__name__': <attribute '__name__' of 'type' objects>, '__qualname__': <attribute '__qualname__' of 'type' objects>, '__bases__': <attribute '__bases__' of 'type' objects>, '__module__': <attribute '__module__' of 'type' objects>, '__abstractmethods__': <attribute '__abstractmethods__' of 'type' objects>, '__dict__': <attribute '__dict__' of 'type' objects>, '__doc__': <attribute '__doc__' of 'type' objects>, '__text_signature__': <attribute '__text_signature__' of 'type' objects>}
>>  everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) :  ['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__dir__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__prepare__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__text_signature__', '__weakrefoffset__', 'mro']
```

Wow, any class can tell all of its derived classes! I wonder how that works...


__Source:__

```python
print("Base.__subclasses__() : ", Base.__subclasses__())
```

__Result:__

```
>> Base.__subclasses__() :  [<class '__main__.Foo'>]
```


### <a id='s1-2-3' />Object creation

Objects recap:
    The object instance holds the \_\_dict\_\_ attribute of the object instance, it's value is a dictionary that holds the object instance members.
    The class is an object that is shared between all object instances, and it holds the static data (class variables, class methods)

What happens upon: foo = Foo() ?

Take the type of Foo - the metaclass of Foo, the metaclass both knows how to create an instance of the class Foo, and the object instances.
A metaclass is derived from built-in class 'type', The 'type' constructor with three argument creates a new class object. [see reference](https://docs.python.org/3/library/functions.html#type)

    class\_obj = Foo

The metaclass is used as a 'callable' - it has a \_\_call\_\_ method, and can therefore be called as if it were a function (see more about callables in the course on [decorators](https://github.com/MoserMichael/python-obj-system/blob/master/decorator.md))

Now this \_\_call\_\_ method creates and initialises the object instance.
The implementation of \_\_call\_\_ now does two steps:
   - Class creation is done in the [\_\_new\_\_](https://docs.python.org/3/reference/datamodel.html#object.\_\_new\_\_) method of the metaclass.  The \_\_new\_\_ method creates the Foo class, it is called exactly once, upon class declaration (you will see this shortly, in the section on custom meta classes)
   - It uses the Foo class and calls its to create and initialise the object (call the \_\_new\_\_ method of the Foo class, in order to create an instance of Foo, then calls the \_\_init\_\_ instance method of the Foo class, on order to initialise it). This all done by the \_\_call\_\_ method of the metaclass.
     instance\_of\_foo = meta\_class\_obj.\_\_call\_\_()

(actually that was a bit of a simplification...
)


__Source:__

```python

# same as: foo_obj = Foo()
foo_obj = Foo.__call__()

print("foo_obj : ", foo_obj)
print("foo_obj.__dict__ : ", foo_obj.__dict__)

```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
>> foo_obj :  <__main__.Foo object at 0x7fcadfee6910>
>> foo_obj.__dict__ :  {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}
```

This is the same as:

__Source:__

```python

class_obj = Foo
instance_of_foo = class_obj()

print("instance_of_foo : ", instance_of_foo)
print("instance_of_foo.__dict__ : ", instance_of_foo.__dict__)

```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
>> instance_of_foo :  <__main__.Foo object at 0x7fcadfec4d60>
>> instance_of_foo.__dict__ :  {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}
```


## <a id='s1-3' />Custom metaclasses


### <a id='s1-3-1' />Metaclasses for implementing singleton objects

An object can define a different way of creating itself, it can define a custom metaclass, which will do exactly the same object creation steps described in the last section.

Let's examine a custom metaclass for creating singleton objects.


__Source:__

```python


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

```

__Result:__

```
>> Singleton_metaclass: __new__ meta_class: <class '__main__.Singleton_metaclass'> name: SquareRootOfTwo bases: () cls_dict: {'__module__': '__main__', '__qualname__': 'SquareRootOfTwo', '__init__': <function SquareRootOfTwo.__init__ at 0x7fcadfee3430>} kwargs: {}
>> Singleton_metaclass: __new__ return value:  <class '__main__.SquareRootOfTwo'> type(class_instance): <class '__main__.Singleton_metaclass'>
>> creating the objects instances...
>> Singleton_metaclass: __call__ args: kwargs: {}
>> SquareRootOfTwo.__init__  self: <__main__.SquareRootOfTwo object at 0x7fcadfee4f10>
>> sqrt_two_a id(sqrt_root_two_a): 140509317058320 type(sqrt_root_two_a): <class '__main__.SquareRootOfTwo'> sqrt_root_two_a.value: 1.4142135623730951
>> Singleton_metaclass: __call__ args: kwargs: {}
>> sqrt_two_b id(sqrt_root_two_b) 140509317058320 type(sqrt_root_two_b): <class '__main__.SquareRootOfTwo'> sqrt_root_two_b.value: 1.4142135623730951
```


### <a id='s1-3-2' />Passing arguments to metaclasses

"
Lets extend the previous singleton creating metaclass, so that it can pass parameters to the \_\_init\_\_ method of the object, these parameters are defined together with the metaclass specifier.


__Source:__

```python


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


```

__Result:__

```
>> Singleton_metaclass_with_args: __new__ meta_class: <class '__main__.Singleton_metaclass_with_args'> name: SquareRootOfTwo bases: (<class '__main__.AnySquareRoot'>,) cls_dict: {'__module__': '__main__', '__qualname__': 'SquareRootOfTwo', '__init__': <function SquareRootOfTwo.__init__ at 0x7fcadfedfe50>, '__classcell__': <cell at 0x7fcadfee5f70: empty>} kwargs: {'arg_num': 2}
>> Singleton_metaclass_with_args: __new__ return value:  <class '__main__.SquareRootOfTwo'> type(class_instance): <class '__main__.Singleton_metaclass_with_args'>
>> Singleton_metaclass_with_args: __new__ meta_class: <class '__main__.Singleton_metaclass_with_args'> name: SquareRootOfThree bases: (<class '__main__.AnySquareRoot'>,) cls_dict: {'__module__': '__main__', '__qualname__': 'SquareRootOfThree', '__init__': <function SquareRootOfThree.__init__ at 0x7fcadfedfd30>, '__classcell__': <cell at 0x7fcadfee5df0: empty>} kwargs: {'arg_num': 3}
>> Singleton_metaclass_with_args: __new__ return value:  <class '__main__.SquareRootOfThree'> type(class_instance): <class '__main__.Singleton_metaclass_with_args'>
>> creating the objects instances...
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_two_a id(sqrt_root_two_a): 140509317062032 type(sqrt_root_two_a): <class '__main__.SquareRootOfTwo'> sqrt_root_two_a.value: 1.4142135623730951
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_two_b id(sqrt_root_two_b) 140509317062032 type(sqrt_root_two_b): <class '__main__.SquareRootOfTwo'> sqrt_root_two_b.value: 1.4142135623730951
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_three_a id(sqrt_root_three_a): 140509317061888 type(sqrt_root_three_a): <class '__main__.SquareRootOfThree'> sqrt_root_three_a.value: 1.7320508075688772
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_three_b id(sqrt_root_three_b) 140509317061888 type(sqrt_root_three_b): <class '__main__.SquareRootOfThree'> sqrt_root_three_b.value: 1.7320508075688772
```


## <a id='s1-4' />Metaclasses in the Python3 standard library

This section lists examples of meta-classes in the python standard library. Looking at the standard library of a language is often quite useful, when learning about the intricacies of a programming language.


### <a id='s1-4-1' />ABCMeta class

The purpose of this metaclass is to define abstract base classes (also known as ABC's), as defined in [PEP 3119](https://www.python.org/dev/peps/pep-3119/), the documentation for the metaclass [ABCMeta class](https://docs.python.org/3/library/abc.html#abc.ABCMeta).

A python metaclass imposes a different behavior for builtin function [isinstance](https://docs.python.org/3/library/functions.html#isinstance) and [issubclass](https://docs.python.org/3/library/functions.html#issubclass) Only classes that are [registered](https://docs.python.org/3/library/abc.html#abc.ABCMeta.register) with the metaclass, are reported as being subclasses of the given metaclass. The referenced PEP explains, why this is needed, i didn't quite understand the explanation. Would be helpful if the reader can clarify this issue.


### <a id='s1-4-2' />Enum classes

Python has support for [enum classes](https://docs.python.org/3/library/enum.html). An enum class lists a set of integer class variables, these variables can then be accessed both by their name, and by their integer value.

An example usage: Note that the class doesn't have a constructor, everything is being taken care of by the baseclass [enum.Enum](https://docs.python.org/3/library/enum.html#enum.Enum) which is making use of a meta-class in he definition of the Enum class [here](https://docs.python.org/3/library/enum.html), this metaclass [EnumMeta source code](https://github.com/python/cpython/blob/f6648e229edf07a1e4897244d7d34989dd9ea647/Lib/enum.py#L161)  then creates a behind the scene dictionary, that maps the integer values to their constant names.

The advantage is, that you get an exception, when accessing an undefined constant, or name. There are also more things there, please refer to the linked [documentation](https://docs.python.org/3/library/enum.html)



__Source:__

```python


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


```

__Result:__

```
>> type(Rainbow.GREEN): <enum 'Rainbow'>
>> The string rep Rainbow.Green.name: GREEN type(Rainbow.GREEN.name): <class 'str'>
>> The integer rep Rainbow.GREEN.value:  4 type(Rainbow.GREEN.value): <class 'int'>
>> Access by name: Rainbow['GREEN']: Rainbow.GREEN
>> Access by value: Rainbow(4): Rainbow.GREEN
```


## <a id='s1-5' />Conclusion

Python meta-classes and decorators are very similar in their capabilities.
Both are tools for [metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming), tools for modifying the program text, and treating and modifying code, as if it were data.

I would argue, that decorators are most often the easiest way of achieving the same goal.
However some things, like hooking the classification of classes and objects (implementing class methods [\_\_instancecheck\_\_ and \_\_subclasscheck\_\_](https://docs.python.org/3/reference/datamodel.html#customizing-instance-and-subclass-checks), can only be done with meta-classes.

I hope, that this course has given you a better understanding, of what is happening under the hood, which would be a good thing.

*** eof tutorial ***

