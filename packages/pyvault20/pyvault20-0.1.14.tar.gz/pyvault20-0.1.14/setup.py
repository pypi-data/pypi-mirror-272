import setuptools

with open("README.md", "r") as file:
    readme = file.read()

setuptools.setup(
    name="pyvault20",
    version="0.1.14",
    description="Vault encryption tool.",
    url="https://github.com/thecodeforge/pyvault",
    py_modules=["pyvault"],
    install_requires=[
        "pychacha",
        "pyyaml",
        "requests",
        "rsa",
        ],
    packages=setuptools.find_packages(),
    package_dir={
        "pyvault":"pyvault"
    },
    python_requires= '>=3.11',
    long_description = readme,
    long_description_content_type = "text/markdown",
    entry_points = {
        "console_scripts": ["pyvault = pyvault.command_line:main"]
    }
)