#!/usr/bin/env python3

import os, filecmp
from ccjtools import ccj_make

def test_mcux():
    """Produce compilation database from MCUExpresso build log, check if as expected"""

    projectDir = '/home/langrind/Documents/MCUXpresso_11.0.1_2563/workspace/evkmimxrt1064_lwip_ping_bm'
    
    existingFile =  'tests/mcux_compile_commands.json'
    if not os.path.exists(existingFile):
        assert False

    outputFile =  'tests/mcux_test_output.json'
    if os.path.exists(outputFile):
        os.remove(outputFile)
        if (os.path.exists(outputFile)):
            assert False

    cmdLine = 'ccj-make tests/mcux_build.log -r gcc -o {of} -p {pd}'.format(of=outputFile, pd=projectDir)
    ccj_make.main(cmdLine.split())

    
    if not os.path.exists(outputFile):
        assert False

    if not filecmp.cmp( outputFile, existingFile, shallow=False):
        assert False

    os.remove(outputFile)
    if (os.path.exists(outputFile)):
        assert False

    assert True
