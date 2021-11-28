" Set text width as 72.

Memory address where object foo\_obj is stored is returned by id built-in
```id(foo_obj) :  140615532923296```
If two variables have the same object id value, then they both refer to the very same object/instance!

each user defined object has a \_\_dict\_\_ attribute, this is a dictionary that lists all the object instance variable.
This also includes instance members that were added by the \_\_init\_\_ method of the base class !!

```foo_obj.__dict__ :  {'obj_var_a': 42, 'obj_var_b': 'name', 'obj_var_base': 10}```
```
foo instance <class '__main__.Foo'> at 0x7fe39ae3c460 fields: {
  'obj_var_a' : 42,
  'obj_var_b' : 'name',
  'obj_var_base' : 10
}
```


Wait, but where does the \_\_dict\_\_ attribute come from?
The built-in getattr function can return this built-in \_\_dict\_\_ attribute!
Interesting: the python notation object.member\_name can mean different things:
  1) for built-in attributes it means a call to getattr
  2) for object instances (assigned in the \_\_init\_\_ method of the class) it means a call to retrieve the \_\_dict\_\_ attribute, and then a lookup of the variable name in that dictionary.

foo\_obj.\_\_dict\_\_ and getattr(foo\_obj,'\_\_dict\_\_',None) is the same thing!

The getattr builtin function has good part, its return value can be checked for None, to check, if the argument is not an object with a \_\_dict\_\_ attribute.

An object of built-in type  <class 'object'>  doesn't have a \_\_dict\_\_ member
An object of built-in type  <class 'int'>  doesn't have a \_\_dict\_\_ member

The dir builtin function https://docs.python.org/3/library/functions.html#dir
it does different things, depending on the argument,
for regular objects it returns a  "list that contains the object’s attributes’ names, the names of its class’s attributes, and recursively of the attributes of its class’s base classes."
all this sorted alphabetically.

```dir(foo_obj) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'obj_var_a', 'obj_var_b', 'obj_var_base', 'show_base', 'show_derived']```

The class is an object, it's purpose is to hold the static data that is shared between all object instances.

Each object has a built-in \_\_class\_\_ attribute, that refers to this class object.

Note that the name of the class includes the module name, \_\_main\_\_ if the class is defined in the file given as argument to the python interpreter.
Also note that the type built-in of type(foo\_obj) is really the same as: str(foo\_obj.\_\_class\_\_) (for python3)

```foo_obj.__class__ : <class '__main__.Foo'>```
```type(foo_obj) : <class '__main__.Foo'>```

Again, the built in attribute \_\_class\_\_ can also be accessed with the getattr built-in function.

```foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!```
 the \_\_name\_\_ and \_\_qualname\_\_ built-in attributes return the name of the class, without the module name 
```foo_boj.__class__.__name__ :  Foo```
```foo_boj.__class__.__qualname__ :  Foo```

to get the immedeate base class list as declared in that particular class.

```foo_obj.__class__.__bases__ : (<class '__main__.Base'>,)```

mro stands for 'method resultion order'. This is ;
to get the base class list: this includes all of the base class, recursively traversing all base classes, in depth first traversion order.
This list is used to resolve a member function 'member\_function' of an object, when you call it via: obj\_ref.member\_function()

