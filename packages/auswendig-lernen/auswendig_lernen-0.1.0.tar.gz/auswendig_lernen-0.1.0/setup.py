from setuptools import setup, find_packages

setup(
    name='auswendig_lernen',
    version='0.1.0',
    author='Torrez',
    author_email='that1.stinkyarmpits@gmail.com',
    description='To memorise a list of words in an order.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your package dependencies here
    ],
    entry_points={
        'console_scripts': [
            'auswendiglernen = auswendiglernen.__main__:main'
        ]
    },
)
