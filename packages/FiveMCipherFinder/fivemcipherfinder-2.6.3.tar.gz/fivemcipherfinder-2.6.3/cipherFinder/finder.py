#!/bin/python3.11

#  Copyright (c) 2022-2023 - exersalza
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal # noqa
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all # noqa
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, # noqa OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE # noqa
#  SOFTWARE.
from __future__ import annotations
from datetime import datetime as dt

import os
import sys
import argparse

from cipherFinder.de_obfs import de_obfs, do_regex
from cipherFinder.deleter import deleter_main, y_n_validator, _BACKUP_DIR
from cipherFinder.plugins import load_plugs, _PluginDummy, get_remote_plugins
from cipherFinder.utils import detect_encoding

DEBUG = False
_REGEX = r"(((\\x|\\u)([a-fA-F0-9]{2}))+)"
_URL_REGEX = (
    r"(https?://(www\.)?[-\w@:%.\+~#=]{2,256}\."
    r"[a-z]{2,4}\b([-\w@:%\+.~#?&//=]*))"
)
_COLORS = ["\033[0m", "\033[91m", "\033[92m"]

# Prevent accidental overwrites through plugins
_log = []
_shadow_log = []
_del_lines = []
_counter = {"failed": 0}
_hooks = {"__blanc": _PluginDummy()}

_args = {"skip": False}


def __update_hooks(new_hooks: dict) -> int:
    """Update the Hook dict because of python can't
    do it itself without setting something global

    Parameters
    ----------
    new_hooks : dict
        give the new hooks

    Returns
    -------
    int :
        Return code
    """

    for k, v in new_hooks.items():
        _hooks[k] = v

    return 0


def __execute_hook(hook_name: str, *args, **kw) -> int:
    """Just executes the given hook name

    Parameters
    ----------
    hook_name : str
        Give a hook name to execute

    args : any
        Give a list of values to the hook

    kw : any
        Give a dict of values to the hook

    Returns
    -------
    int :
        Return code
    """
    _hooks.get(hook_name, _hooks["__blanc"]).execute(*args, **kw)

    return 0


def validate_lines(lines: list) -> list[tuple]:
    """Validate the lines that are given through the 'lines' parameter.

    Parameters
    ----------
    lines : list
        The lines from the current read file.

    Returns
    -------
    list[tuple]
        A list with infected line
        (or false positives by AntiCheat or obfuscated code)
    """

    ret: list[tuple] = []

    for ln, line in enumerate(lines, start=1):
        if x := do_regex(line, _REGEX):
            ret.append(
                (
                    ln,
                    line,
                    de_obfs(x, line)
                    if not _args["skip"]
                    else "Disabled de obfuscation",
                )
            )

    __execute_hook("GetValidatedLines", ret)
    return ret


def prepare_log_line(**kw) -> int:
    """Prepares the string for the logging

    Parameters
    ----------
    kw : str, Any
        Some values listed below

    Returns
    -------
    int
        Returns the current count
    """
    d = kw.pop("d", ".")  # Directory
    ln = kw.pop("ln", "")  # Triggered line number
    file = kw.pop("file", "poggers.lua")  # filename
    line = kw.pop("line", "")  # Trigger line
    count = kw.pop("count", 0)  # global trigger count
    target = kw.pop("target", "")  # Decoded lines
    logged = kw.pop("logged", {})  # don't print stuff twice

    path = d.replace("\\", "/") + f"/{file}"
    url = ""

    if x := do_regex(target, _URL_REGEX):
        url = x[0][0]

    # why TF do it even gets printed twice????
    if logged.get(path, -1) == ln:
        return count

    _shadow = {
        "dir": d,
        "ln": ln,
        "file": file,
        "line": line,
        "count": count + 1,
        "decoded": target,
        "path": path,
    }

    __execute_hook("GetLoggingValues", _shadow)

    to_log = (
        f"File: {path}\n"
        f"LineNumber: {ln}\n"
        f"Attacker URL: {url}\n"
        f"DecodedLines: \n{'-' * 10}\n{target}\n{'-' * 10}"
    )

    if kw.pop("verbose", 0):
        print(to_log)

    _log.append(to_log + f"\nTrigger Line:\n{line!r}\n{'-' * 15}\n")
    _shadow_log.append(_shadow)
    _del_lines.append((line, ln, path))

    count += 1
    logged[path] = ln
    return count


