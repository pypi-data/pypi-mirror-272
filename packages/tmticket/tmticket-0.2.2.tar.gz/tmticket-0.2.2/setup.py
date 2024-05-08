from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='tmticket',
    version='0.2.2',
    author='hokiebrian',
    author_email='hokiebrian@gmail.com',
    description="Python wrapper for the Ticketmaster Discovery API",
    #long_description=read('README.rst'), 
    license='MIT',
    keywords='Ticketmaster API',
    url='https://github.com/hokiebrian/pytmtickets',
    packages=['tmticket'],
    install_requires=['aiohttp', 'requests'],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
