#! /usr/bin/env python

# Originally based upon Python26\Tools\Scripts\which.py

# Variant of "which".
# On stderr, near and total misses are reported.

import sys
if sys.path[0] in (".", ""): del sys.path[0]

import sys, os
from stat import *

def msg(str):
    sys.stderr.write(str + '\n')

def main():
    pathlist = os.environ['PATH'].split(os.pathsep)

    ext = [""]
    if os.name == "nt":
        ext = ["", ".exe", ".bat", ".cmd"]

    sts = 0

    for prog in sys.argv[1:]:
        ident = ()
        for dir in pathlist:
            basename = os.path.join(dir, prog)

            for e in ext:
                try:
                    filename = basename + e
                    st = os.stat(filename)
                    break
                except os.error:
                    filename = ""
                    continue

            if not filename:
                continue

            if not S_ISREG(st[ST_MODE]):
                msg(filename + ': not a disk file')
            else:
                mode = S_IMODE(st[ST_MODE])
                if mode & 0111:
                    if not ident:
                        print filename
                        ident = st[:3]
                    else:
                        if st[:3] == ident:
                            s = 'same as: '
                        else:
                            s = 'also: '
                        msg(s + filename)
                else:
                    msg(filename + ': not executable')

        if not ident:
            msg(prog + ': not found')
            sts = 1

    sys.exit(sts)

if __name__ == '__main__':
    main()
