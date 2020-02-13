from distutils.core import setup
from distutils.extension import Extension

from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        "dbe",
        ["dbe.pyx"],
        language='c++',
        extra_compile_args=["-std=c++17"],
        include_dirs=['/localdisk/gal/root/igalink/omnisci_dbe_gcc/omniscidb'],
        library_dirs=[
            '/usr/lib/x86_64-linux-gnu',
            '/usr/local/mapd-deps/lib',
            './',
        ],
        libraries=['DBEngine'],
    )
]

setup(name='dbe', cmdclass={'build_ext': build_ext}, ext_modules=ext_modules)
