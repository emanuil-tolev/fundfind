from setuptools import setup, find_packages

setup(
    name = 'fundfind',
    version = '0.1',
    packages = find_packages(),
    install_requires = [
        "Flask==0.8",
        "Flask-Login",
        "Flask-WTF",
        "pyes==0.16",
        "requests",
        "parsedatetime==0.8.7"
				],
    url = 'TODO PUT URL HERE WHEN DEPLOYED',
    author = 'Emanuil Tolev',
    author_email = 'emanuil.tolev@gmail.com',
    description = 'fundfind - an Open way to share, visualise and map out scholarly funding opportunities',
    license = 'TODO PUT LICENCE HERE WHEN DECIDED',
    # TODO define classifiers when decided (also look for other potentially 
    # useful classifiers
    # classifiers = [
        # 'Development Status :: 3 - Alpha',
        # 'Environment :: Console',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Topic :: Software Development :: Libraries :: Python Modules'
    # ],
)

