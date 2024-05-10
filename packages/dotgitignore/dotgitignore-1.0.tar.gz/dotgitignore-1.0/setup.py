import setuptools
import os

directory = os.path.abspath(os.path.dirname(__file__))
requirements_path = os.path.join(directory, 'requirements.txt')
readme_path = os.path.join(directory, 'README.md')

LONG_DESCRIPTION = open(readme_path).read()
REQUIRED_PACKAGES = open(requirements_path).read().splitlines()

setuptools.setup(
    name="dotgitignore",
    version="1.0",
    author="Aiglon Doré & Rainbow",
    author_email="contact@mathquantlab.com",
    packages=setuptools.find_packages(),
    description="A command-line utility tool to fetch .gitignore files for multiple languages.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="GNU GPL-3",
    keywords="gitignore git ignore",
    install_requires=REQUIRED_PACKAGES,
)
