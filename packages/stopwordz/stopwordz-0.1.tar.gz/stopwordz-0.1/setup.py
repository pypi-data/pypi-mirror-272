from setuptools import setup, find_packages

setup(
    name='stopwordz',
    version='0.1',
    packages=find_packages(),
    description='A simple stopword cleaner',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Subashanan Nair',
    author_email='subaashnair12@gmail.com',
    url='https://github.com/subaashnair/stopwordz',
    install_requires=[
        # Any dependencies, for example: 'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
