# a Python object primer

Python is good at creating the illusion of being a simple programming language. Sometimes this illusion fails, like when you have to deal with the import/module system  [my attempts to get it](https://github.com/MoserMichael/pythonimportplayground). Another area of complexity is the object system, last week I tried to understand how [python enums](https://docs.python.org/3/library/enum.html), it turns that they are built on top of [meta objects](https://github.com/python/cpython/blob/2c56c97f015a7ea81719615ddcf3c745fba5b4f3/Lib/enum.py#L511), So now I have come to realize, that I really don't know much about python and its object system, after having failed to understand meta objects. The purpose of this text is to figure out, how the python object system ticks.

## an object in memory.

Let's create a simple object: a class ```Foo``` with a base class ```Base```, both class and base class have a few object variables (these are specific to an object instance) and class variables (shared between all object instances) (note that this is a very simple case, without complications like multiple inheritance)

(as a first aproximation: look at the file tut.md here, this is the output of the tut.py program)
