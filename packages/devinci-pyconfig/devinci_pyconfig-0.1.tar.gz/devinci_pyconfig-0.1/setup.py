from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='devinci_pyconfig',
    version='0.1',
    description='A Python toolkit for managing configuration properties in a '
                'Python application',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='devinci-it',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    package_data={'config': ['config.ini']}
)