def check_file(
    d: str, file: str, count: int, args: argparse.Namespace
) -> tuple[int, int]:
    """Iterate over a file and check the lines

    Parameters
    ----------
    d : str
        Give the path to the file e.g "/home/wildCiphers"
    file : str
        Give a file name to scan e.g "wildCipherInHere.lua"
    count: int
        Give the current cipher count.
    args: argparse.Namespace
        Give the arguments delivered from the Cmd line.

    Returns
    -------
    tuple[ret_code, count]
        A Tuple with the return code and the current cipher count.
    """

    enc, confidence = detect_encoding(f"{d}/{file}")

    with open(f"{d}/{file}", "r", encoding=enc, errors="replace") as f:
        try:
            lines = f.readlines()

        except UnicodeDecodeError as e:
            if DEBUG:
                print(e)

            _counter["failed"] += 1
            print(
                f"Can't decode `{d}/{file}`. File has an unknown encoding"
                f"or it can't be determined."
                f"Consider looking into it by yourself.",
                (
                    f" -> Encoding: {enc!r} "
                    f"Confidence: {confidence * 100:.0f}%"
                    if args.verbose
                    else ""
                ),
            )
            return 1, count

        match = validate_lines(lines)
        logged = {}

        if not match:
            return 0, count

        for ln, line, target in match:
            count = prepare_log_line(
                d=d,
                ln=ln,
                file=file,
                line=line,
                count=count,
                target=target,
                logged=logged,
                verbose=args.verbose,
            )
    return 0, count


def get_filename(output) -> str:
    """Get the filename of args, when set.

    Parameters
    ----------
    output : str
        The string that is given when someone puts the -o switch

    """
    filename = f"CipherLog-{dt.now():%H-%M-%S}.txt"
    temp_name = filename

    if output:
        temp_name = output[0]

    if temp_name.endswith("/"):
        return temp_name + filename

    return temp_name


def write_log_file(**kw) -> int:
    """writes the logfile

    parameters
    ----------
    kw : dict
        path : str : path and or filename
        red : str : colorcode for red
        white : str : colorcode for white
        count : int : the found cipher count

    returns
    -------
    int
        statuscode
    """
    print(
        f'{kw.pop("red")}oh no, the program found a spy in your files x.x '
        f"check the cipherlog.txt for location and trigger. "
        f'{kw.pop("count")} were found!'
        f'{kw.pop("white")}\n#staysafe'
    )
    args = kw.pop("args")

    # we want them to print before the no_log bc of reasons
    __execute_hook("GetFileContents", _log)
    __execute_hook(
        "GetRawFileContents", _shadow_log, failed=_counter.get("failed", 0)
    )

    if args.no_log:  # if the user types -n
        return 0

    filename = get_filename(args.output)

    __execute_hook("GetLogFilename", filename)

    with open(filename, "w+", encoding="utf-8") as f:
        f.writelines(_log)

    return 0


