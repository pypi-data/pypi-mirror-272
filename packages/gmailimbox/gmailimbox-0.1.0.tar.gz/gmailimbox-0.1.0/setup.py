from setuptools import setup, find_packages

setup(
    name='gmailimbox',
    version='0.1.0',
    description='A simple Gmail API client to fetch emails based on specific criteria',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Santosh Kumar',
    author_email='rayskumar02@gmail.com',
    url='https://github.com/santoshray02/gmailimbox',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
