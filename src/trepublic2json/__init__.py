import argparse
import json
import os
from glob import glob

from trepublic2json.error import TRParserError
from trepublic2json.parser import parse_pdf


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path of the pdf files to parse.", type=_is_valid_path)
    args = parser.parse_args()
    search = os.path.join(args.path, "*.pdf")

    pdfs = glob(search)
    pdfs = [parse_pdf(pdf) for pdf in pdfs]
    pdfs = json.dumps(pdfs, indent=2, sort_keys=True)
    print(pdfs)
    return 0


def _is_valid_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise TRParserError(f"main.py: error: argument path: {path} is not a valid path")
