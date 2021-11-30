" Set text width as 72.


# Python object primer for python3

Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand how [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta classes](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system, after having failed to understand meta classes. The purpose of this text is to figure out, how the python object system ticks.

Lets look at a simple python class Foo with a single base class, and see how objects are created and represented in memory


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
        # object variables are specific to a given instance of Base
        # each object has a builtin hash member: __dict__ this one lists all object members (including those added by the base class __init__ method)
        self.obj_var_base = 10

    # an object method - needs an object instance, which is passed as first 'self' argument.
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
        print_md("obj_var_a:", self.obj_var_a, "obj_var_b:", self.obj_var_b)

    # a class method/static method is called without an object instance.
    @staticmethod
    def make_foo():
        return Foo()

# make a new object instance of type Foo class.
foo_obj=Foo()


```


```
print("id(foo_obj) : ", id(foo_obj))
```

```
>> id(foo_obj) :  140427771374560
```




```
print("foo_obj.__dict__ : ", foo_obj.__dict__)
```

```
>> foo_obj.__dict__ :  {'obj_var_a': 42, 'obj_var_b': 'name', 'obj_var_base': 10}
```



```
assert id(foo_obj.obj_var_a) == id( foo_obj.__dict__['obj_var_a'] ) 
```



```
assert id(foo_obj.__dict__) == id( getattr(foo_obj,'__dict__',None) )
```


```
base_obj = object()
```


```
assert getattr(base_obj, '__dict__', None) is None
```

```
int_obj = 42
```


```
assert getattr(int_obj, '__dict__', None) is None
```


```
print("dir(foo_obj) : ", dir(foo_obj))
```

```
>> dir(foo_obj) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'obj_var_a', 'obj_var_b', 'obj_var_base', 'show_base', 'show_derived']
```



```
print("foo_obj.__class__ :", foo_obj.__class__)
```

```
>> foo_obj.__class__ : <class '__main__.Foo'>
```


```
print("type(foo_obj) :", type(foo_obj) )
```

```
>> type(foo_obj) : <class '__main__.Foo'>
```



```
print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!") 
```

```
>> foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!
```


```
assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) ) 
```


```
print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)
```

```
>> foo_boj.__class__.__name__ :  Foo
```


```
print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)
```

```
>> foo_boj.__class__.__qualname__ :  Foo
```



```
print("foo_obj.__class__.__bases__ :", foo_obj.__class__.__bases__)
```

```
>> foo_obj.__class__.__bases__ : (<class '__main__.Base'>,)
```



```
print("foo_obj.__class__.__mro__ :", foo_obj.__class__.__mro__) 
```

```
>> foo_obj.__class__.__mro__ : (<class '__main__.Foo'>, <class '__main__.Base'>, <class 'object'>)
```


```

print("*** mro in detail:")
for cls in foo_obj.__class__.__mro__:
    print_md("	class-in-mro: ", str(cls), "id:", id(cls), "dir(cls): ", dir(cls))
print("*** eof mro in detail")

