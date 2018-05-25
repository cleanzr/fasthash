from distutils.core import setup, Extension

module1 = Extension('hello',
                    # sources = ['C++Codes/Bucket.cpp', 'C++Codes/DensifiedMinHash.cpp', 'C++Codes/SignedRandomProjection.cpp', 'C++Codes/CaPSuLe.cpp', 'C++Codes/LSH.cpp', 'C++Codes/main.cpp'],
                    sources = ['hello.cpp'])
                    # extra_compile_args=['-fopenmp'])

setup (name = 'PackageName',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])