"""
Copyright (C) 2024 William Newport

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildPyCommand(build_py):
    """Custom build command."""

    def run(self):
        import grpc_tools.protoc  # type: ignore
        # Your custom generation logic here

        # Generate gRPC code for DataSurface API
        # The code will be generated in the src/datasurface/api folder
        grpc_tools.protoc.main([  # type: ignore
            'grpc_tools.protoc',
            '--proto_path=./src',
            '--python_out=./src',
            '--pyi_out=./src',
            '--grpc_python_out=./src',
            './src/datasurface/api/api.proto'
        ])

        build_py.run(self)


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='datasurface',
    version='0.0.16',
    license='AGPLv3',
    description='Automate the governance, management and movement of data within your enterprise',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Billy Newport',
    author_email='billy@billynewport.com',
    url='https://github.com/billynewport/datasurface',
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
        'Topic :: Database :: Database Engines/Servers',
    ],
    packages=find_packages(where='src'),
    cmdclass={
        'build_py': BuildPyCommand
    },
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={"datasurface": ["*.pyi", "**/*.pyi", "py.typed"]},  # Include .pyi files and py.typed file
    install_requires=requirements,
    setup_requires=['grpcio-tools'],
    # Modules with DataPlatforms should register their entry points here
    entry_points={
        'DataPlatforms': []
    }
)
