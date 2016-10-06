from setuptools import setup, find_packages

setup(
    name='django-media-manager',
    version='3.4.1',
    description='Media-Management with the Django Admin-Interface.',
    author=['Patrick Kranzlmueller','Six Foot'],
    author_email='dev@6ft.com',
    url='https://github.com/oliverseal/django-media-manager',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = [
        "Django>=1.8",
        "pillow",
    ],
)
