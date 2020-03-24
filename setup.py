import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="srtm30_parser", # Replace with your own username
    version="0.1",
    author="Marc Wiedermann",
    author_email="marcwie@pik-potsdam.de",
    description="A framework to work with SRTM30 near-global digital elevation data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcwie/srtm30-parser",
    packages=setuptools.find_packages(include=("srtm30_parser",)),
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    #],
    scripts=("bash_scripts/download-srtm30-data.sh", ),
    python_requires='>=3',
    #setup_requires=['numpy', 'cython'], # This is needed for proper install of cartopy
    #install_requires=['numpy', 
    #                  'matplotlib', 
    #                  'cartopy', 
    #                  'scipy',      # Scipy is required for cartopy to work
    #                  'shapely<=1.6.4.post2']  
    )
