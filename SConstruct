# scons script for fsm

import os, sys

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

env = Environment(ENV = os.environ)

vars = Variables('build-setup.conf');
vars.AddVariables(
    BoolVariable('CONFIG_FROM_FILE', '', False),
    ('CONFIG_PLATFORM', '', ''),
    ('GIT_CHECKOUT', '', ''),
    ('WHICH_PATH', '', '%s %s' % (sys.executable, os.path.normpath("tools/which.py"))),
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
    print 'Configuring...'

    isGitCheckout = os.path.exists('.git')

    def CheckProgram(context, name):
        context.Message( 'Checking for %s... ' % name )
        ret = context.TryAction( env['WHICH_PATH'] + " " + name )[0]
        context.Result( ret )
        return ret

    conf_tests = { 'CheckProgram' : CheckProgram }
    conf = Configure(env, custom_tests = conf_tests)

    if not conf.CheckCXX() :
        print('\t!! Your compiler and/or environment is not correctly configured.')
        Exit(1)

    if not conf.CheckFunc('printf', language="C++") :
        print('\t!! Your compiler and/or environment is not correctly configured.')
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
            print("\t!! You need '%s' to compile this library" % header)
            Exit(1)

    doAssertHeader('stddef.h')
    doAssertHeader('math.h')
    doAssertHeader('float.h')
    doAssertHeader('string.h')
    doAssertHeader('limits')
    doAssertHeader('assert.h')

#    env['FSM_ISNAN'] = ''
#    if not conf.CheckFunc('isnan', language="C++"):
#        if not conf.CheckFunc('_isnan', language="C++"):
#            print "\t!! You nee the function 'isnan' or '_isnan' to compile this library"
#            Exit(1)
#        else:
#            env['FSM_ISNAN'] = '_isnan'

    if GetOption('run_doxygen'):
        if conf.CheckProgram( 'doxygen' ):
            env['HAS_DOXYGEN'] = True
        else:
            print "\tCannot find doxygen on your system, make sure it is in your PATH"
            print "\tSkipping doxygen..."
            env['HAS_DOXYGEN'] = False

    if GetOption('run_ctags'):
        if conf.CheckProgram( 'ctags' ):
            env['HAS_CTAGS'] = True
        else:
            print "\tCannot find ctags on your system, make sure it is in your PATH"
            print "\tSkipping tags..."
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
