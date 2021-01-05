# srtm30-parser
A framework to work with SRTM30 near-global digital elevation data, i.e., a combination of data from the Shuttle Radar Topography Mission and the U.S. Geological Survey's GTOPO30 data set. 

This package is work in progress and currently updated frequently.

A documentation of the data is found here: https://dds.cr.usgs.gov/srtm/version2_1/SRTM30/srtm30_documentation.pdf

# Installation

This package only works with `python3`. To install just type:
```
git clone git@github.com:marcwie/srtm30-parser.git
cd srtm30-parser
python setup.py install
```

# Usage

1. Download the necessary raw input files by typing `download-srtm30-data.sh`. All file will be stored in a special folder `.srtm30` in your home directory. 
   After succesfully downloading the data the structure of `.srtm30` should look like this:    
    ```
    .srtm30/
    ├── E020N40.DEM
    ├── e020n40.dem.zip
    ├── E020N40.HDR
    ├── e020n40.hdr.zip
    ├── ...
    ├── W180S10.HDR
    └── w180s10.hdr.zip
    ```

2. A minimal working example for loading the data and processing it for further usage looks like so:
   ```python
   from srtm30_parser import elevation                                             

   data = elevation.Elevation(lonmin=5, lonmax=6, latmin=5, latmax=6)              
   data_table = data.as_list()                                                     
   print(data_table)                                                                                       
   ```
Note that allowed values for longitudes range from -180 to 180 and allowed values for latitudes range from -90 to 90. `data.as_list()` return a table with three colunms (longitude, latitude, elevation). Note that (longitude, latitude) refer to the position of the lower left corner of each grid cell.
A quick-and-dirty sanity check can be done by saving the data as an image:
   ```python
   from srtm30_parser import elevation                                             

   data = elevation.Elevation(lonmin=5, lonmax=6, latmin=5, latmax=6)              
   data.plot(filename="out.png")                                                                                      
   ```
The plot does not look pretty but it serves its purpose.
