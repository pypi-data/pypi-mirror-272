from setuptools import setup, find_packages

setup(
    name="PubChem_Prospector",
    version="0.1",
    packages=find_packages(),
    description="functions for bulk scraping pubchem annotations",
    author="demontrees",
    author_email="demontrees96@gmail.com",
    url="https://github.com/demontrees/PubChem_Prospector",
    install_requires=[
        'urllib3>=1.26.16'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)