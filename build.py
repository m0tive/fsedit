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

#isGitCheckout = os.path.exists('.git')

if which( "scons" )[0] != 0:
    msg( "no scons" )

sconsPath = "scons-local/scons.py"
if not os.path.exists( sconsPath ):
    msg( "scons-local is missing" )
    exit(1)

os.system( sys.executable + " " + sconsPath )
