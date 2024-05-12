# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# STANDARD LIBARY IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
from setuptools import (
    find_packages,
    setup,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# INTERNAL IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

from src.meetlify import __VERSION__

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# DATABASE/CONSTANTS LIST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

python_minor_min = 8
python_minor_max = 12
confirmed_python_versions = [
    "Programming Language :: Python :: 3.{MINOR:d}".format(MINOR=minor)
    for minor in range(python_minor_min, python_minor_max + 1)
]

# Fetch readme file
with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

# Define source directory (path)
SRC_DIR = "src"

# Requirements for dev and gui
extras_require = {
    "dev": [
        "black",
        "python-language-server[all]",
        "setuptools",
        "twine",
        "wheel",
        "setuptools",
        "pytest",
        "pytest-cov",
        "twine",
        "wheel",
        "mkdocs",
        "mkdocs-gen-files",
        "mkdocstrings[python]",
        "pymdown-extensions",
    ],
}
extras_require["all"] = list(
    {rq for target in extras_require.keys() for rq in extras_require[target]}
)

# Install package
setup(
    name="meetlify",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
    version=__VERSION__,
    description="Python Package to Generate Meetup Websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Faisal Shahzad",
    author_email="pybodensee@gmail.com",
    url="https://github.com/pybodensee/meetlify",
    download_url="https://github.com/pybodensee/meetlify/releases/v%s.tar.gz"
    % __VERSION__,
    license="MIT",
    keywords=["meetups", "static-site-generators", "seo", "python"],
    scripts=[],
    include_package_data=True,
    python_requires=">=3.{MINOR:d}".format(MINOR=python_minor_min),
    setup_requires=[],
    install_requires=["click", "markdown", "Jinja2"],
    extras_require=extras_require,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "meetlify = meetlify.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ]
    + confirmed_python_versions
    + [
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
        "Topic :: System",
        "Topic :: System :: Archiving",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Archiving :: Mirroring",
        "Topic :: System :: Filesystems",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
