from setuptools import setup, find_packages

with open(r"F:\akash\python_package\extensionmigrationassistant\assessment\readme.md" , "r") as file:
    long_description = file.read()

with open(r"F:\akash\python_package\extensionmigrationassistant\LICENSE.txt", "r") as file:
    licence = file.read()

setup(
    name = "extensionmigrationassistant",
    version = "0.1.0", 
    author = "DataCloudGaze",
    author_email = "contact@datacloudgaze.com",
    description = "Description of your package",
    long_description = long_description,
    long_description_content_type ="text/markdown",
    licence = licence,
    url = "https://github.com/dcgadmin/extensionmigrationassistant.git",
    package_dir={"": "."},  
    packages=find_packages(),
    python_requires = ">=3.0",
    install_requires = [
                        "Jinja2",
                        "matplotlib",
                        "numpy",
                        "pandas",
                        "psycopg2",
                        "SQLAlchemy"
                        ],

    entry_points = {"console_scripts": ["extension-assisstant=assessment.assessment:main"]},                                       
    include_package_data = True,
    classifiers = [
                    "Programming Language :: Python :: 3",
                    "Development Status :: 4 - Beta",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent",
                    "Environment :: Console"
                    ],

)
