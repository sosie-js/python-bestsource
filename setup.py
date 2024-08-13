from setuptools import setup, find_packages# List of requirements

with open("README.md", 'r') as fh:
    long_description = fh.read()

requirements = [ "setuptools"]  # This could be retrieved from requirements.txt# Package (minimal) configuration

setup(
    name="python-bssource",
    version="1.0.0",
    description="Python helpers to manipulate video from vapoursynth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Olivier Lutzwiller",
    author_email="sosie@sos-productions.com",
    keywords="vapoursynth python bestsource helper",
    url="http://github.com/sosie-js/python-bssource",
    license='GPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(),  # __init__.py folders search
    install_requires=requirements,
    python_requires='>=3.10',
)

