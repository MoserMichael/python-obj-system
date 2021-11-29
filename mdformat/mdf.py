import sys
from io import StringIO
import inspect
import contextlib

# show text as part of markdown file. (quote underscores)
def print_md(*args):
    print(" ".join(map(str, args)).replace('_', "\\_") )

# show stuff as quoted text
def print_quoted(*args):
    print("```\n" +  ' '.join(map(str, args)) + "\n```" )

# evaluate the argument string, show the source and show the results
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

    frame = inspect.currentframe()

    # get globals from calling frame...
    calling_frame_globals = frame.f_back.f_globals
     
    with stdoutIO() as sout:
        exec(arg_str, calling_frame_globals)
    
    sline = sout.getvalue().strip()
    if sline != "":
        print("")
        print_quoted( '\n'.join( map( lambda line : ">> " + line, sline.split("\n") ) ) )
        print("")


