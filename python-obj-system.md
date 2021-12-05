* [Python object primer for python3 / meta classes](#s1)
  * [Introduction](#s1-1)
  * [The Python object system](#s1-2)
      * [How objects are represented](#s1-2-1)
      * [How classes are represented](#s1-2-2)
      * [Object creation](#s1-2-3)
  * [Custom metaclasses](#s1-3)
      * [Metaclasses for implementing singleton objects](#s1-3-1)
      * [Passing arguments to metaclasses](#s1-3-2)
  * [Metaclasses in the python3 standard library](#s1-4)
      * [ABCMeta class](#s1-4-1)
      * [Enum classes](#s1-4-2)
  * [Conclusion](#s1-5)


# <a id='s1' />Python object primer for python3 / meta classes


## <a id='s1-1' />Introduction

Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand how [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta classes](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system, after having failed to understand meta classes. The purpose of this text is to figure out, how the python object system ticks.


## <a id='s1-2' />The Python object system


### <a id='s1-2-1' />How objects are represented

Lets look at a simple python class Foo with a single base class, and see how objects are created and represented in memory


__Source:__

```


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


```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
```

Memory address where object foo\_obj is stored is returned by the [id built-in](https://docs.python.org/3/library/functions.html#id)

__Source:__

```
print("id(foo_obj) : ", id(foo_obj))
```

__Result:__

```
>> id(foo_obj) :  140679411836672
```

If two variables have the same object id value, then they both refer to the very same object/instance!
each user defined object has a \_\_dict\_\_ attribute, this is a dictionary that lists all the object instance variable.
This also includes instance members that were added by the \_\_init\_\_ method of the base class !!


__Source:__

```
print("foo_obj.__dict__ : ", foo_obj.__dict__)
```

__Result:__

```
>> foo_obj.__dict__ :  {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}
```

So you see that the following is exactly the same thing:


__Source:__

```
assert id(foo_obj.obj_var_a) == id( foo_obj.__dict__['obj_var_a'] ) 
```
Wait, but where does the \_\_dict\_\_ attribute come from?
The [built-in getattr](https://docs.python.org/3/library/functions.html#getattr) function can return this built-in \_\_dict\_\_ attribute!
Interesting: the python notation object.member\_name can mean different things:
  1) for built-in attributes it means a call to getattr
  2) for object instances (assigned in the \_\_init\_\_ method of the class) it means a call to retrieve the \_\_dict\_\_ attribute, and then a lookup of the variable name in that dictionary.

foo\_obj.\_\_dict\_\_ and getattr(foo\_obj,'\_\_dict\_\_',None) is the same thing! 

__Source:__

```
assert id(foo_obj.__dict__) == id( getattr(foo_obj,'__dict__',None) )
```
The getattr builtin function has good part, its return value can be checked for None, to check, if the argument is not an object with a \_\_dict\_\_ attribute.


__Source:__

```
base_obj = object()
```
An object of built-in type  <class 'object'>  doesn't have a \_\_dict\_\_ member

__Source:__

```
assert getattr(base_obj, '__dict__', None) is None
```

__Source:__

```
int_obj = 42
```
An object of built-in type  <class 'int'>  doesn't have a \_\_dict\_\_ member

__Source:__

```
assert getattr(int_obj, '__dict__', None) is None
```
The [dir builtin](https://docs.python.org/3/library/functions.html#dir) function
does different things, depending on the argument,
for regular objects it returns a  "list that contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes."
all this sorted alphabetically.


__Source:__

```
print("dir(foo_obj) : ", dir(foo_obj))
```

__Result:__

```
>> dir(foo_obj) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'obj_var_a', 'obj_var_b', 'obj_var_base', 'show_base', 'show_derived']
```


### <a id='s1-2-2' />How classes are represented

The built-in function [type](https://docs.python.org/3/library/functions.html#type), is returning the class of an object, when applied to a variable

__Source:__

```

# make a new object instance of type Foo class.
foo_obj=Foo()

print("class of object foo_obj - type(foo_obj): ", type(foo_obj))

# that's the same as showing the __class__ member of the variable (in python3)
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
Also note that the type built-in of type(foo\_obj) is really the same as: str(foo\_obj.\_\_class\_\_) (for python3)

Again, the built in attribute \_\_class\_\_ can also be accessed with the getattr built-in function.


__Source:__

```

print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!")
assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) )

```

__Result:__

```
>> foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!
```

the \_\_name\_\_ and \_\_qualname\_\_ built-in attributes return the name of the class, without the module name 

__Source:__

```

print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)
```

__Result:__

```
>> foo_boj.__class__.__name__ :  Foo
>> foo_boj.__class__.__qualname__ :  Foo
```

To get the immedeate base class list as declared in that particular class.


__Source:__

```
print("foo_obj.__class__.__bases__ :", foo_obj.__class__.__bases__)
```

__Result:__

```
>> foo_obj.__class__.__bases__ : (<class '__main__.Base'>,)
```

The mro member of an object stands for 'method resultion order'. This is ;
to get the base class list: this includes all of the base class, recursively traversing all base classes, in depth first traversion order.
This list is used to resolve a member function 'member\_function' of an object, when you call it via: obj\_ref.member\_function()


__Source:__

```
print("foo_obj.__class__.__mro__ :", foo_obj.__class__.__mro__) 
```

__Result:__

```
>> foo_obj.__class__.__mro__ : (<class '__main__.Foo'>, <class '__main__.Base'>, <class 'object'>)
```


__Source:__

```

print("*** mro in detail:")
for cls in foo_obj.__class__.__mro__:
    print_md("	class-in-mro: ", str(cls), "id:", id(cls), "dir(cls): ", dir(cls))
print("*** eof mro in detail")

```

__Result:__

```
>> *** mro in detail:
>> class-in-mro:  <class '\_\_main\_\_.Foo'> id: 140679409948112 dir(cls):  ['\_\_class\_\_', '\_\_delattr\_\_', '\_\_dict\_\_', '\_\_dir\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_format\_\_', '\_\_ge\_\_', '\_\_getattribute\_\_', '\_\_gt\_\_', '\_\_hash\_\_', '\_\_init\_\_', '\_\_init\_subclass\_\_', '\_\_le\_\_', '\_\_lt\_\_', '\_\_module\_\_', '\_\_ne\_\_', '\_\_new\_\_', '\_\_reduce\_\_', '\_\_reduce\_ex\_\_', '\_\_repr\_\_', '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_subclasshook\_\_', '\_\_weakref\_\_', 'base\_clas\_var', 'class\_var', 'class\_var2', 'make\_base', 'make\_foo', 'show\_base', 'show\_derived']
>> class-in-mro:  <class '\_\_main\_\_.Base'> id: 140679409947168 dir(cls):  ['\_\_class\_\_', '\_\_delattr\_\_', '\_\_dict\_\_', '\_\_dir\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_format\_\_', '\_\_ge\_\_', '\_\_getattribute\_\_', '\_\_gt\_\_', '\_\_hash\_\_', '\_\_init\_\_', '\_\_init\_subclass\_\_', '\_\_le\_\_', '\_\_lt\_\_', '\_\_module\_\_', '\_\_ne\_\_', '\_\_new\_\_', '\_\_reduce\_\_', '\_\_reduce\_ex\_\_', '\_\_repr\_\_', '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_subclasshook\_\_', '\_\_weakref\_\_', 'base\_clas\_var', 'make\_base', 'show\_base']
>> class-in-mro:  <class 'object'> id: 4504513456 dir(cls):  ['\_\_class\_\_', '\_\_delattr\_\_', '\_\_dir\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_format\_\_', '\_\_ge\_\_', '\_\_getattribute\_\_', '\_\_gt\_\_', '\_\_hash\_\_', '\_\_init\_\_', '\_\_init\_subclass\_\_', '\_\_le\_\_', '\_\_lt\_\_', '\_\_ne\_\_', '\_\_new\_\_', '\_\_reduce\_\_', '\_\_reduce\_ex\_\_', '\_\_repr\_\_', '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_subclasshook\_\_']
>> *** eof mro in detail
```

the class object has a \_\_dict\_\_ too - here you will see all the class variables (for Foo these are class\_var and class\_var2) and class methods (defined with @staticmethod), but also  the object methods with the self parameter


__Source:__

```
print("foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)
```

__Result:__

```
>> foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7ff27a5e8820>, 'show_derived': <function Foo.show_derived at 0x7ff27a5e88b0>, 'make_foo': <staticmethod object at 0x7ff27a5ea910>, '__doc__': None}
```

Again, the [dir](https://docs.python.org/3/library/functions.html#dir) built-in dir function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
That means it displays both the names of static variables, and the names of the static functions, for the class and it's base classes.
Note that the names are sorted.


__Source:__

```
print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )
```

__Result:__

```
>> dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
```

The class object derives from built-in class type, you can check if an object is a class by checking if it is an instance of class 'type'!


__Source:__

```

assert isinstance(foo_obj.__class__, type)
# same thing as
assert inspect.isclass(foo_obj.__class__)

# an object is not derived from class type
assert not isinstance(foo_obj, type)
# same thng as 
assert not inspect.isclass(foo_obj)

```
Now there is much more. there is the inspect module that returns it all, a kind of rosetta stone of the python object model.
inspect.getmembers returns everything! You can see the source of inspect.getmembers here: https://github.com/python/cpython/blob/3.10/Lib/inspect.py


__Source:__

```
print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))
```

__Result:__

```
>> inspect.getmembers(foo_obj):  [('__class__', <class '__main__.Foo'>), ('__delattr__', <method-wrapper '__delattr__' of Foo object at 0x7ff27a5eaca0>), ('__dict__', {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}), ('__dir__', <built-in method __dir__ of Foo object at 0x7ff27a5eaca0>), ('__doc__', None), ('__eq__', <method-wrapper '__eq__' of Foo object at 0x7ff27a5eaca0>), ('__format__', <built-in method __format__ of Foo object at 0x7ff27a5eaca0>), ('__ge__', <method-wrapper '__ge__' of Foo object at 0x7ff27a5eaca0>), ('__getattribute__', <method-wrapper '__getattribute__' of Foo object at 0x7ff27a5eaca0>), ('__gt__', <method-wrapper '__gt__' of Foo object at 0x7ff27a5eaca0>), ('__hash__', <method-wrapper '__hash__' of Foo object at 0x7ff27a5eaca0>), ('__init__', <bound method Foo.__init__ of <__main__.Foo object at 0x7ff27a5eaca0>>), ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x7ff27a41d5d0>), ('__le__', <method-wrapper '__le__' of Foo object at 0x7ff27a5eaca0>), ('__lt__', <method-wrapper '__lt__' of Foo object at 0x7ff27a5eaca0>), ('__module__', '__main__'), ('__ne__', <method-wrapper '__ne__' of Foo object at 0x7ff27a5eaca0>), ('__new__', <built-in method __new__ of type object at 0x10c7d6bb0>), ('__reduce__', <built-in method __reduce__ of Foo object at 0x7ff27a5eaca0>), ('__reduce_ex__', <built-in method __reduce_ex__ of Foo object at 0x7ff27a5eaca0>), ('__repr__', <method-wrapper '__repr__' of Foo object at 0x7ff27a5eaca0>), ('__setattr__', <method-wrapper '__setattr__' of Foo object at 0x7ff27a5eaca0>), ('__sizeof__', <built-in method __sizeof__ of Foo object at 0x7ff27a5eaca0>), ('__str__', <method-wrapper '__str__' of Foo object at 0x7ff27a5eaca0>), ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x7ff27a41d5d0>), ('__weakref__', None), ('base_clas_var', 'Base'), ('class_var', 42), ('class_var2', 43), ('make_base', <function Base.make_base at 0x7ff27a5e8790>), ('make_foo', <function Foo.make_foo at 0x7ff27a5e8940>), ('obj_var_a', 42), ('obj_var_b', 'name'), ('obj_var_base', 10), ('show_base', <bound method Base.show_base of <__main__.Foo object at 0x7ff27a5eaca0>>), ('show_derived', <bound method Foo.show_derived of <__main__.Foo object at 0x7ff27a5eaca0>>)]
```

Attention!
the type of the object is the Class of the object (remember: the classes is an object, where the \_\_dict\_\_ member holds the class variables)


__Source:__

```

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

```
print("id(foo_obj) : ", id(foo_obj), " str(foo_obj) : ", str(foo_obj))
```

__Result:__

```
>> id(foo_obj) :  140679411838112  str(foo_obj) :  <__main__.Foo object at 0x7ff27a5eaca0>
```

The following expressions refer to the same thing: the type of the object foo\_obj, also known as the class of foo\_obj


__Source:__

```

print("type(foo_obj)            :", type(foo_obj), " id(type(foo_obj))             :", id(type(foo_obj)), " type(foo_obj).__name__ : ", type(foo_obj).__name__ )
print("str(foo_obj.__class__)   :", str(foo_obj.__class__), " id(foo_obj.__class__)         :", id(foo_obj.__class__), "foo_obj.__class__.__name__ : ", foo_obj.__class__.__name__)
print("str(Foo)                 :", str(Foo), " id(Foo)                       :", id( Foo ), "Foo.__name__ :", Foo.__name__)

assert id(Foo) == id(type(foo_obj))
assert id(type(foo_obj)) == id(foo_obj.__class__)

```

__Result:__

```
>> type(foo_obj)            : <class '__main__.Foo'>  id(type(foo_obj))             : 140679409948112  type(foo_obj).__name__ :  Foo
>> str(foo_obj.__class__)   : <class '__main__.Foo'>  id(foo_obj.__class__)         : 140679409948112 foo_obj.__class__.__name__ :  Foo
>> str(Foo)                 : <class '__main__.Foo'>  id(Foo)                       : 140679409948112 Foo.__name__ : Foo
```

The Foo class members


__Source:__

```

print("foo_obj.__class__.__dict__   :", foo_obj.__class__.__dict__)
print("Foo.__dict__                 :", Foo.__dict__)
# everything accessible form the class
print("dir(foo_obj.__class__)       :", dir( foo_obj.__class__))

```

__Result:__

```
>> foo_obj.__class__.__dict__   : {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7ff27a5e8820>, 'show_derived': <function Foo.show_derived at 0x7ff27a5e88b0>, 'make_foo': <staticmethod object at 0x7ff27a5ea910>, '__doc__': None}
>> Foo.__dict__                 : {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7ff27a5e8820>, 'show_derived': <function Foo.show_derived at 0x7ff27a5e88b0>, 'make_foo': <staticmethod object at 0x7ff27a5ea910>, '__doc__': None}
>> dir(foo_obj.__class__)       : ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
```

The following expressions refer to the same thing: the meta-type of the foo\_obj.


__Source:__

```

print("type(foo_obj.__class__.__class__):", type(foo_obj.__class__.__class__), " id( foo_obj.__class__.__class__ ) :" , id( foo_obj.__class__.__class__ ) , "foo_obj.__class__.__class__.__name__ : ", foo_obj.__class__.__class__.__name__ )
print("type(Foo)                        :", type(Foo), " id(type(Foo)) : ", id( type( Foo ) ), " Foo.__class__.__name__ :", Foo.__class__.__name__)
print("type(Foo.__class__)              :", type(Foo.__class__), " id(type(Foo.__class__)) : ", id( type( Foo.__class__ ) ), " Foo.__class__.__name__ :", Foo.__class__.__name__)
print("type(Foo.__class__.__class__)    :", type(Foo.__class__.__class__), " id(type(Foo.__class__.__class__)) :", id( type( Foo.__class__.__class__ ) ) )

assert type(Foo) == type(Foo.__class__)
assert type(Foo.__class__) == type(Foo.__class__.__class__)

```

__Result:__

```
>> type(foo_obj.__class__.__class__): <class 'type'>  id( foo_obj.__class__.__class__ ) : 4504513864 foo_obj.__class__.__class__.__name__ :  type
>> type(Foo)                        : <class 'type'>  id(type(Foo)) :  4504513864  Foo.__class__.__name__ : type
>> type(Foo.__class__)              : <class 'type'>  id(type(Foo.__class__)) :  4504513864  Foo.__class__.__name__ : type
>> type(Foo.__class__.__class__)    : <class 'type'>  id(type(Foo.__class__.__class__)) : 4504513864
```

The type of the type is the metaclass - the metaclass constructs the Class object! (the class of an object is also an object!)


__Source:__

```

print("type( type( foo_obj ) )              :", type( type( foo_obj ) ) )
print("str( foo_obj.__class__.__class__ )   :", str(foo_obj.__class__.__class__) )

```

__Result:__

```
>> type( type( foo_obj ) )              : <class 'type'>
>> str( foo_obj.__class__.__class__ )   : <class 'type'>
```


__Source:__

```

print(" metaclass members: foo_obj.__class__.__class__.__dict__ : ", foo_obj.__class__.__class__.__dict__)
print(" everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) : ", dir( foo_obj.__class__.__class__) )

```

__Result:__

```
>> metaclass members: foo_obj.__class__.__class__.__dict__ :  {'__repr__': <slot wrapper '__repr__' of 'type' objects>, '__call__': <slot wrapper '__call__' of 'type' objects>, '__getattribute__': <slot wrapper '__getattribute__' of 'type' objects>, '__setattr__': <slot wrapper '__setattr__' of 'type' objects>, '__delattr__': <slot wrapper '__delattr__' of 'type' objects>, '__init__': <slot wrapper '__init__' of 'type' objects>, '__new__': <built-in method __new__ of type object at 0x10c7d6d48>, 'mro': <method 'mro' of 'type' objects>, '__subclasses__': <method '__subclasses__' of 'type' objects>, '__prepare__': <method '__prepare__' of 'type' objects>, '__instancecheck__': <method '__instancecheck__' of 'type' objects>, '__subclasscheck__': <method '__subclasscheck__' of 'type' objects>, '__dir__': <method '__dir__' of 'type' objects>, '__sizeof__': <method '__sizeof__' of 'type' objects>, '__basicsize__': <member '__basicsize__' of 'type' objects>, '__itemsize__': <member '__itemsize__' of 'type' objects>, '__flags__': <member '__flags__' of 'type' objects>, '__weakrefoffset__': <member '__weakrefoffset__' of 'type' objects>, '__base__': <member '__base__' of 'type' objects>, '__dictoffset__': <member '__dictoffset__' of 'type' objects>, '__mro__': <member '__mro__' of 'type' objects>, '__name__': <attribute '__name__' of 'type' objects>, '__qualname__': <attribute '__qualname__' of 'type' objects>, '__bases__': <attribute '__bases__' of 'type' objects>, '__module__': <attribute '__module__' of 'type' objects>, '__abstractmethods__': <attribute '__abstractmethods__' of 'type' objects>, '__dict__': <attribute '__dict__' of 'type' objects>, '__doc__': <attribute '__doc__' of 'type' objects>, '__text_signature__': <attribute '__text_signature__' of 'type' objects>}
>>  everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) :  ['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__dir__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__prepare__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__text_signature__', '__weakrefoffset__', 'mro']
```

Wow, any class can tell all of its derived classes! I wonder how that works...


__Source:__

```
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

take the type of Foo - the metaclass of Foo. (the metaclass knows how to create an instance of the class, and instances of the object)
    class\_obj = Foo

The metaclass is used as a 'callable' - it has a \_\_call\_\_ method, and can therefore be called as if it were a function
Now this \_\_call\_\_ method creates and initialises the object instance.
The implementation of \_\_call\_\_ now does two steps:
   - Class creation is done in the [\_\_new\_\_](https://docs.python.org/3/reference/datamodel.html#object.\_\_new\_\_) method of the metaclass. It does a lookup for the Foo class object, remember that this object holds all of the static data. It creates the Foo class instance, if it does not yet exist, upon the first call, otherwise the existing class object is used.
   - It uses the Foo class and calls its to create and initialise the object (call it's \_\_init\_\_ method). This all done by the \_\_call\_\_ method of the class object.
     instance\_of\_foo = class\_obj.\_\_call\_\_()

actually that was a bit of a simplification...


__Source:__

```

# same as: foo_obj = Foo()
foo_obj = Foo.__call__()

print("foo_obj : ", foo_obj)
print("foo_obj.__dict__ : ", foo_obj.__dict__)

```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
>> foo_obj :  <__main__.Foo object at 0x7ff27a5ea340>
>> foo_obj.__dict__ :  {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}
```

This is the same as:

__Source:__

```

class_obj = Foo
instance_of_foo = class_obj()

print("instance_of_foo : ", instance_of_foo)
print("instance_of_foo.__dict__ : ", instance_of_foo.__dict__)

```

__Result:__

```
>> calling Base.__init__
>> calling Foo.__init__
>> instance_of_foo :  <__main__.Foo object at 0x7ff27a5ea160>
>> instance_of_foo.__dict__ :  {'obj_var_base': 10, 'obj_var_a': 42, 'obj_var_b': 'name'}
```


## <a id='s1-3' />Custom metaclasses


### <a id='s1-3-1' />Metaclasses for implementing singleton objects

An object can define a different way of creating itself, it can define a custom metaclass, which will do exactly the same object creation steps described in the last section.

Let's examine a custom metaclass for creating singleton objects.


__Source:__

```


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
>> Singleton_metaclass: __new__ meta_class: <class '__main__.Singleton_metaclass'> name: SquareRootOfTwo bases: () cls_dict: {'__module__': '__main__', '__qualname__': 'SquareRootOfTwo', '__init__': <function SquareRootOfTwo.__init__ at 0x7ff27a5f2ee0>} kwargs: {}
>> Singleton_metaclass: __new__ return value:  <class '__main__.SquareRootOfTwo'> type(class_instance): <class '__main__.Singleton_metaclass'>
>> creating the objects instances...
>> Singleton_metaclass: __call__ args: kwargs: {}
>> SquareRootOfTwo.__init__  self: <__main__.SquareRootOfTwo object at 0x7ff27a5fbf70>
>> sqrt_two_a id(sqrt_root_two_a): 140679411908464 type(sqrt_root_two_a): <class '__main__.SquareRootOfTwo'> sqrt_root_two_a.value: 1.4142135623730951
>> Singleton_metaclass: __call__ args: kwargs: {}
>> sqrt_two_b id(sqrt_root_two_b) 140679411908464 type(sqrt_root_two_b): <class '__main__.SquareRootOfTwo'> sqrt_root_two_b.value: 1.4142135623730951
```


### <a id='s1-3-2' />Passing arguments to metaclasses

"
Lets extend the previous singleton creating metaclass, so that it can pass parameters to the \_\_init\_\_ method of the object, these parameters are defined togather with the metaclass specifier.


__Source:__

```


# metaclass are always derived from the type class. 
# the type class has functions to create class objects
# the type class has also a default implementation of the __call__ method, for creating object instances.
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
>> Singleton_metaclass_with_args: __new__ meta_class: <class '__main__.Singleton_metaclass_with_args'> name: SquareRootOfTwo bases: (<class '__main__.AnySquareRoot'>,) cls_dict: {'__module__': '__main__', '__qualname__': 'SquareRootOfTwo', '__init__': <function SquareRootOfTwo.__init__ at 0x7ff27a5f75e0>, '__classcell__': <cell at 0x7ff27a601910: empty>} kwargs: {'arg_num': 2}
>> Singleton_metaclass_with_args: __new__ return value:  <class '__main__.SquareRootOfTwo'> type(class_instance): <class '__main__.Singleton_metaclass_with_args'>
>> Singleton_metaclass_with_args: __new__ meta_class: <class '__main__.Singleton_metaclass_with_args'> name: SquareRootOfThree bases: (<class '__main__.AnySquareRoot'>,) cls_dict: {'__module__': '__main__', '__qualname__': 'SquareRootOfThree', '__init__': <function SquareRootOfThree.__init__ at 0x7ff27a5f7670>, '__classcell__': <cell at 0x7ff27a601790: empty>} kwargs: {'arg_num': 3}
>> Singleton_metaclass_with_args: __new__ return value:  <class '__main__.SquareRootOfThree'> type(class_instance): <class '__main__.Singleton_metaclass_with_args'>
>> creating the objects instances...
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_two_a id(sqrt_root_two_a): 140679411930928 type(sqrt_root_two_a): <class '__main__.SquareRootOfTwo'> sqrt_root_two_a.value: 1.4142135623730951
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_two_b id(sqrt_root_two_b) 140679411930928 type(sqrt_root_two_b): <class '__main__.SquareRootOfTwo'> sqrt_root_two_b.value: 1.4142135623730951
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_three_a id(sqrt_root_three_a): 140679411930784 type(sqrt_root_three_a): <class '__main__.SquareRootOfThree'> sqrt_root_three_a.value: 1.7320508075688772
>> Singleton_metaclass_with_args: __call__ args: kwargs: {}
>> sqrt_three_b id(sqrt_root_three_b) 140679411930784 type(sqrt_root_three_b): <class '__main__.SquareRootOfThree'> sqrt_root_three_b.value: 1.7320508075688772
```


## <a id='s1-4' />Metaclasses in the python3 standard library

This section lists examples of metaclasses in the python standard library. Looking at the standard library of a language is often quite usefull, when learning about the intricacies of a programming language.


### <a id='s1-4-1' />ABCMeta class

The purpose of this metaclass is to define abstract base classes (also known as ABC's), as defined in [PEP 3119](https://www.python.org/dev/peps/pep-3119/), the documentation for the metaclass [ABCMeta class](https://docs.python.org/3/library/abc.html#abc.ABCMeta).

A python metaclass imposes a different behavior for builtin function [isinstance](https://docs.python.org/3/library/functions.html#isinstance) and [issubclass](https://docs.python.org/3/library/functions.html#issubclass) Only classes that are [registered](https://docs.python.org/3/library/abc.html#abc.ABCMeta.register) with the metaclass, are reported as being subclasses of the given metaclass. The referenced PEP explains, why this is needed, i didn't quite understand the explanation. Would be helpful if the reader can clarify this issue.


### <a id='s1-4-2' />Enum classes

Python has support for [enum classes](https://docs.python.org/3/library/enum.html). An enum class lists a set of integer class variables, these variables can then be accessed both by their name, and by their integer value.

An example usage: Note that the class doesn't have a constructor, everything is being taken care of by the baseclass [enum.Enum](https://docs.python.org/3/library/enum.html#enum.Enum) which is making use of a metaclass in he definition of the Enum class [here](https://docs.python.org/3/library/enum.html), this metaclass [EnumMeta source code](https://github.com/python/cpython/blob/f6648e229edf07a1e4897244d7d34989dd9ea647/Lib/enum.py#L161)  then creates a behind the scene dictionary, that maps the integer values to their constant names.

The advantage is, that you get an exception, when accessing an undefined constant, or name. There are also more things there, please refer to the linked [documentation](https://docs.python.org/3/library/enum.html)



__Source:__

```


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

Python metaclasses and decorators are very similar in their capabilities.
Both are tools for [metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming), tools for modifying the program text, and treating code as data.

I would argue, that decorators are most often the easiest way of achieving the same goal.
However some things, like hooking the classification of classes and objects (implementing class methods [\_\_instancecheck\_\_ and \_\_subclasscheck\_\_](https://docs.python.org/3/reference/datamodel.html#customizing-instance-and-subclass-checks), can only be done with metaclasses.

I hope, that this course has given you a better understanding, of what is happening under the hood, which would be a good thing.

*** eof tutorial ***

