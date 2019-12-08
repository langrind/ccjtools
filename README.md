# CCJTools

Scripts for working with JSON compilation databases fro clang etc. 

I need to produce and convert [compilation
databases](https://sarcasm.github.io/notes/dev/compilation-database.html)
for different projects and different toolchains. This repo has
sscripts to help with that.

There are currently three commands:

* ccj-make      - Produce a JSON format compilation database from a text build log
* ccj-xform-ap  - Sanitize ArduPilot compilation database and move it to current directory
* ccj-xform-px4 - Sanitize PX4 compilation database and move it to current directory

`ccj-make` is useful when you've captured make commands in a text file
and need to produce a compilation database. For each line of text that
your make produced, if it looks like a compile command, `ccj-make`
creates a single record with three fields: `directory`, `command` and
`file`.

The `directory` member is the same for each record. It comes from the
`-p` command line option, or from $PWD.

The `command` comes from looking for lines whose first word appears to
be a compiler. The `-c` command line option specifies an exact match
string if needed. Otherwise, the program guesses.

The `file` is assumed to be the last word on the line that was
identified as a command.

Heuristics are naive, and presumably will evolve to be more
sophisticated, and also to be governable via user options

At the end of the run, the compilation database is produced by emitting
all the records to the file `compile_commands.json`, or a name that you
provide via the `-o` command line switch.

An existing json file can be provided via the `-e` command line
option. It is used to prepopulate the internal list of records.
(Should add the ability to preserve existing entries or modify
them. Currently it only modifies them.)

This program is not cautious about overwriting the existing
`compile_commands.json`.

The other two programs transform a `compile_commands.json` taken from
a PX4 or ArduPilot build, by making it appear as if the build was
performed in the root, minimizing the significance of the
`build/<config>` directory. This makes tools such as CCLS, Rtags and
LSP work more smoothly.

## Usage and Examples

### ccj-make

The ccjtools repo has a file `tests/mcux_build.log` that you can turn
into a compilation database by doing:

```
$ ccj-make mcux_build.log -r gcc
```

### ccj-xform-px4

From the top of a PX4 dir, after it's been built:

```
$ ccj-xform-px4 -f build/px4_fmu-v5_multicopter/compile_commands.json
```

will produce `./compile_commands.json`, which can be used by the
Rtags command for instance:

```
$ rc --project-root=$PWD -J .
```

### ccj-xform-ap

Similarly for an Ardupilot build, from the root of your Ardupilot
clone after it's been built:

```
$ ccj-xform-ap -f build/CubeBlack/compile_commands.json
```

## Author

* **[Nik Langrind](https://github.com/langrind)**

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details


