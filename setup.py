import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setuptools.setup(name="tltsne",
                 version="0.0.1",
                 author="Vojtech Spiwok",
                 author_email="spiwokv@vscht.cz",
                 description="Time-lagged t-SNE of molecular trajectories",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/spiwokv/tltsne",
                 classifiers=[
                     "Programming Language :: Python",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Development Status :: 2 - Pre-Alpha",
                     "Topic :: Scientific/Engineering :: Chemistry",
                 ],
                 packages=["tltsne"],
                 scripts=["bin/tltsne"],
                 install_requires=[
                     "scipy",
                     "sklearn",
                     "pyemma",
                     "mdtraj",
                     "argparse",
                     "datetime",
                     "codecov",
                 ],
                 include_package_data=True,
                 zip_safe=False
)