def main(arg_list: list) -> int:
    """validates lua files.

    usage:
    ------
    run the program: `find-cipher [path] [exclude path] [options...]`.

    args:
        --path : optional :
            give the path to search, when no path is given, the
            current working directory will be used `.`
        --exclude-path : optional :
            exclude directory's where you don't want to search.
        --no-log: optional :
            don't create a log file, can be used hand in hand with --verbose
        --verbose : optional :
            print a cipher directly to the command line on found.
        --v2 : optional :
            uses an extra algorithm to find gibberish or randomly generated
            variable/function/table names. it can introduce more palse-positiv
            because of obfuscated scripts, but can help to find ciphers.

    advertisement:
    --------------
    get your beautiful cipher today, just smack the play button and find some.
    just for $9.99 you can get the base edition, and just for anohter $49.99
    you can get yourself access to the version 2.
    i hope you don't have any but always be sure to have none.

    returns
    -------
    int
        return code
    """

    if sys.version_info < (3, 8):
        print(
            "Please use python 3.8 or above. "
            "Python 3.7 and below are not supported."
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(description="validates lua files.")

    parser.add_argument(
        "-p",
        "--path",
        nargs="?",
        default=".",
        help="give the path to search, when no path is given"
        ', the current working directory will be used "."',
    )

    parser.add_argument(
        "-x",
        "--exclude",
        nargs="*",
        default="",
        help="exclude directories where you don't want to search.",
    )

    parser.add_argument(
        "-n",
        "--no-log",
        action="store_true",
        help="don't create a log file, can be used hand in hand with -v",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print a cipher directly to the command line " " on found.",
    )

    parser.add_argument(
        "-o",
        "--output",
        nargs=1,
        help="define the output path/filename of the logfile. "
        "syntax: path/[filename]. please note to add an / "
        "to the end of the path when you don't want to use"
        " a custom filename.",
    )

    parser.add_argument(
        "--plug-dir",
        nargs=1,
        help="give a directory that stores plugins for the cipherfinder."
        "read the documentation or inside the cipherfinder/plugins.py"
        " on how to write custom plugins.",
    )

    parser.add_argument(
        "-w",
        "--no-wizard",
        action="store_true",
        help="don't start the eraser wizard after the script finishes.",
    )

    parser.add_argument(
        "--get-remote-plugins",
        action="store_true",
        help="Get remote plugins to your local environment.",
    )

    parser.add_argument(
        "--no-deobfs",
        action="store_true",
        help="Don't run the De Obfuscation part, can help when "
        "you an MemoryError",
    )

    args = parser.parse_args(arg_list)
    os.environ["DEBUG"] = str(DEBUG)

    if not args.path:
        print("No Path given to argument -p")
        sys.exit(1)

    if args.get_remote_plugins:
        get_remote_plugins()
        return 0

    if args.plug_dir:
        _plugs = load_plugs(args.plug_dir[0])

        if _plugs.get("error", 0):
            return 1

        __update_hooks(_plugs)

    # Iniate hooks
    __execute_hook("Init")

    pattern = "".join(
        [
            (i.replace(",", ")|(") if "--" not in i else "")
            for i in args.exclude
        ]
    )
    local_path = args.path
    _args["skip"] = args.no_deobfs
    count = 0

    for d, _, files in os.walk(local_path):
        # skip excluded directories, but why you skip 'em?
        if pattern and do_regex(rf"{d}", f'{"(" + pattern + ")"}'):
            continue

        for file in files:
            if ".lua" not in file:
                continue

            _, count = check_file(d, file, count, args)

    # Write log
    red = green = white = ""

    if not os.name == "nt":
        white, red, green = _COLORS

    if _log:  # this triggers if there is a cipher
        write_log_file(white=white, red=red, count=count, args=args)

        if args.no_wizard:
            return 0

        if y_n_validator(
            input(  # pylint: disable=bad-builtin
                "Do you want to start the eraser wizard? files getting backed "
                f"up in a directory named {_BACKUP_DIR} [y/N] "
            )
        ):
            if not os.path.isdir(_BACKUP_DIR):
                os.mkdir(_BACKUP_DIR)
            deleter_main(_del_lines)

        return 0

    print(f"{green}Nice! There were no Cipher's found!{white}")
    return 0


def entry_point() -> int:
    """Just the entry_point for find-cipher"""
    return main(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(entry_point())
