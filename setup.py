"""
Flask-MITOAuth2
---------------

Flask extension for authenticating users against MIT OAuth2
service.
"""
import io
from setuptools import setup, find_packages


with io.open('LICENSE') as f:
    license = f.read()

setup(
    name='Flask-MITOAuth2',
    version='0.0.1',
    url='http://github.com/MITLibraries/flask-mitoauth2',
    license=license,
    author='Mike Graves',
    author_email='mgraves@mit.edu',
    description='Flask extension for MIT OAuth2 authentication',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Flask',
        'PyJWT',
        'Flask-OAuthlib'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ]
)
