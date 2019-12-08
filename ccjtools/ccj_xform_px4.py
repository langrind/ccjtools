#!/usr/bin/env python3
"""
Transform compile_commands.json taken from a PX4 build, by making it
appear as if the build was performed in the root, minimizing the
significance of the build/<config> directory.This makes ccls and lsp
work more smoothly.

From the top of a PX4 dir, after it's been built:

$ xpx4_ccj -f build/px4_fmu-v5_multicopter/compile_commands.json

will produce ./compile_commands.json, which can be used by the
rtags command:

$ rc --project-root=$PWD -J .
"""

import argparse, sys, os, json, re

def xform_file(root, buildsub, filename):
    """
    chop buildsub out of filename, if the resulting filename is an
    actual file, return the chopped filename. Otherwise, return the
    original
    """
    newFilename = filename.replace(buildsub, '')
    if os.path.exists(newFilename):
        return newFilename
    return filename

def xform_command(root, buildsub, command, regex, replaceDict):
    """
    do all the transforms
    """
    return regex.sub(lambda mo: replaceDict[mo.string[mo.start():mo.end()]], command) 

def split_build_dir(args):
    cwd = os.getcwd()
    prefix = args.input_file.split('compile_commands.json')[0]
    return cwd, prefix
    
def main(args):

    parser = argparse.ArgumentParser(prog=args[0],
                                     description="Sanitize 'compile_commands.json' and move it to current directory")
    parser.add_argument('-f', '--input-file', help='Input filename')
    parsedArgs,unparsedArgs = parser.parse_known_args(args)

    root, buildsub = split_build_dir(parsedArgs)
    mIbuildsub = "-I" + buildsub
    replaceDict = {
        "-Isrc/lib"       : "",
        "-Isrc/modules"   : "",
        "-Isrc"           : "",
        "-isystem NuttX"  : "-Iplatforms/nuttx/NuttX",
        "-INuttX"         : "-Iplatforms/nuttx/NuttX",
        "-I NuttX"        : "-Iplatforms/nuttx/NuttX",
        "-isystem ../../" : "-I",
        "-I../../"        : "-I",
        "-I. "           : mIbuildsub,
    }
    regex = re.compile("(%s)" % "|".join(map(re.escape, replaceDict.keys())))

    with open(parsedArgs.input_file) as json_file:
        data = json.load(json_file)
        for p in data:
            p['directory'] = root
            p['command'] = xform_command(root, buildsub, p['command'],
                                         regex, replaceDict)
            p['file'] = xform_file(root, buildsub, p['file'])

    with open("compile_commands.json", "w") as outfile:
        print(json.dumps(data, indent=2), file=outfile)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
