from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='test-pkhan-12345',  # Updated package name
    version='0.5.0',
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
    long_description=long_description,
    long_description_content_type='text/markdown',
)