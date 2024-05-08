from setuptools import find_packages, setup

DEPENDENCIES = [
    "setuptools",
    "pefile",
    "pycurl",
    "tqdm",
    "google-cloud-storage",
    "sphinx",
    "pytest",
    "pyqt6",
    "pyinstaller",
    "PySide6",
]

VERSION = "0.0.4-alpha5"
DOC = ""

setup(
    name="WGSE-NG",
    packages=find_packages(),
    author="Multiple",
    author_email="",
    include_package_data=True,
    extras_require={"gui": ["wgse.gui"], "cli": ["wgse.cli"]},
    description="Whole Genome Sequencing data manipulation tool",
    long_description="Whole Genome Sequencing data manipulation tool",
    install_requires=DEPENDENCIES,
    entry_points={"gui_scripts": ["wgse = wgse.gui:main"]},
    url="https://github.com/chaplin89/WGSE-NG",
    version=VERSION,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="bioinformatics",
)
