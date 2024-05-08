from setuptools import setup, find_packages

VERSION = '0.1.1'
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
    packages=find_packages(),
    keywords=['python', 'nlp', 'ems', 'global ems'],
    classifiers=[]
)
