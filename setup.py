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
    url="https://Get an online repo",
    packages=setuptools.find_packages(),
    install_requires=['numpy',
                      'scipy',
                      'opencv-python',
                      'XlsxWriter',
                      'scikit-learn',
                      'sklearn',
                      'Pillow',
                      'mttkinter',
                      'matplotlib'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
