#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""isobmff-parse.py: A generic ISOBMFF (ISO base media file,
ISO/IEC 14496-12) parser."""

import argparse
import glob
import os
import pandas as pd
import pathlib
import sys
import tempfile

dirname = os.path.dirname(sys.modules[__name__].__file__)
this_dir = os.path.abspath(dirname)
rootdir = os.path.join(this_dir, "..")
sys.path.append(rootdir)

import isobmff

__version__ = "0.2"

FUNC_CHOICES = {
    "parse": "parse isobmff input",
    "extract-box": "extract full box by name",
    "extract-value": "extract box payload by name",
    "list-items": "list item IDs and their types",
    "get-item-sizes": "list sizes per item type",
    "extract-item": "extract contents of item with item ID to file",
    "parse-item": "parse contents of item with item ID",
}

default_values = {
    "debug": 0,
    "dry_run": False,
    "func": "parse",
    "testdir": None,
    "listfile": None,
    "path": None,
    "item_id": None,
    "infile": None,
    "outfile": None,
}


ITEM_LIST_HEADERS = (
    "item_id",
    "path",
    "item_type",
    "primary",
    "construction_method",
    "offset",
    "length",
)


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


ISOBMFF_EXTENSIONS = (".mp4", ".heic", ".heif", ".mov", ".m4a", ".3gp", ".uvu")


def get_list_of_isobmff_files(testdir, debug):
    known_atom_list = isobmff.get_atom_list()
    filelist = []
    for fname in glob.glob(os.path.join(testdir, "*")):
        if os.path.isdir(fname):
            filelist += get_list_of_isobmff_files(fname, debug)
        elif pathlib.Path(fname).suffix in ISOBMFF_EXTENSIONS:
            with open(fname, "rb") as fin:
                size0 = fin.read(4)
                brand0 = fin.read(4)
                if brand0 in known_atom_list:
                    filelist.append(fname)
    return filelist


def test_directory(testdir, debug):
    # 1. get the list of isobmff files
    filelist = get_list_of_isobmff_files(testdir, debug)
    # 2. parse them all
    error_list = {}
    for fname in filelist:
        # parse the input file
        if debug > 1:
            print(f"### parsing {fname}")
        try:
            _ = parse_file(fname, debug)
        except Exception as exc:
            if debug > 0:
                print(f"    error on {fname}")
            error_list[fname] = exc.args[0]
    # 3. dump the list of broken input files
    if error_list:
        print("# BROKEN FILES")
        for fname, error in error_list.items():
            print(f"-> {fname}")
            print(f"{error}")


def extract_bytes(infile, offset, size, outfile, debug):
    # read the bytes
    with open(infile, "rb") as fin:
        fin.seek(offset)
        data = fin.read(size)
    # write the bytes
    if outfile is None or outfile == "-":
        outfile = "/dev/fd/1"
    with open(outfile, "wb") as fout:
        fout.write(data)


def extract_box(media_file, path, outfile, include_headers, debug):
    # search the path in media_file
    box = media_file.find_subbox(path)
    if box is None:
        print(f"error: cannot find {path} in {media_file.filename}")
        sys.exit(-1)
    # extract the expected bytes
    start_offset = box.offset if include_headers else box.payload_offset
    size = box.size
    if not include_headers:
        size -= start_offset - box.offset
    extract_bytes(media_file.filename, start_offset, size, outfile, debug)


def parse_item(media_file, item_id, debug):
    # extract the item to a tempfile
    outfile = tempfile.NamedTemporaryFile(prefix="pyisobmff.", suffix=".bin").name
    item_dict = extract_item(media_file, outfile, item_id, debug)
    # check whether the item type is defined
    item_type = item_dict["item_type"]
    item_classes = isobmff.get_class_list(isobmff.Item, set())
    for item_class in item_classes:
        if item_class.item_type == item_type.encode():
            break
    else:
        # unimplemented item
        item_class = isobmff.Item
    with open(outfile, "rb") as fd:
        item = item_class(item_id, item_type, fd)
    return item


def extract_item(media_file, outfile, item_id, debug):
    # get the item list info
    df = get_item_list(media_file, debug)
    # ensure the item_id exists
    assert (df["item_id"] == item_id).any(), f"error: item_id {item_id} does not exist"
    # get item info as dictionary
    item_dict = df[df["item_id"] == item_id].to_dict("records")[0]
    # extract item into outfile
    if item_dict["construction_method"] == 0:  # file_offset
        extract_bytes(
            media_file.filename,
            item_dict["offset"],
            item_dict["length"],
            outfile,
            debug,
        )
    elif item_dict["construction_method"] == 1:  # idat_offset
        idat_offset = media_file.find_subbox("/meta/idat").payload_offset
        extract_bytes(
            media_file.filename,
            idat_offset + item_dict["offset"],
            item_dict["length"],
            outfile,
            debug,
        )
    elif item_dict["construction_method"] == 2:  # item_offset
        raise Exception("error: do not support construction_method 2 (item_offset)")
    return item_dict


def get_item_sizes(media_file, debug):
    # get the full item list
    df = get_item_list(media_file, debug)
    # get list of unique types
    item_type_list = df.item_type.unique()
    # join the rows based on item_type
    df_new = pd.DataFrame(columns=("item_type", "num_rows", "length"))
    for item_type in item_type_list:
        num_rows = len(df[df["item_type"] == item_type])
        length = sum(df[df["item_type"] == item_type].to_dict()["length"].values())
        df_new.loc[df_new.size] = [
            item_type,
            num_rows,
            length,
        ]
    return df_new


def get_item_list(media_file, debug):
    # 1. look for the item-related boxes
    iloc_box = media_file.find_subbox("/meta/iloc")
    assert iloc_box is not None, "error: cannot find /meta/iloc"
    iinf_box = media_file.find_subbox("/meta/iinf")
    assert iinf_box is not None, "error: cannot find /meta/iinf"
    pitm_box = media_file.find_subbox("/meta/pitm")
    assert pitm_box is not None, "error: cannot find /meta/pitm"
    # 2. process the data
    # 2.1. primary item ID from pitm box
    pitm_item_id = pitm_box.item_id
    # 2.2. item types and paths from iinf box
    item_types = {
        item_info.item_id: (item_info.item_type, item_info.path)
        for item_info in iinf_box.item_infos
    }
    # 2.3. item locations from iloc box
    item_locations = {
        item["item_id"]: (
            item.get("construction_method", 0),
            (0 if not item["base_offset"] else item["base_offset"])
            + item["extents"][0]["extent_offset"],
            item["extents"][0]["extent_length"],
        )
        for item in iloc_box.items
    }
    # 3. merge the data into a pandas DataFrame
    df = pd.DataFrame(columns=ITEM_LIST_HEADERS)
    item_ids = set(item_types.keys()) & set(item_locations.keys())
    for item_id in item_ids:
        item_type, path = item_types[item_id]
        primary = 1 if item_id == pitm_item_id else 0
        construction_method, offset, length = item_locations[item_id]
        df.loc[df.size] = [
            item_id,
            path,
            item_type,
            primary,
            construction_method,
            offset,
            length,
        ]
    return df


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
        action="version",
        version=__version__,
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
        "--item-id",
        type=int,
        dest="item_id",
        default=default_values["item_id"],
        metavar="item_id",
        help="item id",
    )
    parser.add_argument(
        "--testdir",
        type=str,
        default=default_values["testdir"],
        metavar="test-dir",
        help="test dir",
    )
    parser.add_argument(
        "--listfile",
        type=str,
        default=default_values["listfile"],
        metavar="list-file",
        help="list file",
    )
    parser.add_argument(
        "-i",
        "--infile",
        type=str,
        default=default_values["infile"],
        metavar="input-file",
        help="input file",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        type=str,
        default=default_values["outfile"],
        metavar="output-file",
        help="output file",
    )
    # do the parsing
    options = parser.parse_args(argv[1:])
    # implement help
    if options.func == "help":
        parser.print_help()
        sys.exit(0)
    return options


def main(argv):
    # 0. parse options
    options = get_options(argv)
    if options.debug > 0:
        print(options)

    # 1. run test cases
    if options.listfile is not None:
        test_file_of_files(options.listfile, options.debug)
        sys.exit()
    elif options.testdir is not None:
        test_directory(options.testdir, options.debug)
        sys.exit()

    # 2. parse the input file
    media_file = parse_file(options.infile, options.debug)

    if options.func == "parse":
        print(media_file)

    elif options.func == "extract-box":
        extract_box(
            media_file,
            options.path,
            options.outfile,
            include_headers=True,
            debug=options.debug,
        )

    elif options.func == "extract-value":
        extract_box(
            media_file,
            options.path,
            options.outfile,
            include_headers=False,
            debug=options.debug,
        )

    elif options.func == "extract-item":
        extract_item(media_file, options.outfile, options.item_id, options.debug)

    elif options.func == "parse-item":
        item = parse_item(media_file, options.item_id, options.debug)
        if options.outfile is None or options.outfile == "-":
            options.outfile = "/dev/fd/1"
        with open(options.outfile, "wb") as fout:
            fout.write(str(item).encode())

    elif options.func == "list-items":
        df = get_item_list(media_file, options.debug)
        if options.outfile is None or options.outfile == "-":
            options.outfile = "/dev/fd/1"
        df.to_csv(options.outfile, index=False)

    elif options.func == "get-item-sizes":
        df = get_item_sizes(media_file, options.debug)
        if options.outfile is None or options.outfile == "-":
            options.outfile = "/dev/fd/1"
        df.to_csv(options.outfile, index=False)


if __name__ == "__main__":
    # at least the CLI program name: (CLI) execution
    main(sys.argv)
