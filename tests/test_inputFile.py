#!/usr/bin/env python3
import os

from ccjtools import ccj_make
import json

def test_readInput():
    """read an empty file, get nothing"""
    inputFileName = 'tests/emptyBuild.txt'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', inputFileName])
    if not parsedArgs:
        assert False

    jsonList, xrefDict = ccj_make.mkccj_convert_input_file(parsedArgs)
    if jsonList:
        assert False

    if xrefDict:
        assert False

    assert True


def test_readExistingAndEmptyInput():
    """read an empty file, but produce a dictionary because we start with an existing dict"""
    inputFileName = 'tests/emptyBuild.txt'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', inputFileName, '-e', 'tests/existing.json'])
    if not parsedArgs:
        assert False

    outputList, crossRefDict = ccj_make.mkccj_read_existing_json(parsedArgs)
    if not outputList:
        assert False

    if not crossRefDict:
        assert False

    record = outputList[0]
    if not record:
        assert False

    outputFile = 'tests/out.json'
    if os.path.exists(outputFile):
        os.remove(outputFile)
        if (os.path.exists(outputFile)):
            assert False

    with open(outputFile, "w") as outfile:
        print(json.dumps(record, indent=2), file=outfile)

    if os.path.exists(outputFile):
        os.remove(outputFile)
        if (os.path.exists(outputFile)):
            assert False

    # Check that the crossRefDictionary and the List are coherent
    for record in outputList:
        if record is not crossRefDict[record['file']]:
            assert False

    assert True