```foo_obj.__class__.__mro__ : (<class '__main__.Foo'>, <class '__main__.Base'>, <class 'object'>)```
```

*** mro in detail:
	class-in-mro:  <class '\_\_main\_\_.Foo'> id: 140615529710560 dir(cls):  ['\_\_class\_\_', '\_\_delattr\_\_', '\_\_dict\_\_', '\_\_dir\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_format\_\_', '\_\_ge\_\_', '\_\_getattribute\_\_', '\_\_gt\_\_', '\_\_hash\_\_', '\_\_init\_\_', '\_\_init\_subclass\_\_', '\_\_le\_\_', '\_\_lt\_\_', '\_\_module\_\_', '\_\_ne\_\_', '\_\_new\_\_', '\_\_reduce\_\_', '\_\_reduce\_ex\_\_', '\_\_repr\_\_', '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_subclasshook\_\_', '\_\_weakref\_\_', 'base\_clas\_var', 'class\_var', 'class\_var2', 'make\_base', 'make\_foo', 'show\_base', 'show\_derived']
	class-in-mro:  <class '\_\_main\_\_.Base'> id: 140615529709616 dir(cls):  ['\_\_class\_\_', '\_\_delattr\_\_', '\_\_dict\_\_', '\_\_dir\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_format\_\_', '\_\_ge\_\_', '\_\_getattribute\_\_', '\_\_gt\_\_', '\_\_hash\_\_', '\_\_init\_\_', '\_\_init\_subclass\_\_', '\_\_le\_\_', '\_\_lt\_\_', '\_\_module\_\_', '\_\_ne\_\_', '\_\_new\_\_', '\_\_reduce\_\_', '\_\_reduce\_ex\_\_', '\_\_repr\_\_', '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_subclasshook\_\_', '\_\_weakref\_\_', 'base\_clas\_var', 'make\_base', 'show\_base']
	class-in-mro:  <class 'object'> id: 4525837232 dir(cls):  ['\_\_class\_\_', '\_\_delattr\_\_', '\_\_dir\_\_', '\_\_doc\_\_', '\_\_eq\_\_', '\_\_format\_\_', '\_\_ge\_\_', '\_\_getattribute\_\_', '\_\_gt\_\_', '\_\_hash\_\_', '\_\_init\_\_', '\_\_init\_subclass\_\_', '\_\_le\_\_', '\_\_lt\_\_', '\_\_ne\_\_', '\_\_new\_\_', '\_\_reduce\_\_', '\_\_reduce\_ex\_\_', '\_\_repr\_\_', '\_\_setattr\_\_', '\_\_sizeof\_\_', '\_\_str\_\_', '\_\_subclasshook\_\_']
*** eof mro in detail

```

the class object has a \_\_dict\_\_ too - here you will see all the class variables (for Foo these are class\_var and class\_var2) and class methods (defined with @staticmethod), but also  the object methods with the self parameter

```foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fe39aedd670>, 'show_derived': <function Foo.show_derived at 0x7fe39aedd700>, 'make_foo': <staticmethod object at 0x7fe39ae3cc70>, '__doc__': None}```

the dir method for a class:
Again, this built-in dir function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
Note that the names are sorted.

```dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']```

The class object derives from built-in class type, you can chekck if an object is a type by checking if it is an instance of type !


Now there is much more. there is the inspect module that returns it all, a kind of rosetta stone of the python object model.
inspect.getmembers returns everything! You can see the source of inspect.getmembers here: https://github.com/python/cpython/blob/3.10/Lib/inspect.py

