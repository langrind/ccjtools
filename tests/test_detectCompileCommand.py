#!/usr/bin/env python3

from ccjtools import ccj_make

def test_detectExactSpecifiedCompilerCommandWord():
    """Using -c option, check that the exact word is recognized"""

    inputFileName = 'dummy'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', inputFileName, '-c', 'mastadon'])
    if not parsedArgs:
        assert False

    # Note that we are basically testing "strcmp()" here. A different test is used
    # to check a whole line of input
    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "mastadon"):
        assert False

    if ccj_make.mkccj_is_compiler_command(parsedArgs, "Mastadon"):
        assert False

    if ccj_make.mkccj_is_compiler_command(parsedArgs, "Mastadon"):
        assert False

    if ccj_make.mkccj_is_compiler_command(parsedArgs, "mastadon++"):
        assert False

    if ccj_make.mkccj_is_compiler_command(parsedArgs, "astadon"):
        assert False

    assert True


def test_detectCompilerWord():
    """Not using -c option, check that plausible compiler commands are recognized"""

    inputFileName = 'dummy'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', inputFileName])
    if not parsedArgs:
        assert False

    # Note that we are basically testing a regexp single-word match. A different test
    # is used to check a whole line of input
    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "gcc"):
        assert False

    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "mastadon-gcc"):
        assert False

    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "Mastadon-c++"):
        assert False

    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "gcc"):
        assert False

    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "c++"):
        assert False

    if not ccj_make.mkccj_is_compiler_command(parsedArgs, "g++"):
        assert False

    if ccj_make.mkccj_is_compiler_command(parsedArgs, "mastadon++"):
        assert False

    if ccj_make.mkccj_is_compiler_command(parsedArgs, "mastadon"):
        assert False

    assert True


def test_detectExactSpecifiedCompilerCommand():
    """Using -c option, check that lines are recognized correctly"""

    inputFileName = 'dummy'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', inputFileName, '-c', 'mastadon'])
    if not parsedArgs:
        assert False

    if ccj_make.mkccj_process_line(parsedArgs, {}, [], "mastadons are not bluefish -Itheentireseas"):
        assert False

    if not ccj_make.mkccj_process_line(parsedArgs, {}, [], "mastadon are not bluefish -Itheentireseas"):
        assert False

    if ccj_make.mkccj_process_line(parsedArgs, {}, [], "mastadon-gcc mastadon.c -D_THIS_ -D_THAT_ -fno-dependent-clauses-or-santa-clauses-either"):
        assert False

    bigString = "/opt/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-g++  -DCONFIG_ARCH_BOARD_PX4_FMU_V5 -D__CUSTOM_FILE_IO__ -D__DF_NUTTX -D__PX4_NUTTX -D__STDC_FORMAT_MACROS -isystem ../../platforms/nuttx/NuttX/include/cxx -isystem NuttX/nuttx/include/cxx -isystem NuttX/nuttx/include -I../../boards/px4/fmu-v5/src -I../../platforms/nuttx/src/px4/common/include -I. -Isrc -Isrc/lib -Isrc/modules -I../../platforms/nuttx/src/px4/stm/stm32f7/include -I../../platforms/common/include -I../../src -I../../src/include -I../../src/lib -I../../src/lib/DriverFramework/framework/include -I../../src/lib/matrix -I../../src/modules -I../../src/platforms -INuttX/nuttx/arch/arm/src/armv7-m -INuttX/nuttx/arch/arm/src/chip -INuttX/nuttx/arch/arm/src/common -INuttX/apps/include  -mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard -Os -DNDEBUG   -g -fdata-sections -ffunction-sections -fomit-frame-pointer -fmerge-all-constants -fno-signed-zeros -fno-trapping-math -freciprocal-math -fno-math-errno -fno-strict-aliasing -fvisibility=hidden -include visibility.h -Wall -Wextra -Werror -Warray-bounds -Wcast-align -Wdisabled-optimization -Wdouble-promotion -Wfatal-errors -Wfloat-equal -Wformat-security -Winit-self -Wlogical-op -Wpointer-arith -Wshadow -Wuninitialized -Wunknown-pragmas -Wunused-variable -Wno-missing-field-initializers -Wno-missing-include-dirs -Wno-unused-parameter -fdiagnostics-color=always -fno-builtin-printf -fno-strength-reduce -Wformat=1 -Wunused-but-set-variable -Wno-format-truncation -fcheck-new -fno-exceptions -fno-rtti -fno-threadsafe-statics -Wreorder -Wno-overloaded-virtual -nostdinc++ -std=gnu++11 -o msg/CMakeFiles/uorb_msgs.dir/topics_sources/uORBTopics.cpp.obj -c /home/langrind/Firmware/build/px4_fmu-v5_multicopter/msg/topics_sources/uORBTopics.cpp"

    if ccj_make.mkccj_process_line(parsedArgs, {}, [], bigString):
        assert False

    assert True


