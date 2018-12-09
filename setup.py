import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IdentiCyte",
    version="1.0",
    author="Guillaume Garnier",
    author_email="guillaume.garnier@monash.edu",
    description="A package to count and classify cells in an image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IdentiCyte/IdentiCyte",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib>=3.0.2',
                      'mttkinter>=0.6.1',
                      'numpy>=1.15.4',
                      'opencv-python>=3.4.3.18',
                      'Pillow>=5.3.0',
                      'scikit-learn>=0.20.0',
                      'scipy>=1.1.0',
                      'sklearn>=0.0',
                      'XlsxWriter>=1.1.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL 3.0 or later",
        "Operating System :: OS Independent",
    ],
)
