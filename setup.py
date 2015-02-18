from distutils.core import setup

version = '0.0.1'

with open('README.markdown') as readme:
    long_description = readme.read()

setup(
    name = 'clowder',
    version = version,
    description = 'Client for the Clowder monitoring server',
    long_description = long_description,
    author = 'Keith Hackbarth',
    author_email = 'keith@clowder.io',
    license = 'LICENCE.txt',
    url = 'https://github.com/keithhackbarth/clowder_client',
    py_modules = ['clowder'],
    download_url = 'https://github.com/keithhackbarth/clowder_client/archive/master.zip',
    platforms='Cross-platform',
    classifiers=[
      'Programming Language :: Python',
      'Programming Language :: Python :: 3'
    ],
    install_requires = [
        'requests_futures',
    ],
)