```inspect.getmembers(foo_obj):  [('__class__', <class '__main__.Foo'>), ('__delattr__', <method-wrapper '__delattr__' of Foo object at 0x7fe39ae3c460>), ('__dict__', {'obj_var_a': 42, 'obj_var_b': 'name', 'obj_var_base': 10}), ('__dir__', <built-in method __dir__ of Foo object at 0x7fe39ae3c460>), ('__doc__', None), ('__eq__', <method-wrapper '__eq__' of Foo object at 0x7fe39ae3c460>), ('__format__', <built-in method __format__ of Foo object at 0x7fe39ae3c460>), ('__ge__', <method-wrapper '__ge__' of Foo object at 0x7fe39ae3c460>), ('__getattribute__', <method-wrapper '__getattribute__' of Foo object at 0x7fe39ae3c460>), ('__gt__', <method-wrapper '__gt__' of Foo object at 0x7fe39ae3c460>), ('__hash__', <method-wrapper '__hash__' of Foo object at 0x7fe39ae3c460>), ('__init__', <bound method Foo.__init__ of <__main__.Foo object at 0x7fe39ae3c460>>), ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x7fe39ab2c3e0>), ('__le__', <method-wrapper '__le__' of Foo object at 0x7fe39ae3c460>), ('__lt__', <method-wrapper '__lt__' of Foo object at 0x7fe39ae3c460>), ('__module__', '__main__'), ('__ne__', <method-wrapper '__ne__' of Foo object at 0x7fe39ae3c460>), ('__new__', <built-in method __new__ of type object at 0x10dc2cbb0>), ('__reduce__', <built-in method __reduce__ of Foo object at 0x7fe39ae3c460>), ('__reduce_ex__', <built-in method __reduce_ex__ of Foo object at 0x7fe39ae3c460>), ('__repr__', <method-wrapper '__repr__' of Foo object at 0x7fe39ae3c460>), ('__setattr__', <method-wrapper '__setattr__' of Foo object at 0x7fe39ae3c460>), ('__sizeof__', <built-in method __sizeof__ of Foo object at 0x7fe39ae3c460>), ('__str__', <method-wrapper '__str__' of Foo object at 0x7fe39ae3c460>), ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x7fe39ab2c3e0>), ('__weakref__', None), ('base_clas_var', 'Base'), ('class_var', 42), ('class_var2', 43), ('make_base', <function Base.make_base at 0x7fe39aedd5e0>), ('make_foo', <function Foo.make_foo at 0x7fe39aedd790>), ('obj_var_a', 42), ('obj_var_b', 'name'), ('obj_var_base', 10), ('show_base', <bound method Base.show_base of <__main__.Foo object at 0x7fe39ae3c460>>), ('show_derived', <bound method Foo.show_derived of <__main__.Foo object at 0x7fe39ae3c460>>)]```

Attention!
the type of the object is the Class of the object (remember: the classes is an object, where the \_\_dict\_\_ member holds the class variables)

```type(foo_obj) :  <class '__main__.Foo'>```
```str(foo_obj.__class__) :  <class '__main__.Foo'>```


Let's look at both the type and identity of all these objects:


```id(foo_obj) :  140615532921952  str(foo_obj) :  <__main__.Foo object at 0x7fe39ae3c460>```

The following expressions refer to the same thing: the type of the object foo\_obj, also known as the class of foo\_obj

```type(foo_obj) :  <class '__main__.Foo'>  id(type(foo_obj)) :  140615529710560  type(foo_obj).__name__ :  Foo```
```str(foo_obj.__class__) :  <class '__main__.Foo'>  id(foo_obj.__class__) :  140615529710560 foo_obj.__class__.__name__ :  Foo```
```str(Foo) :  <class '__main__.Foo'>  id(Foo) :  140615529710560 Foo.__name__ :  Foo```

    The Foo class members

``` foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fe39aedd670>, 'show_derived': <function Foo.show_derived at 0x7fe39aedd700>, 'make_foo': <staticmethod object at 0x7fe39ae3cc70>, '__doc__': None}```
``` Foo.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fe39aedd670>, 'show_derived': <function Foo.show_derived at 0x7fe39aedd700>, 'make_foo': <staticmethod object at 0x7fe39ae3cc70>, '__doc__': None}```
``` dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']```

The following expressions refer to the same thing: the meta-type of the foo\_obj.

```type(foo_obj.__class__.__class__) :  <class 'type'>  id( foo_obj.__class__.__class__ ) :  4525837640 foo_obj.__class__.__class__.__name__ :  type```
```type(Foo) :  <class 'type'>  id(type(Foo)) :  4525837640  Foo.__class__.__name__ :  type```
```type(Foo.__class__) :  <class 'type'>  id(type(Foo.__class__)) :  4525837640  Foo.__class__.__name__ :  type```
```type(Foo.__class__.__class__)  <class 'type'>  id(type(Foo.__class__.__class__)) :  4525837640```

