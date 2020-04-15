DATA_FOLDER="$HOME/.srtm30"

if [ ! -d $DATA_FOLDER ]
then
    mkdir $DATA_FOLDER
fi

wget --continue -r -P $DATA_FOLDER -nd -A "*.dem.zip","*.hdr.zip" https://dds.cr.usgs.gov/srtm/version2_1/SRTM30/
unzip "$DATA_FOLDER/*.zip" -d $DATA_FOLDER
