# a Python object primer

Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand how [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta objects](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system, after having failed to understand meta objects. The purpose of this text is to figure out, how the python object system ticks.

## an object in memory.

Let's create a simple object: a class ```Foo``` with a base class ```Base```, both class and base class have a few object variables (these are specific to an object instance) and class variables (shared between all object instances) (note that this is a very simple case, without complications like multiple inheritance)


```

# the base class. All python classes have the base class object.
# the long form is therefore
# class Base(object):

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


    @staticmethod
    def make_foo():
        return Foo()


# make a new object instance of type Foo class.
foo_obj=Foo()

```





