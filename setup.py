from setuptools import setup

setup(
    name='abaqus_parser',
    description='Parse and write Abaqus Input files.',
    version='1.0',
    packages=[
        'abaqus_parser',
        'abaqus_parser.inp'],
    package_dir={
        'abaqus_parser': 'abaqus_parser'
    },
    url='https://github.com/mrettl/abaqus_parser',
    license='MIT',
    author='Matthias Rettl',
    author_email='',
    install_requires=[
        "numpy>=1.19",
        "ply>=3.11"
    ]
)
