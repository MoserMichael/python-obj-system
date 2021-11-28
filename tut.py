#!/usr/bin/env python3
import sys
from io import StringIO
import inspect
import pprintex
import contextlib

# stuff for producing this tutorial.
def print_md(*args):
    print(" ".join(map(str, args)).replace('_', "\\_") )
def print_quoted(*args):
    print("```\n" +  ' '.join(map(str, args)) + "\n```" )
def eval_and_quote(arg_str):
    print("")

    print_quoted(arg_str)

    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
     
    with stdoutIO() as sout:
        exec(arg_str, globals())
    
    sline = sout.getvalue().strip()
    if sline != "":
        print("")
        print_quoted( '\n'.join( map( lambda line : ">> " + line, sline.split("\n") ) ) )
        print("")

def quote():
    print_md("```")

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


print("""
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

""")

print_md("Memory address where object foo_obj is stored is returned by the [id built-in](https://docs.python.org/3/library/functions.html#id)")

eval_and_quote('print("id(foo_obj) : ", id(foo_obj))')

print_md("If two variables have the same object id value, then they both refer to the very same object/instance!")

print_md("""
each user defined object has a __dict__ attribute, this is a dictionary that lists all the object instance variable.
This also includes instance members that were added by the __init__ method of the base class !!
""")

eval_and_quote("""print("foo_obj.__dict__ : ", foo_obj.__dict__)""")

#eval_and_quote("""printex.dprint("foo instance", foo_obj)""")

print_md("")

print_md("""
Wait, but where does the __dict__ attribute come from?
The [built-in getattr](https://docs.python.org/3/library/functions.html#getattr) function can return this built-in __dict__ attribute!
Interesting: the python notation object.member_name can mean different things:
  1) for built-in attributes it means a call to getattr
  2) for object instances (assigned in the __init__ method of the class) it means a call to retrieve the __dict__ attribute, and then a lookup of the variable name in that dictionary.
""")

eval_and_quote("""print("foo_obj.__dict__ and getattr(foo_obj,'__dict__',None) is the same thing!") """)

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
it does different things, depending on the argument,
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

eval_and_quote( """print("foo_obj.__class__ and getattr(foo_obj,'__class__',None) is the same thing!") """)
eval_and_quote( """assert id(foo_obj.__class__) == id( getattr(foo_obj,'__class__',None) ) """)

print_md(""" the __name__ and __qualname__ built-in attributes return the name of the class, without the module name """)

eval_and_quote( """print("foo_boj.__class__.__name__ : ", foo_obj.__class__.__name__)""" )
eval_and_quote( """print("foo_boj.__class__.__qualname__ : ", foo_obj.__class__.__qualname__)""" )


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
the dir method for a class:
Again, this built-in dir function does different things, depending on the argument type
for a class object it returns a "list that contains the names of its attributes, and recursively of the attributes of its bases"
Note that the names are sorted.
""")


eval_and_quote("""print("dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )""")

print_md("""
The class object derives from built-in class type, you can chekck if an object is a type by checking if it is an instance of type !
""")

# check that foo_obj.__class__ is a type - it is derived from built-in class type
eval_and_quote("""assert isinstance(foo_obj.__class__, type)""")
eval_and_quote("""assert inspect.isclass(foo_obj.__class__)""")

print_md( """
Now there is much more. there is the inspect module that returns it all, a kind of rosetta stone of the python object model.
inspect.getmembers returns everything! You can see the source of inspect.getmembers here: https://github.com/python/cpython/blob/3.10/Lib/inspect.py
""")

eval_and_quote("""print("inspect.getmembers(foo_obj): ", inspect.getmembers(foo_obj))""")


print_md("""
Attention!
the type of the object is the Class of the object (remember: the classes is an object, where the __dict__ member holds the class variables)
""")

eval_and_quote("""print("type(foo_obj) : ", type(foo_obj))""")
eval_and_quote("""print("str(foo_obj.__class__) : ", str(foo_obj.__class__) )""")

print_md("""

Let's look at both the type and identity of all these objects:

""")

eval_and_quote("""print("id(foo_obj) : ", id(foo_obj), " str(foo_obj) : ", str(foo_obj))""")

print_md("""
The following expressions refer to the same thing: the type of the object foo_obj, also known as the class of foo_obj
""")

