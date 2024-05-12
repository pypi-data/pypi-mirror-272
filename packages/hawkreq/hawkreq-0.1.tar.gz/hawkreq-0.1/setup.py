from setuptools import setup, find_packages

setup(
    name='hawkreq',
    version='0.1',
    packages=find_packages(),
    description='A Python package to install external libraries',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/your_username/your_package',
    entry_points={
        'console_scripts': [
            'hawkreq = hawkreq:main'
        ]
    },
    install_requires=[],
)
