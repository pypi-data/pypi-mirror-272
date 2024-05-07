from setuptools import setup, find_packages


setup(
    name='rlanutils',
    version='0.1.9',
    packages=find_packages(),
    description='A handy tool that make your day to day programming much easier. ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='brianlan',
    author_email='brianlanbo@gmail.com',
    url='https://gitlab.com/rlan/rlanutils',
    install_requires=[
        "numpy",
        "scipy",
        "tqdm",
        "matplotlib",
        "pytest",
        "pyyaml",
    ],
)