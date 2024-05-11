from setuptools import setup, find_packages

setup(
    name='tokencurator',
    version='0.1.0',
    description='Manage text content to fit specific token limits of machine learning models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Grade Calculator',
    author_email='hello@gradecalculator.ai',
    url='https://gradecalculator.ai/',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tiktoken'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
)
