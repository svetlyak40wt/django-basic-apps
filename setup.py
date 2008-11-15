from setuptools import setup, find_packages

packages = ['basic.%s' % package for package in find_packages()]
packages.insert(0, 'basic')

setup(
    name = 'django-basic-apps',
    version = '0.1.0',
    description = 'Collection of general purpose application for Django.',
    keywords = 'django apps',
    license = '',
    author = 'Nathan',
    author_email = 'nathan@playgroundblues.com',
    maintainer = 'Alexander Artemenko',
    maintainer_email = 'svetlyak.40wt@gmail.com',
    url = 'http://github.com/svetlyak40wt/django-basic-apps/',
    install_requires = [],
    dependency_links = [],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = packages,
    package_dir = {'basic': '.'},
    package_data = {'basic': ['*/templates/*/*.html']},
    include_package_data = True,
)

