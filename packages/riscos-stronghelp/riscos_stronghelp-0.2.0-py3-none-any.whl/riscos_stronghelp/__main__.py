#!/usr/bin/env python
"""
Command line tool for extracting StrongHelp manuals into a directory.

    python -m riscos_stronghelp.extractor --extract-dir <directory> <stronghelp-file>
"""

import argparse
import os
import sys

from riscos_stronghelp.format import StrongHelp, objtype_dir


def extract_to_directory(sh, output_dir):
    """
    Extract the whole archive to a target directory.
    """
    try:
        os.makedirs(output_dir)
    except OSError:
        pass

    for shf in sh:
        print("Extracting {}".format(shf.filename))
        filename = os.path.join(output_dir, shf.unix_filename)
        if shf.objtype == objtype_dir:
            try:
                os.makedirs(filename)
            except OSError:
                pass
        else:
            with open(filename, 'wb') as fh:
                fh.write(shf.read())


def setup_argparse():
    parser = argparse.ArgumentParser(usage="%s [<options>] <strong-help-file>" % (os.path.basename(sys.argv[0]),))
    parser.add_argument('file', action='store',
                        help="StrongHelp file to read")
    parser.add_argument('--extract-dir', action='store', default="SHManual",
                        help="Directory to extract into")

    return parser


def main():
    parser = setup_argparse()

    options = parser.parse_args()

    sh = StrongHelp(options.file)

    if options.extract_dir:
        extract_to_directory(sh, options.extract_dir)


if __name__ == '__main__':
    main()
