# scons script for fsm

import os, sys
from ctypes import *

AddOption("--test",
          action="store_true", dest="run_tests", default=True,
          help="Compile and run unit tests [default]")
AddOption("--no-test",
          action="store_false", dest="run_tests",
          help="Don't compile and run unit tests")

AddOption("--debug-build",
          action="store_true", dest="debug",
          help="Compile with debug information and warnings")
AddOption("--release",
          action="store_false", dest="debug", default=False,
          help="Compile without debug information and warnings [default]")

AddOption("--doxygen",
          action="store_true", dest="run_doxygen", default=True,
          help="Generate the reference documents [default]")
AddOption("--no-doxygen",
          action="store_false", dest="run_doxygen",
          help="Don't generate the reference documents")

AddOption("--tags",
          action="store_true", dest="run_ctags",
          help="Generate tags")
AddOption("--no-tags",
          action="store_false", dest="run_ctags", default=False,
          help="Don't generate tags [default]")

AddOption("--configure",
          action="store_true", dest="run_config_and_quit", default=False,
          help="Run the build configuration process and quit")

#-------------------------------------------------------------------------------

def color_print(color, text, newline=True):
    # 1 - red
    # 2 - green
    # 3 - yellow
    # 4 - blue
    text = "\033[9%sm%s\033[0m" % (color,text)
    if not newline:
        print text,
    else:
        print text

def win_color_print(color, text, newline=True):
    col = [ 15, 12, 10, 14, 9 ]
    windll.Kernel32.GetStdHandle.restype = c_ulong
    h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))
    windll.Kernel32.SetConsoleTextAttribute(h, col[color])
    if not newline:
        print text,
    else:
        print text
    windll.Kernel32.SetConsoleTextAttribute(h, 15)

def regular_print(color, text, newline=True):
    if not newline:
        print text,
    else:
        print text

if os.name == 'nt':
  color_print = win_color_print

#-------------------------------------------------------------------------------

env = Environment(ENV = os.environ)

vars = Variables('build-setup.conf');
vars.AddVariables(
    BoolVariable('CONFIG_FROM_FILE', '', False),
    ('CONFIG_PLATFORM', '', ''),
    ('GIT_CHECKOUT', '', ''),
    ('WHICH_PATH', '', '%s %s' % (sys.executable, os.path.normpath("tools/which.py"))),
    ('PKG_CONFIG_PATH', '', 'pkg-config'),
    ('GTKCONFIG', '', ''),
#    BoolVariable('USE_MSC_STDINT', '', False),
#    ('FSM_ISNAN', '', ''),
    BoolVariable('HAS_DOXYGEN', '', False),
    BoolVariable('HAS_CTAGS', '', False),
    )
vars.Update(env)

clean_build = GetOption('clean')
display_help = GetOption('help')

#-------------------------------------------------------------------------------

reconfig = True

if clean_build or display_help:
    reconfig = False
else:
    if GetOption('run_config_and_quit'):
        reconfig = True
    elif env['CONFIG_FROM_FILE']:
        if env['CONFIG_PLATFORM'] == env['PLATFORM']:
            reconfig = False
        else:
            print "Configuration file is for a different platform."
            reconfig = True


if reconfig :
    color_print(2, 'Configuring...')

    isGitCheckout = os.path.exists('.git')

    def CheckExecutable(context, name):
        context.Message( 'Checking for %s... ' % name )
        ret = context.TryAction( env['WHICH_PATH'] + " " + name )[0]
        context.Result( ret )
        return ret

    def CheckPkgConfig(context, version):
        context.Message( 'Checking for pkg-config... ' )
        ret = context.TryAction(
            '%s --atleast-pkgconfig-version=%s' % (context.env["PKG_CONFIG_PATH"], version))[0]
        context.Result( ret )
        return ret

    def CheckPkg(context, name):
        context.Message( 'Checking for %s... ' % name )
        ret = context.TryAction(
            '%s --exists \'%s\'' % (context.env["PKG_CONFIG_PATH"], name))[0]
        context.Result( ret )
        return ret

    def CheckGtk(context):
        context.Message( 'Checking for gtk+... ' )