eval_and_quote("""print("type(foo_obj) : ", type(foo_obj), " id(type(foo_obj)) : ", id(type(foo_obj)), " type(foo_obj).__name__ : ", type(foo_obj).__name__ )""")
eval_and_quote("""print("str(foo_obj.__class__) : ", str(foo_obj.__class__), " id(foo_obj.__class__) : ", id(foo_obj.__class__), "foo_obj.__class__.__name__ : ", foo_obj.__class__.__name__)""")
eval_and_quote("""print("str(Foo) : ", str(Foo), " id(Foo) : ", id( Foo ), "Foo.__name__ : ", Foo.__name__)""")

eval_and_quote("""assert id(Foo) == id(type(foo_obj))""")
eval_and_quote("""assert id(type(foo_obj)) == id(foo_obj.__class__)""")


print_md("""
    The Foo class members
""")

eval_and_quote("""print(" foo_obj.__class__.__dict__ : ", foo_obj.__class__.__dict__)""")
eval_and_quote("""print(" Foo.__dict__ : ", Foo.__dict__)""")

eval_and_quote("""print(" dir(foo_obj.__class__) : ", dir( foo_obj.__class__ ) )""")



print_md("""
The following expressions refer to the same thing: the meta-type of the foo_obj.
""")


eval_and_quote("""print("type(foo_obj.__class__.__class__) : ", type(foo_obj.__class__.__class__), " id( foo_obj.__class__.__class__ ) : " , id( foo_obj.__class__.__class__ ) , "foo_obj.__class__.__class__.__name__ : ", foo_obj.__class__.__class__.__name__ )""")
eval_and_quote("""print("type(Foo) : ", type(Foo), " id(type(Foo)) : ", id( type( Foo ) ), " Foo.__class__.__name__ : ", Foo.__class__.__name__)""")
eval_and_quote("""print("type(Foo.__class__) : ", type(Foo.__class__), " id(type(Foo.__class__)) : ", id( type( Foo.__class__ ) ), " Foo.__class__.__name__ : ", Foo.__class__.__name__)""")
eval_and_quote("""print("type(Foo.__class__.__class__) ", type(Foo.__class__.__class__), " id(type(Foo.__class__.__class__)) : ", id( type( Foo.__class__.__class__ ) ) )""")

eval_and_quote("""assert type(Foo) == type(Foo.__class__)""")
eval_and_quote("""assert type(Foo.__class__) == type(Foo.__class__.__class__)""")


print_md("""
The type of the type is the metaclass - the metaclass constructs the Class object! (the class of an object is also an object!)
""")

eval_and_quote("""print("type( type( foo_obj ) ) : ", type( type( foo_obj ) ) )""")
eval_and_quote("""print("str( foo_obj.__class__.__class__ ) : ", str(foo_obj.__class__.__class__) )""")


# result:

eval_and_quote("""print(" metaclass members: foo_obj.__class__.__class__.__dict__ : ", foo_obj.__class__.__class__.__dict__)""")

eval_and_quote("""print(" everything accessible form metaclass: dir( foo_obj.__class__.__class__ ) : ", dir( foo_obj.__class__.__class__) )""")

print_md("""
Wow, any class can tell all of its derived classes! I wonder how that works...
""")

eval_and_quote("""print("Base.__subclasses__() : ", Base.__subclasses__())""")


print_md("""

PART II - OBJECT CREATION
=========================

Objects recap:
    The object instance holds the __dict__ attribute of the object instance, it's value is a dictionary that holds the object instance members.
    The class is an object that is shared between all object instances, and it holds the static data (class variables, class methods)

What happens upon: foo = Foo() ?

take the type of Foo - the metaclass of Foo. (the metaclass knows how to create an instance of the class, and instances of the object)
    class_obj = Foo

The metaclass is used as a 'callable' - it has a __call__ method, and can therefore be called as if it were a function
Now this __call__ method creates and initialises the object instance.
The implementation of __call__ now does two steps:
   - first it does a lookup for the Foo class, if the Foo class has already been created.
     It creates the Foo class instance, if it does not yet exist, upon the first call.
   - it uses the Foo class and calls its __init__ method, in order to create the instance of class Foo !!!
     instance_of_foo = class_obj.__call__()

actually that was a bit of a simplification...

""")

eval_and_quote("""foo_obj = Foo.__call__()""")

eval_and_quote("""class_obj = Foo
instance_of_foo = class_obj.__call__()
print('instance_of_foo', instance_of_foo.__dict__)""")

print_md("*** eof tutorial ***")
