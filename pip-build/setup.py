import os
import setuptools

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as file:
        return file.read()

install_requires = read("requirements.txt")
install_requires = install_requires.split("\n")
install_requires = list(filter(lambda x: x[0:1] != "#", install_requires))
print("install-requires:", install_requires)

setuptools.setup(
    name = "mdpyformat",
    version = "1.0.1",
    author = "Michael Moser",
    author_email = "moser.michael@gmail.com",
    description = ("mdformat is a literate programming framework for python."),
    license = "MIT",
    keywords = "utility",
    url = "https://github.com/MoserMichael/python-obj-system",
    package_dir={'': 'src'},
    packages=setuptools.find_packages("src"),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Software Development :: Documentation"
    ],
    python_requires='>=3.6',
)
