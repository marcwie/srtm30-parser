wget --continue -r -P srtm30 -nd -A "*.dem.zip","*.hdr.zip" https://dds.cr.usgs.gov/srtm/version2_1/SRTM30/
unzip "srtm30/*.zip" -d srtm30/
