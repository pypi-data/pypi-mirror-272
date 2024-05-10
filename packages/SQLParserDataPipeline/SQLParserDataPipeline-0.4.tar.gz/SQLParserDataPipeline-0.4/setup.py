from setuptools import setup, find_packages
print(find_packages())

setup(
    name='SQLParserDataPipeline', 
    version='0.4',      
    author='Emanuele Iaccarino',  
    author_email='emanueleiaccarino.ei@gmail.com',  
    description="The SQLParserDataPipeline Library is a powerful Python package designed for parsing and interpreting complex SQL queries. It was developed with a focus on BigQuery but is adaptable to other SQL dialects due to its flexible parsing strategy that doesn't consider the function itself but the most inner parentheses.",
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    packages=find_packages(), 
    install_requires=[
    ], # No install required because we only use re packages that is already part of Python’s standard library
    python_requires='>=3.6',  
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
