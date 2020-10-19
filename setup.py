from setuptools import setup, find_packages

setup(
    name='spid-django',
    packages=find_packages(exclude='example'),
    include_package_data=True,
    zip_safe=False,
    version='0.1.0',
    description='Spid authentication app for django',
    author='Marco Federighi',
    author_email='federighi.marco@gmail.com',
    url='https://github.com/italia/spid-django',
    keywords=['django', 'authentication', 'spid', 'italia'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
    ],
)
