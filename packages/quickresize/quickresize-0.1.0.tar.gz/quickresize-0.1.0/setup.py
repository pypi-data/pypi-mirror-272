from setuptools import find_packages, setup

readme = open('README.md').read()

setup(
    name='quickresize',
    packages=find_packages(),
    version='0.1.0',
    description='In-place resizing of images present in a folder',
    long_description=readme,
    author='Nityanand Mathur',
    license='MIT',
    entry_points={
        'console_scripts': [
            'resize=quickresize.resize:main'
        ]
    }
)
