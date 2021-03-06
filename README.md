# Advanced course on Python3
This course covers several topics

- [Python decorators](https://github.com/MoserMichael/python-obj-system/blob/master/decorator.md) 
- [The python object system / meta classes](https://github.com/MoserMichael/python-obj-system/blob/master/python-obj-system.md) 
- [Iterators, generators and asyncio](https://github.com/MoserMichael/python-obj-system/blob/master/gen-iterator.md)
- Also see my text on [Python import system](https://github.com/MoserMichael/pythonimportplayground) /different repo/
- An introduction to the [Python bytecode](https://github.com/MoserMichael/pyasmtool/blob/master/bytecode_disasm.md) /different repo/
- [Writing a python tracer](https://github.com/MoserMichael/pyasmtool/blob/master/tracer.md) /different repo/ 

Each lesson is a python program, the output of that program is the rendered markdown text that makes up the lesson. This approach gives me some confidence about the quality of the material.

## mdpyformat literate programming library

I am using a kind of [literate programming tool](https://en.wikipedia.org/wiki/Literate_programming) developed for this course.
The tool is right here in this repository, in the [mdpyformat package](https://github.com/MoserMichael/python-obj-system/tree/master/mdpyformat)

The main function of the [mdpyformat package](https://github.com/MoserMichael/python-obj-system/tree/master/mdpyformat) is ```eval_and_quote(string_arg)```. This function does the following steps:
1. Renders the argument string as a code snippet
2. Evaluates the string argument as a python script, with the global variable context of the calling module
3. Renders the result of evaluating the code (both standard output and standard error)

There is also ```print_md(*args)``` - this shows the outut as a markdown regular text section

```header_md(line, nesting=1)``` - this renders the line as a header

```print_quoted(*args)``` - shows the aguments as markdown quoted text


### Installation of mdpyformat

The mdpyformat library can be installed via pip

```pip3 install mdpyformat```

Here is the [link to pypi](https://pypi.org/project/mdpyformat/)

### table of content generation script

The mdpyformat package contains a script for the generation of table of contents in the generated markdown files.

To invoke this script run

```python3 -m mdpyformat.tocgen MARKDOWN_INPUT_FILE MARKDOWN_OUTPUT_WITH_ADDED_TABLE_OF_CONTENT```

The script has beend derived from this [gist](https://gist.github.com/chriscasola/4700426) Thanks!
 
