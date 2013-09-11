from setuptools import setup, find_packages

setup(
    name = 'fundfind',
    version = '0.1',
    packages = find_packages(),
    url = 'http://fundfind.cottagelabs.com',
    author = 'Emanuil Tolev',
    author_email = 'emanuil.tolev@gmail.com',
    description = 'fundfind - an Open way to share, visualise and map out scholarly funding opportunities',
    license = 'MIT',
    # TODO look for other potentially useful classifiers
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = [
        'Flask==0.9',
        'Flask-Login==0.1.3',
        'Flask-WTF==0.8.2',
        'pyes==0.16',
        'requests==1.1.0',
        'parsedatetime==0.8.7',
    ],
)

