from setuptools import setup, find_packages

setup(
    name='test-pkhan-12345',  # Updated package name
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.13.3',
        'scipy>=0.19.1',
    ],
    entry_points={
        'console_scripts': [
            'pixegami_hello = pixegami_hello:hello',
        ],
    },
)