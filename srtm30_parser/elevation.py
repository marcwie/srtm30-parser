import numpy as np
import os
from matplotlib import pyplot as plt

file_lons = np.arange(-180, 180, 40)
file_lats = np.arange(90, -20, -50)
DATA_FOLDER = os.path.expanduser("~") + "/.srtm30/"


class Elevation():

    def __init__(self, lonmin, lonmax, latmin, latmax):

        assert lonmin % 1 / 120 == 0
        assert lonmax % 1 / 120 == 0
        assert latmin % 1 / 120 == 0
        assert latmax % 1 / 120 == 0

        self._extent = [lonmin, lonmax, latmin, latmax]

        self._load()

    def _load(self):

        lonmin, lonmax, latmin, latmax = self._extent

        lonmask = (file_lons >= (lonmin - 40)) & (file_lons <= lonmax)
        latmask = (file_lats >= latmin) & (file_lats <= (latmax + 50))

        valid_lons = file_lons[lonmask]
        valid_lats = file_lats[latmask]

        n_lat_files = len(valid_lats)
        n_lon_files = len(valid_lons)

        full_data = np.zeros((n_lat_files * 6000, n_lon_files * 4800),
                             dtype=int)

        for i, valid_lat in enumerate(valid_lats):
            for j, valid_lon in enumerate(valid_lons):

                lon_pref = "W" if valid_lon < 0 else "E"
                lat_pref = "S" if valid_lat < 0 else "N"

                infile = DATA_FOLDER + lon_pref + \
                    str(abs(valid_lon)).zfill(3) + \
                    lat_pref + str(abs(valid_lat)).zfill(2) + ".DEM"

                data = np.fromfile(infile, np.dtype('>i2')).reshape(6000, 4800)
                full_data[i*6000:(i+1)*6000, j*4800:(j+1)*4800] = data

        lat_range = max(valid_lats) - np.arange(0, n_lat_files * 6000) / 120
        lon_range = min(valid_lons) + np.arange(0, n_lon_files * 4800) / 120

        # Substract 1 / 120 because in the original data each grid cell is
        # characzerized by its UPPER LEFT corner. Since we want everything
        # relative to the lower left corner we need to substract the size of
        # each cell from the latitude range
        lat_range -= 1 / 120

        # We round here because 1 / 120 is fractional
        required_lats = (lat_range.round(8) <= latmax) \
            & (lat_range.round(8) >= latmin)
        required_lons = (lon_range.round(8) <= lonmax) \
            & (lon_range.round(8) >= lonmin)

        full_data = full_data[required_lats, :][:, required_lons]
        lat_range = lat_range[required_lats]
        lon_range = lon_range[required_lons]

        self._data = full_data
        self._latitude_range = lat_range
        self._longitude_range = lon_range

    def plot(self, filename="out.png"):

        plt.imshow(self._data, rasterized=True)
        plt.savefig(filename)

    def as_list(self):

        lat_range = self._latitude_range
        lon_range = self._longitude_range
        data = self._data

        lat_list = np.repeat(lat_range, len(lon_range))
        lon_list = np.tile(lon_range, len(lat_range))

        return np.stack((lon_list, lat_list, data.flatten())).T


if __name__ == "__main__":

    elevation = Elevation(5, 6, 5, 6)
    data_list = elevation.as_list()
    print(data_list)

    elevation.plot()
