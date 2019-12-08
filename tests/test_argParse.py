#!/usr/bin/env python3

from ccjtools import ccj_make

def test_createParser():
    parser = ccj_make.mkccj_create_parser('progname')
    assert True

def test_parseNoArgs():
    """If you don't provide one positional argument, parsing fails"""
    parsedArgs = None
    try:
        parsedArgs = ccj_make.mkccj_parse_args(['progname'])
    except:
        pass

    if parsedArgs:
        assert False

    assert True

def test_parseArgs():
    """provide one positional argument, succeeds"""
    input_file = 'foo.txt'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', input_file])
    if not parsedArgs:
        assert False

    if parsedArgs.input_file != input_file:
        assert False

    assert True

def test_parseOptionalArgs():
    """Check optional parameters"""
    input_file = 'foo.txt'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', '-e', 'compile_commands.json',  '-o', 'compile_commands.json', input_file])
    if not parsedArgs:
        assert False

    if parsedArgs.existing != 'compile_commands.json':
        assert False

    if parsedArgs.output != 'compile_commands.json':
        assert False

    assert True
