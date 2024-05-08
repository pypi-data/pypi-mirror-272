from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy
extensions = [
    Extension("zentropy.lib", ["lib/knnpermute.c",],
        include_dirs=[numpy.get_include(),]),
]
setup_args = dict(
    ext_modules = extensions,
    package_data = {"lib":["knnpermute.c"]}
)
setup(**setup_args)