from setuptools import setup, find_packages

setup(
    name='ParentLOL',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        "colorama",
        "datetime"
    ],
    description='Printing with Ease.',
    author='parent',
    author_email='parent@parent.lol',
    url='https://github.com/parentrb',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
