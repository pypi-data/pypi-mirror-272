from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='healthharbor_dental_client',
    version='0.1.0',
    description='An Unofficial client library for interacting with Health Harbor Dental API',
    long_description=read('README.md'),  
    long_description_content_type='text/markdown',
    author='Don Johnson',
    author_email='donj@zuub.com',
    url='https://github.com/yourusername/healthharbor_dental_client', 
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify which versions of Python are supported
    keywords='healthharbor api dental client',  # Keywords to improve discoverability
    project_urls={  # Additional URLs that are relevant to your project
        'Bug Reports': 'https://github.com/copyleftdev/healthharbor_dental_client/issues',
        'Source': 'https://github.com/copyleftdev/healthharbor_dental_client',
    },
)
