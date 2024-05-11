from setuptools import setup 
import libreppc

VERSION = libreppc.__VERSION__
DESCRIPTION = 'A simple profile page creator.'

with open("README.md", "r") as ofile:
    LONG_DESCRIPTION = ofile.read()

packages = [
    'libreppc', 'libreppc.templates', 'libreppc.static'
]

# Setting up
setup(
    url="https://codeberg.org/librehub/libreppc",
    name="libreppc",
    version=VERSION,
    author="loliconshik3",
    author_email="loliconshik3@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=packages,
    include_package_data=True,
    install_requires=['flask', 'markdown', 'feedgen', 'pytz', 'pygments'], 
    keywords=['python', 'profile', 'html', 'css', 'markdown', 'profile page', 'page', 'site', 'personal page'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
