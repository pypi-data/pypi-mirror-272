from setuptools import find_packages, setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='tabqa',
    packages=find_packages(),
    version='0.1.3',
    description='This Python package provides functions to convert natural language to SQL queries using a pre-trained language model.',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author='Ketan More',
    install_requires = ["torch", "transformers", "bitsandbytes", "accelerate", "sqlparse"],
    setup_requires = ["torch", "transformers", "bitsandbytes", "accelerate", "sqlparse"],
    tests_require= ["torch", "transformers", "bitsandbytes", "accelerate", "sqlparse"],
    test_suite='tests',
)