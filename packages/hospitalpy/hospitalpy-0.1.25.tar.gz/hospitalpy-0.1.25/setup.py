from setuptools import setup, find_packages

VERSION = '0.1.25'
DESCRIPTION = 'Text Regularization for Unstructured Text from EMS Reports'
LONG_DESCRIPTION = 'Made by Michael Chary'

# Setting up
setup(
    name="hospitalpy",
    version=VERSION,
    author="Michael Chary",
    author_email="<mic9189@med.cornell.edu>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where='src'),
    include_package_data=True,
    keywords=['python', 'nlp', 'ems', 'global ems'],
    classifiers=[]
)
