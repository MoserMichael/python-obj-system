# Advanced course on python

This course covers several topics

- [The python object system](https://github.com/MoserMichael/python-obj-system/blob/master/python-obj-system.md) 
- [Python decorators](https://github.com/MoserMichael/python-obj-system/blob/master/decorator.md) 

The lessons are python files, these are run to create the markdown text for the lesson.
It uses a kind of [literate programming tool](https://en.wikipedia.org/wiki/Literate_programming) developed for this course, which formats the output of the script in markdown format.
The tool is here in this repository, in the [mdformat package](https://github.com/MoserMichael/python-obj-system/tree/master/mdformat)

The main function in this package is ```eval_and_quote(string_arg)``` this function 
1. Renders the argument string as a code snippet
2. Evaluates the string argument as a python script, with the global variable context of the calling module
3. Renders the result of evaluating the code (both standard output and standard error)

There is also ```print_md(*args)``` - this shows the outut as a markdown regular text section

```header_md(line, nesting=1)``` - this renders the line as a header

```print_quoted(*args)``` - shows the aguments as markdown quoted text

