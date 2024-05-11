from setuptools import setup, find_packages

setup(
    name='rag-pychunk',
    version='0.1.0',
    packages=find_packages(),
    scripts=['pychunk/scripts/python-scripts/classify-python-code.sh', 
             'pychunk/scripts/python-scripts/find-node-relationships.sh', 
             'pychunk/scripts/python-scripts/generate-node-metadata.sh'],
    author="Jaime Sancho Molero", 
    author_email="jimysanchomolero@gmail.com", 
)
