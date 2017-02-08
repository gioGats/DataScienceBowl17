import sys
import subprocess


def install_lib(library_name):
    if library_name == 'tensorflow':
        install_tensorflow()
    else:
        subprocess.run(['pip3', 'install', library_name])
        # TODO Subprocess execute 'pip3 install $LIB'


def install_tensorflow():
    # TODO pick the binary_url
    binary_url = ''
    install_lib(binary_url)


if __name__ == '__main__':
    missing_libraries = []
    incorrectly_installed = []
    try:
        # noinspection PyUnresolvedReferences
        import numpy
        # TODO test to make sure the library is installed properly
    except ImportError:
        missing_libraries.append('numpy')
    except AssertionError:
        incorrectly_installed.append('numpy')
    try:
        # noinspection PyUnresolvedReferences
        import pydicom
        # TODO test to make sure the library is installed properly
    except ImportError:
        missing_libraries.append('pydicom')
    except AssertionError:
        incorrectly_installed.append('pydicom')
    try:
        # noinspection PyUnresolvedReferences
        import pillow
        # TODO test to make sure the library is installed properly
    except ImportError:
        missing_libraries.append('pillow')
    except AssertionError:
        incorrectly_installed.append('pillow')
    try:
        # noinspection PyUnresolvedReferences
        import tensorflow
        # TODO test to make sure the library is installed properly
    except ImportError:
        missing_libraries.append('tensorflow')
    except AssertionError:
        incorrectly_installed.append('tensorflow')
    if len(missing_libraries) > 0:
        if input('Missing libraries %s.\nWould you like to install them now? [y/n] ' % str(missing_libraries)).lower()\
                == 'y':
            for lib in missing_libraries:
                install_lib(lib)
        else:
            sys.exit()
