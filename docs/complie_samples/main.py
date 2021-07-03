import logging
import sys
import os
import argparse
from typing import Tuple

import ca
import parser
from cga import make_token_list
import discern as ds
import gener


def parse_args():
    argparser = argparse.ArgumentParser(
        description="write your c/c++ program by markdown, then cga builds them.")
    argparser.add_argument("-v", "--version", action="store_const",
                           const=True, default=False, help="查看当前版本")
    argparser.add_argument("markdown", help="input file(it must be markdown file)")
    argparser.add_argument("-o", "--output", default='.', help="output path")

    if len(sys.argv) <= 1:
        return argparser.parse_args(["-h"])
    return argparser.parse_args(sys.argv[1:])


def execute_cga(i_file_path: str, o_file_path: str) -> None:
    tokens = ds.lex(i_file_path)
    node_list = make_token_list(tokens)
    all_code_block = parser.hunt(node_list)

    for code_block in all_code_block:
        info_block = ca.build_block(ca.gcc(code_block.code))
        parser.insert(code_block.end, info_block)

    gener.write_to_md(node_list, o_file_path)


def preprocess(i_file_path: str, o_file_path: str) -> Tuple[str, str]:
    if not os.path.exists(i_file_path):
        logging.error('no such file: ' + i_file_path)
        return
    if o_file_path and o_file_path != '.':
        if os.path.exists(o_file_path):
            logging.error('file has been existed: ' + o_file_path)
            return
        else:
            _dir = os.path.dirname(o_file_path)
            if not os.path.exists(_dir):
                logging.error('no such directory: ' + _dir)
    else:
        i_file_name = i_file_path.split('/')[-1]
        o_file_name = i_file_name.split('.')[0] + '.cc.' + i_file_name.split('.')[-1]
        o_file_path = os.path.dirname(i_file_path) + '/' + o_file_name
    return i_file_path, o_file_path


def main():
    args = parse_args()
    io_path = preprocess(args.markdown, args.output)
    if io_path:
        f_in, f_out = io_path
        execute_cga(f_in, f_out)


if __name__ == '__main__':
    main()
