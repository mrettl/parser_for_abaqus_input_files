from setuptools import setup

setup(
    name='abq_parser',
    description='Parse and write Abaqus Input files.',
    version='2.0',
    packages=[
        'abq_parser',
        'abq_parser.inp'],
    package_dir={
        'abq_parser': 'abq_parser'
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