The type of the type is the metaclass - the metaclass constructs the Class object! (the class of an object is also an object!)

```type( type( foo_obj ) ) :  <class 'type'>```
```str( foo_obj.__class__.__class__ ) :  <class 'type'>```
``` metaclass members: foo_obj.__class__.__class__.__dict__ :  {'__repr__': <slot wrapper '__repr__' of 'type' objects>, '__call__': <slot wrapper '__call__' of 'type' objects>, '__getattribute__': <slot wrapper '__getattribute__' of 'type' objects>, '__setattr__': <slot wrapper '__setattr__' of 'type' objects>, '__delattr__': <slot wrapper '__delattr__' of 'type' objects>, '__init__': <slot wrapper '__init__' of 'type' objects>, '__new__': <built-in method __new__ of type object at 0x10dc2cd48>, 'mro': <method 'mro' of 'type' objects>, '__subclasses__': <method '__subclasses__' of 'type' objects>, '__prepare__': <method '__prepare__' of 'type' objects>, '__instancecheck__': <method '__instancecheck__' of 'type' objects>, '__subclasscheck__': <method '__subclasscheck__' of 'type' objects>, '__dir__': <method '__dir__' of 'type' objects>, '__sizeof__': <method '__sizeof__' of 'type' objects>, '__basicsize__': <member '__basicsize__' of 'type' objects>, '__itemsize__': <member '__itemsize__' of 'type' objects>, '__flags__': <member '__flags__' of 'type' objects>, '__weakrefoffset__': <member '__weakrefoffset__' of 'type' objects>, '__base__': <member '__base__' of 'type' objects>, '__dictoffset__': <member '__dictoffset__' of 'type' objects>, '__mro__': <member '__mro__' of 'type' objects>, '__name__': <attribute '__name__' of 'type' objects>, '__qualname__': <attribute '__qualname__' of 'type' objects>, '__bases__': <attribute '__bases__' of 'type' objects>, '__module__': <attribute '__module__' of 'type' objects>, '__abstractmethods__': <attribute '__abstractmethods__' of 'type' objects>, '__dict__': <attribute '__dict__' of 'type' objects>, '__doc__': <attribute '__doc__' of 'type' objects>, '__text_signature__': <attribute '__text_signature__' of 'type' objects>}```
``` everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) :  ['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__dir__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__prepare__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__text_signature__', '__weakrefoffset__', 'mro']```

Wow, any class can tell all of its derived classes! I wonder how that works...

```Base.__subclasses__() :  [<class '__main__.Foo'>]```


PART II - OBJECT CREATION
=========================

Objects recap:
    The object instance holds the \_\_dict\_\_ attribute of the object instance, it's value is a dictionary that holds the object instance members.
    The class is an object that is shared between all object instances, and it holds the static data (class variables, class methods)

What happens upon: foo = Foo() ?

# take the type of Foo - the metaclass of Foo. (the metaclass knows how to create an instance of the class, and instances of the object)
class\_obj = Foo

# the metaclass is used as a 'callable' - it has a \_\_call\_\_ method, and can therefore be called as if it were a function
# now this \_\_call\_\_ method creates and initialises the object instance.
# the implementation of \_\_call\_\_ now does two steps:
#   - first it does a lookup for the Foo class, if the Foo class has already been created.
#     It creates the Foo class instance, if it does not yet exist, upon the first call.
#   - it uses the Foo class and calls its \_\_init\_\_ method, in order to create the instance of class Foo !!!
instance\_of\_foo = class\_obj.\_\_call\_\_()

# actually that was a bit of a simplification...


```
instance_of_foo <class '__main__.Foo'> at 0x7fe39ae2c640 fields: {
  'obj_var_a' : 42,
  'obj_var_b' : 'name',
  'obj_var_base' : 10
}
```
*** eof tutorial ***
