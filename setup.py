import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccjtools",
    version="0.1.0",
    author="Nik Langrind",
    author_email="langrind@gmail.com",
    description="Scripts for working with JSON compilation databases for clang etc.",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/langrind/ccjtools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=['bin/ccj-make', 'bin/ccj-xform-ap', 'bin/ccj-xform-px4'],
)
