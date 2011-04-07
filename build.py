#! /usr/bin/env python

import os, sys, subprocess

def msg(str):
    sys.stderr.write(str + '\n')

def which(exe):
    sts = 0
    output = subprocess.Popen(
            [sys.executable, "tools/which.py", exe],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE ).communicate()[0]

    if output == '':
        sts = 1
    return [ sts, output ]

def runScons():
    sconsPath = "scons-local/scons.py"
    if not os.path.exists( sconsPath ):
        msg( "scons-local is missing" )
        return 1

    try:
        retcode = subprocess.call( [sys.executable, sconsPath] )
        if retcode < 0:
            return -retcode
        else:
            return retcode
    except OSError, e:
        msg( "Execution failed: " + e )
    return 1

#------------------------------------------------------------------------------

def main():
    if which( "scons" )[0] != 0:
        msg( "no scons" )

    ret = runScons()
    sys.exit(ret)

if __name__ == "__main__":
    main()
