#!/usr/bin/env python3
"""
Take arbitrary compile output and produce a json compilation database
that clang-based tools will be happy with. Uses ad-hoc and naive heuristics,
but it works.

Copyright 2019 Nik Langrind.
SPDX-License-Identifier: MIT
"""

import argparse, sys, os, json, re

'''
See https://sarcasm.github.io/notes/dev/compilation-database.html for
a description of compilation databases.

Here is what a json compilation database looks like:

[
    {
       "directory" : "<absolute path of project>",
       "command"   : "<compile command in all its glory>",
       "file"      : "<absolute path of file being compiled>"
    },
    {
       "directory" : "<absolute path of project>",
       "command"   : "<compile command in all its glory>",
       "file"      : "<absolute path of file being compiled>"
    },
    ...
]

Nothing limits you to something quite as simple as that, but while working
with CCLS, rtags etc. and multiple clang revisions, I'm not sure which
programs have which limits. So I've made my model very simple.

What this program does is take build log file (a text file) that you got by
however you got it.  It could be from an Eclipse build log, from a script
session, whatever, but it is basically all the commands your make
produced. For each line that looks like a compile command, this program
creates a single record with the three fields (directory, command and file.)

The "directory" member is the same for each record. It comes from a command
line option, or from $PWD.

The "command" comes from looking for lines whose first word appears to be a
compiler. There is a command line option to provide an exact match string if
needed.

The "file" is assumed to be the last word on the line that was identified as a
command.

Heuristics are naive, and presumably will evolve to be more sophisticated,
and also to be governable via user options

Implementation-wise, each such record is a dictionary. As the file is
read, a list of these is build up.  In parallel, a crossRef dictionary
is populated, keyed by "file".

At the end of the run, the compilation database is produced by emitted
the list to the file "compile_commands.json", or a name that you
provide via the -o command line switch.

An existing json file can be provided via the -e command line
option. It is used to prepopulate the internal list. The cross
reference dictionary is used to avoid duplicates in the list. (Should
add the ability to preserve existing entries or modify them. Currently
we only modify them.)

This program is not cautious about overwriting the existing
compile_commands.json.
'''

def mkccj_create_parser(prog):
    """Set up the command line arguments parser, but don't parse"""
    parser = argparse.ArgumentParser(prog=prog, description="Produce a JSON format compilation database from a text build log")

    parser.add_argument('input_file',          help='Input text filename')
    parser.add_argument('-c', dest='compiler', help='name of compiler, used to recognize compile lines in input' )
    parser.add_argument('-e', dest='existing', help='Existing json file to augment' )
    parser.add_argument('-o', dest='output',   help='name of json file to emit', default='compile_commands.json' )
    parser.add_argument('-p', dest='project',  help='project directory, defaults to PWD', default=os.getcwd() )
    parser.add_argument('-r', dest='rename',   help='replace compiler with this indexer-friendly compiler name in output json' )

    return parser

def mkccj_parse_args(args):
    """Create command line arguments parser and run it on provided input"""
    parser = mkccj_create_parser(args[0])
    parsedArgs = parser.parse_args(args[1:])
    return parsedArgs

def mkccj_is_compiler_command(parsedArgs, commandString):
    """Return True if the commandString is or appears to name a compiler"""
    if parsedArgs.compiler:
        if parsedArgs.compiler == commandString:
            return True
        else:
            return False

    if re.search(r"cc$", commandString):
        return True

    if re.search(r"[cg]\+\+$", commandString):
        return True

    return False

def mkccj_process_line( parsedArgs, crossRefDict, outputList, line ):
    """Process one line. If it appears to be a compile command, proceed accordingly"""

    # Need to make these replacements (and many others) optional
    # These are sufficient and appropriate for MCUXpresso output I am using as a test case
    # I know they won't be sufficient and appropriate for other cases
    conditionedLine = line.replace('"', '')
    conditionedLine = conditionedLine.replace('../', '')

    words = conditionedLine.split()
    if not words or not mkccj_is_compiler_command(parsedArgs, words[0]):
        return False

    # We have a line that appears to be a compilation command

    # source filename is probably the last word on the line, we are going to produce
    # garbage if it isn't.
    sourceFilename = words[-1]

    # filter out linker commands
    if re.search(r"\.o$", sourceFilename):
        return False

    # substitute the compile name if we were told to
    if parsedArgs.rename:
        words[0] = parsedArgs.rename

    # if not sourceFilename.startswith(parsedArgs.project):
    #     xxx not sure I need to worry about prepending the project path
    
    # Form or update the output record
    try:
        record = crossRefDict.get(sourceFilename)
        record.update({'directory' : parsedArgs.project})
        record.update({'command'   : ' '.join(words)})
        record.update({'file'      : sourceFilename})
            
    except:
        record = {
            'directory' : parsedArgs.project,
            'command'   : ' '.join(words),
            'file'      : sourceFilename
        }

        # Store the output record
        outputList.append(record)
        crossRefDict[sourceFilename] = record

    return True
    
def mkccj_read_existing_json(parsedArgs):
    """Convert the exising json file to list and crossRefDict"""

    crossRefDict = {}
    outputList = []
    if parsedArgs.existing:
        existingFile = parsedArgs.existing
        with open(existingFile) as jsonFile:
            outputList = json.load(jsonFile)
            crossRefDict = {record['file'] : record for record in outputList }

    return outputList, crossRefDict

def mkccj_convert_input_file(parsedArgs):
    """Convert the input file to a dictionary, return the dictionary"""

    outputList, crossRefDict = mkccj_read_existing_json(parsedArgs)

    with open(parsedArgs.input_file) as buildFile:
        for count, line in enumerate(buildFile):
            mkccj_process_line( parsedArgs, crossRefDict, outputList, line )

    return outputList, crossRefDict

def main(argv):
    parsedArgs = mkccj_parse_args(argv)
    outputList,crossRefDict = mkccj_convert_input_file(parsedArgs)
    with open(parsedArgs.output, "w") as outfile:
        print(json.dumps(outputList, indent=2), file=outfile)

if __name__ == '__main__':
    main(sys.argv)

