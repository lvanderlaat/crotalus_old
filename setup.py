from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name             = 'crotalus',
    version          = '0.1',
    description      = 'Volcano seismicity analysis',
    long_description =  readme(),
    url              = 'http://github.com/lvanderlaat/crotalus',
    author           = 'Leonardo van der Laat',
    author_email     = 'leonardo.vanderlaat.munoz@una.cr',
    packages         = ['crotalus'],
    install_requires = [
    ],
    scripts          = [
        'bin/crotalus-web'
    ],
    zip_safe         = False
)
