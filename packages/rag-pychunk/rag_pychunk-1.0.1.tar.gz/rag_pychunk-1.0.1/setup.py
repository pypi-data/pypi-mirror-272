from setuptools import setup, find_packages

setup(
    name='rag-pychunk',
    version='1.0.1',
    packages=find_packages(),
    scripts=['scripts/python-scripts/classify-python-code.sh', 
             'scripts/python-scripts/find-node-relationships.sh', 
             'scripts/python-scripts/generate-node-metadata.sh'],
    author="Jaime Sancho Molero", 
    author_email="jimysanchomolero@gmail.com", 
)
