import sys
import re
from io import StringIO
import inspect
import contextlib

# show argument string as markdown header.
def header_md(line, nesting=1):
    print( "\n" + ('#' * nesting) + line  + "\n")

# show text as a paragraph, as part of markdown file. 
#   quotes underscores
#   removes leading spaces
#
def print_md(*args):
    paragraph = " ".join(map(str, args)) 
    paragrah =  paragraph.replace('_', "\\_") 
    paragraph = re.sub(r"^\s+","", paragraph)
    print( )

# show arguments as quoted text
def print_quoted(*args):
    print("```\n" +  ' '.join(map(str, args)) + "\n```" )

# evaluate the argument string, show the source and show the results
def eval_and_quote(arg_str):
    print("")

    print_quoted(arg_str)

    @contextlib.contextmanager
    def stderrIO(stderr=None):
        old = sys.stderr
        if stderr is None:
            stderr = StringIO()
        sys.stderr = stderr
        yield stderr
        sys.stderr = old

    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    def format_result(out):
        sline = out.getvalue().strip()
        if sline != "":
            print("")
            print_quoted( '\n'.join( map( lambda line : ">> " + line, sline.split("\n") ) ) )
            print("")

    frame = inspect.currentframe()

    # get globals from calling frame...
    calling_frame_globals = frame.f_back.f_globals

    with stderrIO() as serr:
        with stdoutIO() as sout:
            exec(arg_str, calling_frame_globals)

    format_result(sout)
    format_result(serr)

