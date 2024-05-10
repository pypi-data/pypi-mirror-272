from setuptools import setup


from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Basic Hello Package'

# Setting up
setup(
    name="pyharsh",
    version=VERSION,
    author="Harsh Vadhiya",
    author_email="harshvadhiya144@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
