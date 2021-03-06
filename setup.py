from setuptools import find_packages, setup

with open('README.rst', 'r') as long_description_file:
    long_description = long_description_file.read()

setup(
    name='math2',
    version='0.0.1.dev13',
    author='Juho Kim',
    author_email='juho-kim@outlook.com',
    description='A Python package for various math functions',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/AussieSeaweed/math2',
    packages=find_packages(),
    package_data={'math2': ('py.typed',)},
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ),
    python_requires='>=3.9',
    install_requires='auxiliary',
)
