from setuptools import setup
from setuptools import find_packages

setup(
    name='sssm',
    version='0.0.2',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'requests',
        'importlib-metadata',
        'torch',
        'pandas',
        'einops',
        'seaborn',
        'numpy',
        'scipy',
        'matplotlib',
    ],
)
