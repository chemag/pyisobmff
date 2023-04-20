#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""isobmff-parse.py: A generic ISOBMFF (ISO base media file,
ISO/IEC 14496-12) parser."""

import argparse
import os
import sys

dirname = os.path.dirname(sys.modules[__name__].__file__)
this_dir = os.path.abspath(dirname)
rootdir = os.path.join(this_dir, "..")
sys.path.append(rootdir)

import isobmff

__version__ = "0.1"

FUNC_CHOICES = {
    "parse": "parse isobmff input",
    "extract-box": "extract full box by name",
    "extract-value": "extract box payload by name",
}

default_values = {
    "debug": 0,
    "dry_run": False,
    "func": "parse",
    "listfile": None,
    "path": None,
    "infile": None,
    "outfile": None,
}


def parse_file(infile, debug):
    media_file = isobmff.MediaFile(infile, debug)
    media_file.read()
    return media_file


def test_file_of_files(listfile, debug):
    # read the list of input files from the input file
    error_list = []
    with open(listfile, "r") as f:
        for infile in f.readlines():
            # parse the input file
            infile = infile.strip()
            print(f"### parsing {infile}")
            try:
                _ = parse_file(infile, debug)
            except:
                print(f"    error on {infile}")
                error_list.append(infile)
    # dump the list of broken input files
    if error_list:
        print("BROKEN FILES")
        for filename in error_list:
            print(f"  {filename}")


def extract_box(media_file, path, outfile, include_headers, debug):
    # search the path in media_file
    box = media_file.find_subbox(path)
    if box is None:
        print(f"error: cannot find {path} in {media_file.filename}")
        sys.exit(-1)
    # extract the expected bytes
    with open(media_file.filename, "rb") as fin:
        start_offset = box.offset if include_headers else box.payload_offset
        fin.seek(start_offset)
        size = box.size
        if not include_headers:
            size -= start_offset - box.offset
        data = fin.read(size)
    # extract the expected bytes
    with open(outfile, "wb") as fout:
        fout.write(data)


def get_options(argv):
    """Generic option parser.

    Args:
        argv: list containing arguments

    Returns:
        Namespace - An argparse.ArgumentParser-generated option object
    """
    # init parser
    # usage = 'usage: %prog [options] arg1 arg2'
    # parser = argparse.OptionParser(usage=usage)
    # parser.print_help() to get argparse.usage (large help)
    # parser.print_usage() to get argparse.usage (just usage line)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        dest="version",
        default=False,
        help="Print version",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        dest="debug",
        default=default_values["debug"],
        help="Increase verbosity (use multiple times for more)",
    )
    parser.add_argument(
        "--quiet",
        action="store_const",
        dest="debug",
        const=-1,
        help="Zero verbosity",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=default_values["dry_run"],
        help="Dry run",
    )
    parser.add_argument(
        "--func",
        type=str,
        nargs="?",
        default=default_values["func"],
        choices=FUNC_CHOICES.keys(),
        help="%s"
        % (" | ".join("{}: {}".format(k, v) for k, v in FUNC_CHOICES.items())),
    )
    for key, val in FUNC_CHOICES.items():
        parser.add_argument(
            f"--{key}",
            action="store_const",
            dest="func",
            const=f"{key}",
            help=val,
        )
    parser.add_argument(
        "--path",
        type=str,
        default=default_values["path"],
        metavar="box-path",
        help="box path",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        default=default_values["outfile"],
        metavar="output-file",
        help="output file",
    )
    parser.add_argument(
        "--listfile",
        type=str,
        default=default_values["listfile"],
        metavar="list-file",
        help="list file",
    )
    parser.add_argument(
        "infile",
        type=str,
        nargs="?",
        default=default_values["infile"],
        metavar="input-file",
        help="input file",
    )
    # do the parsing
    options = parser.parse_args(argv[1:])
    if options.version:
        return options
    # implement help
    if options.func == "help":
        parser.print_help()
        sys.exit(0)
    return options


def main(argv):
    # 0. parse options
    options = get_options(argv)
    if options.version:
        print("version: %s" % __version__)
        sys.exit(0)
    if options.debug > 0:
        print(options)

    # 1. parse the input file
    if options.listfile is not None:
        test_file_of_files(options.listfile, options.debug)
        sys.exit()
    media_file = parse_file(options.infile, options.debug)

    if options.func == "parse":
        print(media_file)

    elif options.func in ["extract-box", "extract-value"]:
        include_header = options.func == "extract-box"
        extract_box(
            media_file, options.path, options.outfile, include_header, options.debug
        )


if __name__ == "__main__":
    # at least the CLI program name: (CLI) execution
    main(sys.argv)
