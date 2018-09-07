#!/usr/bin/env python3
import argparse
import datetime
import json
import sys


class StoreAsDict(argparse.Action):
    """
    argparse action to create dicts from command-line
    """

    def __call__(self, parser, namespace, values, option_string=None):
        d = dict()
        for pair in values:
            try:
                k, v = pair.split("=")
            except ValueError as e:
                raise ValueError("can't interpret '{}' — no equal-sign".format(pair))

            if k in d:
                raise ValueError("duplicate key '{}'".format(k))
            if k == "msg" or k == "@timestamp":
                raise ValueError("'{}' is a reserved keyword".format(k))
            d[k] = v

        setattr(namespace, self.dest, d)


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("additional_fields",
                        help="additional fields to add to the json, e.g. service_name=my-service",
                        nargs="*",
                        action=StoreAsDict)
    parser.add_argument("-l", help="wrap output line by line", action="store_true")
    return parser


def wrap_msg(msg, additional_fields):
    return json.dumps({
        **additional_fields,
        '@timestamp': datetime.datetime.now().isoformat(),
        'msg': msg
    })


def read_lines(additional_fields):
    for line in sys.stdin:
        print(wrap_msg(line[:-1], additional_fields))


def read_full_stdin(additional_fields):
    msg = "".join([line for line in sys.stdin])

    print(wrap_msg(
        # remove trailing newline
        msg[:-1] if msg.endswith("\n") else msg,
        additional_fields,
    ))


def main():
    args = get_argparser().parse_args()

    if not sys.stdin.isatty():
        if args.l:
            read_lines(args.additional_fields)
        else:
            read_full_stdin(args.additional_fields)


if __name__ == '__main__':
    main()
