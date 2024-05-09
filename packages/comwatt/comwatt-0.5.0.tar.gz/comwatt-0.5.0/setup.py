from setuptools import setup, find_packages

setup(
    version='0.5.0',
    name='comwatt',
    description='Python client for Comwatt',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Christophe Godart',
    author_email='51CGO@armaghast.eu',
    install_requires=['selenium'],
    url='https://github.com/51CGO/comwatt',
    keywords=['Comwatt', 'client'],
    packages=['comwatt']
)
