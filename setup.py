import sys
from setuptools import setup

setup(
    name = "filesystem",        # what you want to call the archive/egg
    version = "0.1",
    packages=["filesystem", "datStream", "main"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'helloworld[foo]'
    package_data = {},
    author=["Moeed Ahmad" , "Haziq Usman"],
    author_email = "moeed27@gmail.com",
    description = "A vitual file managment system implemented for a single .dat file",
    license = "BSD",
    keywords= "virtual file management system",
    url = "http://github.com/dbarnett/vfmsCS7C",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "initializeFileSys = filesys.main:main",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
