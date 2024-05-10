from setuptools import setup, find_packages
import os

VERSION = '0.1'
DESCRIPTION = 'Calculate many figures area or volume'
working_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(working_directory, "README.md"), encoding='utf-8') as f:
    long_description1 = f.read()
# Setting up
setup(
    name="marksgeometrys",
    version=VERSION,
    author="mark. (Marc Pérez)",
    author_email="<marcperezcarrasco2010@gmail.com>",
    url='https://github.com/marc1fino/marksgeometrys',
    description=DESCRIPTION,
    long_description=long_description1,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['math'],
    license='MIT',
    keywords=['python', 'maths', 'figures', 'area', 'volume', 'mathematical figures'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
'pypi-AgEIcHlwaS5vcmcCJDIyZDZhZDUwLTRkNzAtNGRjMS1hZTI5LTg2OTMyZmU4OGYwZgACKlszLCJlNThhMDY5Mi01ZTdiLTRlOTUtYWU2Yy0wYzQ2NjJiOGI2NzMiXQAABiAciNaPzy-LRMDIoyYp4892fBq_KBZCg8pXjZ76eZK-xw'