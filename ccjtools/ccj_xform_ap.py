#!/usr/bin/env python3
"""
Transform compile_commands.json taken from an ArduPilot, by making it
appear as if the build was performed in the root, minimizing the
significance of the build/<config> directory.This makes ccls and lsp
work more smoothly.

From the top of an ardupilot dir, after it's been built:

$ xap_ccj -f build/CubeBlack/compile_commands.json

will produce ./compile_commands.json, which can be used by the
rtags command:

$ rc --project-root=$PWD -J .

"""
import argparse, sys, os, json, re

def xform_file(root, buildsub, filename):
    """
    Try to find the absolute path of filename by replacing buildsub with root,
    or ../.. with root. If the resulting filename is an actual file, return the
    new filename. Otherwise, return the original
    """
    newFilename = filename.replace(buildsub, root)
    if os.path.exists(newFilename):
        return newFilename
    
    newFilename = filename.replace("../..", root)
    if os.path.exists(newFilename):
        return newFilename
    
    return filename

def split_build_dir(args):
    cwd = os.getcwd()
    prefix = args.input_file.split('compile_commands.json')[0]
    return cwd, prefix

def make_command_from_arguments(arguments, root, buildsub):
    """turn the 'arguments' member (a list) of the json into 'command' (a string)"""
    
    # hack to make rtags happy - it won't accept that
    # /opt/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-g++.exe is
    # a compiler:
    if re.match("gcc$", arguments[0]):
        command = "/usr/bin/gcc.exe"
    else:
        command = "/usr/bin/c++.exe"

    # transform or discard each component of argument
    for arg in arguments[1:]:
        if re.match("^-D.*", arg):
            command += " " + arg
        elif re.match("^-std=*", arg):
            command += " " + arg
        elif re.match("^-I../../", arg):
            command += " " + arg.replace("../..", root)
        elif arg == "-include":
            command += " -include " + buildsub + "ap_config.h"
        elif arg == "-I.":
            command += " -I" + buildsub
        elif re.match("^-I", arg):
            command += " -I" + root + "/" + buildsub + arg.replace("-I", "")
    return command


def main(args):

    parser = argparse.ArgumentParser(prog=args[0],
                                     description="Sanitize 'compile_commands.json' and move it to current directory")
    parser.add_argument('-f', '--input-file', required=True,
                        help='path/to/compile_commands.json. ')
    parsedArgs,unparsedArgs = parser.parse_known_args(args)

    if not parsedArgs.input_file:
        print("Must provide correct relative path to compile_commands.json")
        return 1

    root, buildsub = split_build_dir(parsedArgs)

    with open(parsedArgs.input_file) as json_file:
        data = json.load(json_file)
        for p in data:
            p['directory'] = root

            # create "command" and delete "arguments"
            tmpcommand = make_command_from_arguments(p['arguments'], root, buildsub)
            del p['arguments']

            # transform file and delete "file" json member, so we can make it appear last
            tmpfile = xform_file(root, buildsub, p['file'])            
            del p['file']

            # add "command" to json and re-add "file"
            p['command'] = tmpcommand + " " + tmpfile
            p['file'] = tmpfile

    with open("compile_commands.json", "w") as outfile:
        print(json.dumps(data, indent=2), file=outfile)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
