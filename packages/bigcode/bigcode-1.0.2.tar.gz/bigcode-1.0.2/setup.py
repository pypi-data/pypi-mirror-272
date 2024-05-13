from setuptools import setup, find_packages

version = '1.0.2'

long_description = """Python module for bigcode management platform (bigcode wrapper)"""

setup(
    name='bigcode',
    version=version,
    author='ayhan',
    author_email='jumanyyazowayhan32@gmail.com',
    description='A custom admin interface for Django inspired by the Django Jazzmin.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ayhandev/bigcode_adminstration.git',
    download_url=f'https://github.com/ayhandev/bigcode/releases/download/1.0.2/bigcode-1.0.2tar.gz',
    license='MIT',
    packages=find_packages(),
    include_package_data=True, 
    install_requires=[
        'django>=3.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