def test_detectCompilerCommandLine():
    """Not using -c option, check that plausible compiler command lines are recognized"""

    inputFileName = 'dummy'
    parsedArgs = ccj_make.mkccj_parse_args(['progname', inputFileName])
    if not parsedArgs:
        assert False

    if ccj_make.mkccj_process_line(parsedArgs, {}, [], "mastadons are not bluefish -Itheentireseas"):
        assert False

    if not ccj_make.mkccj_process_line(parsedArgs, {}, [], "mastadon-gcc mastadon.c -D_THIS_ -D_THAT_ -fno-dependent-clauses-or-santa-clauses-either"):
        assert False

    bigString = "/opt/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-g++  -DCONFIG_ARCH_BOARD_PX4_FMU_V5 -D__CUSTOM_FILE_IO__ -D__DF_NUTTX -D__PX4_NUTTX -D__STDC_FORMAT_MACROS -isystem ../../platforms/nuttx/NuttX/include/cxx -isystem NuttX/nuttx/include/cxx -isystem NuttX/nuttx/include -I../../boards/px4/fmu-v5/src -I../../platforms/nuttx/src/px4/common/include -I. -Isrc -Isrc/lib -Isrc/modules -I../../platforms/nuttx/src/px4/stm/stm32f7/include -I../../platforms/common/include -I../../src -I../../src/include -I../../src/lib -I../../src/lib/DriverFramework/framework/include -I../../src/lib/matrix -I../../src/modules -I../../src/platforms -INuttX/nuttx/arch/arm/src/armv7-m -INuttX/nuttx/arch/arm/src/chip -INuttX/nuttx/arch/arm/src/common -INuttX/apps/include  -mcpu=cortex-m7 -mthumb -mfpu=fpv5-d16 -mfloat-abi=hard -Os -DNDEBUG   -g -fdata-sections -ffunction-sections -fomit-frame-pointer -fmerge-all-constants -fno-signed-zeros -fno-trapping-math -freciprocal-math -fno-math-errno -fno-strict-aliasing -fvisibility=hidden -include visibility.h -Wall -Wextra -Werror -Warray-bounds -Wcast-align -Wdisabled-optimization -Wdouble-promotion -Wfatal-errors -Wfloat-equal -Wformat-security -Winit-self -Wlogical-op -Wpointer-arith -Wshadow -Wuninitialized -Wunknown-pragmas -Wunused-variable -Wno-missing-field-initializers -Wno-missing-include-dirs -Wno-unused-parameter -fdiagnostics-color=always -fno-builtin-printf -fno-strength-reduce -Wformat=1 -Wunused-but-set-variable -Wno-format-truncation -fcheck-new -fno-exceptions -fno-rtti -fno-threadsafe-statics -Wreorder -Wno-overloaded-virtual -nostdinc++ -std=gnu++11 -o msg/CMakeFiles/uorb_msgs.dir/topics_sources/uORBTopics.cpp.obj -c /home/langrind/Firmware/build/px4_fmu-v5_multicopter/msg/topics_sources/uORBTopics.cpp"

    if not ccj_make.mkccj_process_line(parsedArgs, {}, [], bigString):
        assert False

    assert True
