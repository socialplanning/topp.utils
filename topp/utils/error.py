import sys

def error(msg, parser=None, warning=False):
    """
    print an error message.
    in the future, this should log
    """

    if warning:
        err_string = "WARNING"
    else:
        err_string = "ERROR"
    print err_string + ":", msg
    if parser:
        parser.print_usage()
    if not warning:
        sys.exit(1)
