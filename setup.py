from setuptools import setup
from Cython.Build import cythonize

setup(
    name="chronosmatch-cython",
    ext_modules=cythonize(
        "cython_matching_engine.pyx",
        compiler_directives={"language_level": "3"},
    ),
)