#        lastLIBS = context.env['LIBS']
#        context.env.Append( LIBS = ['gtk', 'gdk'] )
#        ret = context.TryLink( "#include <gtk/gtk.h>\nint main(int c,char **v){gtk_init(&c, &v);return 0;}" )
#        context.env.Replace( LIBS = lastLIBS )
        ret = False
        context.Result( ret )
        return ret

    def configWarning( msg ):
        color_print(1, '\t!! ' + msg)

    def configLog( msg ):
        color_print(3, '\t.. ' + msg)

    conf_tests = {
        'CheckExecutable' : CheckExecutable,
        'CheckPkgConfig' : CheckPkgConfig,
        'CheckPkg' : CheckPkg,
        'CheckGtk' : CheckGtk,
        }

    conf = Configure(env, custom_tests = conf_tests)

    if not conf.CheckCXX() :
        configWarning('Your compiler and/or environment is not correctly configured.')
        Exit(1)

    if not conf.CheckFunc('printf', language="C++") :
        configWarning('Your compiler and/or environment is not correctly configured.')
        Exit(1)

#    if not conf.CheckHeader('stdint.h', language="C++"):
#        if env['CC'] == "cl":
#            print "\tUsing local header 'include/fsm/stdint.h'"
#            env['USE_MSC_STDINT'] = True
#        else:
#            print "\t!! You need 'stdint.h' to compile this library"
#            Exit(1)
#    else:
#        env['USE_MSC_STDINT'] = False

    def doAssertHeader( header ):
        if not conf.CheckHeader( header, language="C++"):
            configWarning("You need '%s' to compile this library" % header)
            Exit(1)

    doAssertHeader('stddef.h')
    doAssertHeader('math.h')
    doAssertHeader('float.h')
    doAssertHeader('string.h')
    doAssertHeader('limits')
    doAssertHeader('assert.h')

    if not conf.CheckPkgConfig('0.15.0'):
        configWarning('You need pkg-config (version 0.15 or greater) to compile this library')
        configLog('Check it is in your PATH, or set PKG_CONFIG_PATH')
        if os.name == 'nt':
            configLog('A Win32 installer can be found at:\n\t.. http://www.gtk.org/download-windows.html')
        Exit(1)

#    env['FSM_ISNAN'] = ''
#    if not conf.CheckFunc('isnan', language="C++"):
#        if not conf.CheckFunc('_isnan', language="C++"):
#            print "\t!! You need the function 'isnan' or '_isnan' to compile this library"
#            Exit(1)
#        else:
#            env['FSM_ISNAN'] = '_isnan'

    if not conf.CheckPkg('gtk+-2.0'):
        configWarning('You need gtk+ to build this library')
        Exit(1)

    if GetOption('run_doxygen'):
        if conf.CheckExecutable( 'doxygen' ):
            env['HAS_DOXYGEN'] = True
        else:
            configLog("Cannot find doxygen on your system, make sure it is in your PATH")
            configLog("Skipping doxygen...")
            env['HAS_DOXYGEN'] = False

    if GetOption('run_ctags'):
        if conf.CheckExecutable( 'ctags' ):
            env['HAS_CTAGS'] = True
        else:
            configLog("Cannot find ctags on your system, make sure it is in your PATH")
            configLog("Skipping tags...")
            env['HAS_CTAGS'] = False

    env = conf.Finish()

    env['GIT_CHECKOUT'] = isGitCheckout
    env['CONFIG_FROM_FILE'] = True
    env['CONFIG_PLATFORM'] = env['PLATFORM']
    vars.Save('build-setup.conf', env)

    if GetOption('run_config_and_quit'):
        Exit(0)

# end reconfig

#-------------------------------------------------------------------------------

global_env = env
Export( 'global_env' )

#SConscript( 'src/SConscript' )

if GetOption('run_tests') or clean_build:
    print "there are no tests to run"
#    SConscript( [ 'googletest.SConscript', 'tests/SConscript' ] )

if (GetOption('run_doxygen') or clean_build) and env['HAS_DOXYGEN'] :
    print "doxygen is not setup yet. Finish updating SConstruct to get it working"
#    doxygen_sources = Glob( 'include/fsm/*.hpp')
#    doxygen_sources.extend( Glob( 'Doxyfile' ) )
#    docs_target = env.Command( 'docs/html/index.html', doxygen_sources, "doxygen" )
#    env.Alias('docs', docs_target)

if (GetOption('run_ctags') or clean_build) and env['HAS_CTAGS'] :
    print "ctags is not setup yet. Finish updating SConstruct to get it working"
#    ctags_sources = Glob( 'include/fsm/*.hpp')
#    tags = []
#    env.Command( 'obj', '', Mkdir("$TARGET") )
#    for ctags_src in ctags_sources:
#        t = env.Command( 'obj/' + os.path.basename(str(ctags_src)) + '.tags.log', ctags_src,
#            [ "ctags -a --sort=yes --c++-kinds=+p --fields=+iaS --extra=+q --verbose=yes $SOURCES > $TARGET" ])
#        tags.append(t)
#    env.Alias('tags', tags)
#
