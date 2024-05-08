import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="texttotest", 
    version="0.0.1", 
    author="djumanovdev", 
    author_email="djumanovdev@gmail.com", 
    packages=["texttotest"], 
    description="A Python package to create tests from text file", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/djumanovdev/texttotest", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
)