```

```
>> *** mro in detail:
>> 
>> 
>> 
>> *** eof mro in detail
```



```
print("foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)
```

```
>> foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fb7e36dc430>, 'show_derived': <function Foo.show_derived at 0x7fb7e36dc4c0>, 'make_foo': <staticmethod object at 0x7fb7e36dedf0>, '__doc__': None}
```



```
print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )
```

```
>> dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
```



```
assert isinstance(foo_obj.__class__, type)
```

```
assert inspect.isclass(foo_obj.__class__)
```


```
print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))
```

```
>> inspect.getmembers(foo_obj):  [('__class__', <class '__main__.Foo'>), ('__delattr__', <method-wrapper '__delattr__' of Foo object at 0x7fb7e36debe0>), ('__dict__', {'obj_var_a': 42, 'obj_var_b': 'name', 'obj_var_base': 10}), ('__dir__', <built-in method __dir__ of Foo object at 0x7fb7e36debe0>), ('__doc__', None), ('__eq__', <method-wrapper '__eq__' of Foo object at 0x7fb7e36debe0>), ('__format__', <built-in method __format__ of Foo object at 0x7fb7e36debe0>), ('__ge__', <method-wrapper '__ge__' of Foo object at 0x7fb7e36debe0>), ('__getattribute__', <method-wrapper '__getattribute__' of Foo object at 0x7fb7e36debe0>), ('__gt__', <method-wrapper '__gt__' of Foo object at 0x7fb7e36debe0>), ('__hash__', <method-wrapper '__hash__' of Foo object at 0x7fb7e36debe0>), ('__init__', <bound method Foo.__init__ of <__main__.Foo object at 0x7fb7e36debe0>>), ('__init_subclass__', <built-in method __init_subclass__ of type object at 0x7fb7e3540570>), ('__le__', <method-wrapper '__le__' of Foo object at 0x7fb7e36debe0>), ('__lt__', <method-wrapper '__lt__' of Foo object at 0x7fb7e36debe0>), ('__module__', '__main__'), ('__ne__', <method-wrapper '__ne__' of Foo object at 0x7fb7e36debe0>), ('__new__', <built-in method __new__ of type object at 0x1101a7bb0>), ('__reduce__', <built-in method __reduce__ of Foo object at 0x7fb7e36debe0>), ('__reduce_ex__', <built-in method __reduce_ex__ of Foo object at 0x7fb7e36debe0>), ('__repr__', <method-wrapper '__repr__' of Foo object at 0x7fb7e36debe0>), ('__setattr__', <method-wrapper '__setattr__' of Foo object at 0x7fb7e36debe0>), ('__sizeof__', <built-in method __sizeof__ of Foo object at 0x7fb7e36debe0>), ('__str__', <method-wrapper '__str__' of Foo object at 0x7fb7e36debe0>), ('__subclasshook__', <built-in method __subclasshook__ of type object at 0x7fb7e3540570>), ('__weakref__', None), ('base_clas_var', 'Base'), ('class_var', 42), ('class_var2', 43), ('make_base', <function Base.make_base at 0x7fb7e36dc3a0>), ('make_foo', <function Foo.make_foo at 0x7fb7e36dc550>), ('obj_var_a', 42), ('obj_var_b', 'name'), ('obj_var_base', 10), ('show_base', <bound method Base.show_base of <__main__.Foo object at 0x7fb7e36debe0>>), ('show_derived', <bound method Foo.show_derived of <__main__.Foo object at 0x7fb7e36debe0>>)]
```



```
print("type(foo_obj) : ", type(foo_obj))
```

```
>> type(foo_obj) :  <class '__main__.Foo'>
```


```
print("str(foo_obj.__class__) : ", str(foo_obj.__class__) )
```

```
>> str(foo_obj.__class__) :  <class '__main__.Foo'>
```



```
print("id(foo_obj) : ", id(foo_obj), " str(foo_obj) : ", str(foo_obj))
```

```
>> id(foo_obj) :  140427771374560  str(foo_obj) :  <__main__.Foo object at 0x7fb7e36debe0>
```



```
print("type(foo_obj) : ", type(foo_obj), " id(type(foo_obj)) : ", id(type(foo_obj)), " type(foo_obj).__name__ : ", type(foo_obj).__name__ )
```

```
>> type(foo_obj) :  <class '__main__.Foo'>  id(type(foo_obj)) :  140427769677168  type(foo_obj).__name__ :  Foo
```


```
print("str(foo_obj.__class__) : ", str(foo_obj.__class__), " id(foo_obj.__class__) : ", id(foo_obj.__class__), "foo_obj.__class__.__name__ : ", foo_obj.__class__.__name__)
```

```
>> str(foo_obj.__class__) :  <class '__main__.Foo'>  id(foo_obj.__class__) :  140427769677168 foo_obj.__class__.__name__ :  Foo
```


```
print("str(Foo) : ", str(Foo), " id(Foo) : ", id( Foo ), "Foo.__name__ : ", Foo.__name__)
```

```
>> str(Foo) :  <class '__main__.Foo'>  id(Foo) :  140427769677168 Foo.__name__ :  Foo
```


```
assert id(Foo) == id(type(foo_obj))
```

```
assert id(type(foo_obj)) == id(foo_obj.__class__)
```


```
print(" foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)
```

```
>> foo_obj.__class__.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fb7e36dc430>, 'show_derived': <function Foo.show_derived at 0x7fb7e36dc4c0>, 'make_foo': <staticmethod object at 0x7fb7e36dedf0>, '__doc__': None}
```


```
print(" Foo.__dict__ : ", Foo.__dict__)
```

```
>> Foo.__dict__ :  {'__module__': '__main__', 'class_var': 42, 'class_var2': 43, '__init__': <function Foo.__init__ at 0x7fb7e36dc430>, 'show_derived': <function Foo.show_derived at 0x7fb7e36dc4c0>, 'make_foo': <staticmethod object at 0x7fb7e36dedf0>, '__doc__': None}
```


```
print(" dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )
```

```
>> dir(foo_obj.__class__) :  ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'base_clas_var', 'class_var', 'class_var2', 'make_base', 'make_foo', 'show_base', 'show_derived']
```



```
print("type(foo_obj.__class__.__class__) : ", type(foo_obj.__class__.__class__), " id( foo_obj.__class__.__class__ ) : " , id( foo_obj.__class__.__class__ ) , "foo_obj.__class__.__class__.__name__ : ", foo_obj.__class__.__class__.__name__ )
```

```
>> type(foo_obj.__class__.__class__) :  <class 'type'>  id( foo_obj.__class__.__class__ ) :  4565138760 foo_obj.__class__.__class__.__name__ :  type
```


```
print("type(Foo) : ", type(Foo), " id(type(Foo)) : ", id( type( Foo ) ), " Foo.__class__.__name__ : ", Foo.__class__.__name__)
```

```
>> type(Foo) :  <class 'type'>  id(type(Foo)) :  4565138760  Foo.__class__.__name__ :  type
```


```
print("type(Foo.__class__) : ", type(Foo.__class__), " id(type(Foo.__class__)) : ", id( type( Foo.__class__ ) ), " Foo.__class__.__name__ : ", Foo.__class__.__name__)
```

```
>> type(Foo.__class__) :  <class 'type'>  id(type(Foo.__class__)) :  4565138760  Foo.__class__.__name__ :  type
```


```
print("type(Foo.__class__.__class__) ", type(Foo.__class__.__class__), " id(type(Foo.__class__.__class__)) : ", id( type( Foo.__class__.__class__ ) ) )
```

```
>> type(Foo.__class__.__class__)  <class 'type'>  id(type(Foo.__class__.__class__)) :  4565138760
```


```
assert type(Foo) == type(Foo.__class__)
```

```
assert type(Foo.__class__) == type(Foo.__class__.__class__)
```


```
print("type( type( foo_obj ) ) : ", type( type( foo_obj ) ) )
```

```
>> type( type( foo_obj ) ) :  <class 'type'>
```


```
print("str( foo_obj.__class__.__class__ ) : ", str(foo_obj.__class__.__class__) )
```

```
>> str( foo_obj.__class__.__class__ ) :  <class 'type'>
```


```
print(" metaclass members: foo_obj.__class__.__class__.__dict__ : ", foo_obj.__class__.__class__.__dict__)
```

```
>> metaclass members: foo_obj.__class__.__class__.__dict__ :  {'__repr__': <slot wrapper '__repr__' of 'type' objects>, '__call__': <slot wrapper '__call__' of 'type' objects>, '__getattribute__': <slot wrapper '__getattribute__' of 'type' objects>, '__setattr__': <slot wrapper '__setattr__' of 'type' objects>, '__delattr__': <slot wrapper '__delattr__' of 'type' objects>, '__init__': <slot wrapper '__init__' of 'type' objects>, '__new__': <built-in method __new__ of type object at 0x1101a7d48>, 'mro': <method 'mro' of 'type' objects>, '__subclasses__': <method '__subclasses__' of 'type' objects>, '__prepare__': <method '__prepare__' of 'type' objects>, '__instancecheck__': <method '__instancecheck__' of 'type' objects>, '__subclasscheck__': <method '__subclasscheck__' of 'type' objects>, '__dir__': <method '__dir__' of 'type' objects>, '__sizeof__': <method '__sizeof__' of 'type' objects>, '__basicsize__': <member '__basicsize__' of 'type' objects>, '__itemsize__': <member '__itemsize__' of 'type' objects>, '__flags__': <member '__flags__' of 'type' objects>, '__weakrefoffset__': <member '__weakrefoffset__' of 'type' objects>, '__base__': <member '__base__' of 'type' objects>, '__dictoffset__': <member '__dictoffset__' of 'type' objects>, '__mro__': <member '__mro__' of 'type' objects>, '__name__': <attribute '__name__' of 'type' objects>, '__qualname__': <attribute '__qualname__' of 'type' objects>, '__bases__': <attribute '__bases__' of 'type' objects>, '__module__': <attribute '__module__' of 'type' objects>, '__abstractmethods__': <attribute '__abstractmethods__' of 'type' objects>, '__dict__': <attribute '__dict__' of 'type' objects>, '__doc__': <attribute '__doc__' of 'type' objects>, '__text_signature__': <attribute '__text_signature__' of 'type' objects>}
```


```
print(" everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) : ", dir( foo_obj.__class__.__class__) )
```

```
>> everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) :  ['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__dir__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__prepare__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__text_signature__', '__weakrefoffset__', 'mro']
```



```
print("Base.__subclasses__() : ", Base.__subclasses__())
```

```
>> Base.__subclasses__() :  [<class '__main__.Foo'>]
```



```
foo_obj = Foo.__call__()
```

```
class_obj = Foo
instance_of_foo = class_obj.__call__()
print('instance_of_foo', instance_of_foo.__dict__)
pprintex.dprint('instance_of_foo', instance_of_foo)
```
