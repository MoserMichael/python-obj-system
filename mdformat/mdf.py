import sys
import re
from io import StringIO
import inspect
import traceback
import contextlib

def header_md(line, nesting=1):
    """ show argument string as markdown header. Nesting of level is set by nesting argument """
    print( "\n" + ('#' * nesting) + " " + line  + "\n")


def print_md(*args):
    """show text as a paragraph, as part of markdown file, quotes underscores, removes leading spaces"""
    paragraph = " ".join(map(str, args))
    paragraph =  paragraph.replace('_', "\\_") #.replace('#','\\#')
    paragraph = re.sub(r"^\s+","", paragraph)
    print(paragraph)

def print_quoted(*args):
    """show arguments as quoted text in markdown"""
    print("```\n" +  ' '.join(map(str, args)) + "\n```" )

def eval_and_quote(arg_str):
    """evaluate the argument string, show the source and show the results"""
    print("")
    print("__Source:__")

    print_quoted(arg_str)

    @contextlib.contextmanager
    def stderr_io(stderr=None):
        old = sys.stderr
        if stderr is None:
            stderr = StringIO()
        sys.stderr = stderr
        yield stderr
        sys.stderr = old

    @contextlib.contextmanager
    def stdout_io(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    def format_result(out, is_first):
        sline = out.getvalue().strip()
        if sline != "":
            print("")
            if is_first:
                print("__Result:__")
                is_first = False
            print_quoted( '\n'.join( map( lambda line : ">> " + line, sline.split("\n") ) ) )
            print("")
        return is_first

    # from walk_tb in https://github.com/python/cpython/blob/f6648e229edf07a1e4897244d7d34989dd9ea647/Lib/traceback.py#L93
    # don't know if that might break in the future
    def show_custom_trace(code, ex):
        code_lines = arg_str.split("\n")

        te = traceback.TracebackException.from_exception(ex)
        first_frame = True
        for frame_summary in te.stack:
            if not first_frame:
                lineno = frame_summary.lineno
                error_line = ""
                if len(code_lines) > lineno -1:
                    error_line = code_lines[ lineno-1 ]
                print(f"{frame_summary.name}")
                print(f"\t{lineno}) {error_line}") 
            first_frame = False

    frame = inspect.currentframe()

    # get globals from calling frame...
    calling_frame_globals = frame.f_back.f_globals
    has_error = False
    with stderr_io() as serr:
        with stdout_io() as sout:
            exc = None

            try:
                exec(arg_str, calling_frame_globals)
            except SyntaxError as err:
                # get error line
                error_line = ""
                code_lines = arg_str.split("\n")
                if len(code_lines) > err.lineno -1:
                    error_line = code_lines[ err.lineno-1 ]
                print("syntax error: ", err, "\n" + str(err.lineno-1) + ")", error_line)
                has_error = True
            except Exception as err:
                print("Error in code. exception:", err)
                exc = err
                has_error = True

            if exc is not None:
                # this doesn't show the line that caused the exception
                #traceback.print_exc()
                show_custom_trace(arg_str, exc)
                        

    is_first = True
    is_first = format_result(sout, is_first)
    format_result(serr, is_first)
    if has_error:
        print("Error during evalutation of the preceeding code snippet, see standard output for more details.", file=sys.stderr) 
        sys.exit(1)
