from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'The ultimate PyPi package for cyber-security and many other things.'
LONG_DESCRIPTION = '''The ultimate PyPi package for cyber-security, encryption, and many other things to simplify your code and make more advanced programs.

RELEASE NOTES: \n
v1.0.0: \n
- Initial release \n
- NOTE: Encryption and logging are both empty for this first version. \n
- v1.0.1 coming very soon. \n
'''

# Setting up
setup(
        name="dreamhack", 
        version=VERSION,
        author="Jack Burr",
        author_email="BurrJ22@Outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['cryptography', 'tqdm', 'setuptools'], 
        keywords=['python', 'windows'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)