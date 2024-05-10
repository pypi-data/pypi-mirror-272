#! /usr/bin/env python3

import argparse
import os
import shutil
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))

LINUX_URL = "https://github.com/nicovank/linux.git"
LINUX_TAG = "personal"


def main(args):
    INSTALL_PATH = os.path.join(ROOT, "local")
    VENDOR_PATH = os.path.join(ROOT, "vendor")

    if args.clean:
        shutil.rmtree(INSTALL_PATH, ignore_errors=True)
        shutil.rmtree(VENDOR_PATH, ignore_errors=True)
        return

    LINUX_ROOT = os.path.join(VENDOR_PATH, "linux")
    PERF_ROOT = os.path.join(LINUX_ROOT, "tools", "perf")

    if not os.path.isdir(LINUX_ROOT):
        print("-- Downloading a copy of the Linux kernel for a modern perf version")
        subprocess.run(
            [
                "git",
                "clone",
                f"--branch={LINUX_TAG}",
                "--depth=1",
                LINUX_URL,
                LINUX_ROOT,
            ],
            stdout=(None if args.verbose else subprocess.DEVNULL),
            stderr=(None if args.verbose else subprocess.DEVNULL),
        ).check_returncode()

    if not os.path.isfile(os.path.join(INSTALL_PATH, "bin", "perf")):
        print("-- Building perf")
        subprocess.run(
            ["make", f"prefix={INSTALL_PATH}", "install"],
            cwd=PERF_ROOT,
            stdout=(None if args.verbose else subprocess.DEVNULL),
            stderr=(None if args.verbose else subprocess.DEVNULL),
        ).check_returncode()
    else:
        print("-- Using existing perf copy")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python3 build.py", description="uperf convenience build script"
    )

    parser.add_argument("--clean", action="store_true", help="Clean up all files")
    parser.add_argument("-v", "--verbose", action="store_true")

    main(parser.parse_args())
