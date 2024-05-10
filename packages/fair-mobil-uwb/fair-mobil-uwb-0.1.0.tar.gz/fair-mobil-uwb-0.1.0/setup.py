from setuptools import setup, find_packages
setup(
    name='fair-mobil-uwb',
    version='0.1.0',
    author='Michael Schwartz',
    author_email='mjschwa@uw.edu',
    description= {
        'Copy of the fair-mobil python package found here: https://pypi.org/project/fair-mobil/'
        'to create a new package containing all changes necessary for fairness research.'
    },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)