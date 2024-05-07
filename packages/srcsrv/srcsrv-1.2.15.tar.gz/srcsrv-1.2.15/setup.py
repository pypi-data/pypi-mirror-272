'''
    Scrip for packaging source indexing
'''

# Copyright (C) 2023 Uri Mann (abba.mann@gmail.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Python modules
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='srcsrv',
    version='1.2.15',
    author='Uri Mann',
    author_email='abba.mann@gmail.com',
    description='Source indexing package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Additional assets for README.md
    package_data={'': [
        'docs/ADVANCE.md',
        'docs/PLUGIN.md',
        'docs/SETUP.md',
        'docs/assets/Cache.png',
        'docs/assets/debugging.png',
        'docs/assets/VS_Options+.png',
        'docs/assets/SrcSrv_Dialog+.png',
        'docs/assets/WinDBG+.png',
        'docs/assets/WinDBG1+.png',
        'docs/assets/WinDBG_SrcDialog.png',
        ]
    },
    include_package_data=True,
    url='https://github.com/urielmann/srcsrv-public',
    license = 'MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Development Status :: 4 - Beta'
    ],
    install_requires=[
        'requests>=2',
        'GitPython>=3',
    ],
    python_requires='>=3.8',
    packages=[
        'srcsrv',
        'srcsrv.plugins',
        'srcsrv.tools',
        'srcsrv.utils',
    ],
    package_dir={'': '.'}
)
