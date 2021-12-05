# Advanced course on Python

This course covers several topics

- [Python decorators](https://github.com/MoserMichael/python-obj-system/blob/master/decorator.md) 
- [The python object system / meta classes](https://github.com/MoserMichael/python-obj-system/blob/master/python-obj-system.md) 
- Also see my text on [Python import system](https://github.com/MoserMichael/pythonimportplayground)

Each lesson is a python program, the output of that program is the rendered markdown text that makes up the lesson. This approach gives me some confidence about the quality of the material.

I am using a kind of [literate programming tool](https://en.wikipedia.org/wiki/Literate_programming) developed for this course.
The tool is right here in this repository, in the [mdformat package](https://github.com/MoserMichael/python-obj-system/tree/master/mdformat)

The main function of the [mdformat package](https://github.com/MoserMichael/python-obj-system/tree/master/mdformat) is ```eval_and_quote(string_arg)```. This function does the following steps:
1. Renders the argument string as a code snippet
2. Evaluates the string argument as a python script, with the global variable context of the calling module
3. Renders the result of evaluating the code (both standard output and standard error)

There is also ```print_md(*args)``` - this shows the outut as a markdown regular text section

```header_md(line, nesting=1)``` - this renders the line as a header

```print_quoted(*args)``` - shows the aguments as markdown quoted text

