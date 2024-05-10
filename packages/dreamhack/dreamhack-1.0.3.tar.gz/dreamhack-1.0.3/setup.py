from setuptools import setup, find_packages

VERSION = '1.0.3' 
DESCRIPTION = 'The ultimate PyPi package for cyber-security and many other things.'
LONG_DESCRIPTION = '''The ultimate PyPi package for cyber-security, encryption, and many other things to simplify your code and make more advanced programs.

*DISCLAIMER* I am not responsible for any damages caused by this package. Please do not use any features of this package for any bad purposes.

RELEASE NOTES: \n
v1.0.3: \n
- Added logging content \n
- Added the ability to get the public ip of the current machine \n
- Added lots of new features \n
- A few bug fixes

v1.0.2: \n
- First official stable version, DO NOT USE PREVIOUS VERSIONS \n
- Added content to encryption and logging \n
- Created networking \n
\n
WARNING: VERSIONS BELOW THIS NOTE ARE UNSTABLE. DO NOT USE THEM.
\n
v1.0.1: \n
- Fixed critical error from v1.0.0 \n
- Working on new version \n

v1.0.0: \n
- Initial release \n
- NOTE: Encryption and logging are both empty for the first few versions. \n
'''

setup(
        name="dreamhack", 
        version=VERSION,
        author="Jack Burr",
        author_email="BurrJ22@Outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['cryptography', 'tqdm', 'setuptools', 'pyuac', 'requests', 'public-ip', 'keyboard', 'pyautogui', 'customtkinter', 'CTkMessagebox'],  #type:ignore
        keywords=['python', 'windows'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)