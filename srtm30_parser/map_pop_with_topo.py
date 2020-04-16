from sedac_gpw_parser import population
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import os

file_lons = np.arange(-180, 180, 40)
file_lats = np.arange(90, -20, -50)
DATA_FOLDER = os.path.expanduser("~") + "/.srtm30/"

def get_population_data(country_id):
    
    pop = population.Population(country_id=country_id)
    pop.mask_invalid_data(below=0)

    data = pop.population_array()
    lat = pop.latitude_range()
    lon = pop.longitude_range()

    lonmin = lon.min()
    lonmax = lon.max()
    latmax = lat.max()
    latmin = lat.min()
    
    extent = (lonmin, lonmax, latmin, latmax)
        
    return data, extent


def get_infiles(lonmin, lonmax, latmin, latmax):
    print(lonmin, lonmax, latmin, latmax)

    lonmask = (file_lons >= (lonmin - 40)) & (file_lons <= lonmax)
    latmask = (file_lats >= latmin) & (file_lats <= (latmax + 50))
    valid_lons = file_lons[lonmask]
    valid_lats = file_lats[latmask]
    
    latmax = np.round(latmax + 1/120, 8) # Add 1/120 because topographic data is with respect to UPPER LEFT corner
    latmin = np.round(latmin + 1/120, 8) # Add 1/120 because topographic data is with respect to UPPER LEFT corner
    lonmin = np.round(lonmin, 8)
    lonmax = np.round(lonmax, 8)

    n_lat = int(np.round((latmax - latmin) * 120) + 1)
    n_lon = int(np.round((lonmax - lonmin) * 120) + 1)

    full_data = np.zeros((n_lat, n_lon))

    lat_offset = 0
    for valid_lat in valid_lats:
    
        #print(valid_lat, end="\r")

        file_lat_range = np.round(np.arange(valid_lat, valid_lat-50, -1/120), 8)
        valid_file_lat_range = (file_lat_range <= latmax) & (file_lat_range >= latmin)
        n_row = valid_file_lat_range.sum()

        lon_offset = 0
        for valid_lon in valid_lons:
            
            file_lon_range = np.round(np.arange(valid_lon, valid_lon+40, +1/120), 8)
            valid_file_lon_range = (file_lon_range <= lonmax) & (file_lon_range >= lonmin)
            n_col = valid_file_lon_range.sum()
            
            if valid_lon < 0:
                lon_pref = "W"
            else:
                lon_pref = "E"
            if valid_lat < 0:
                lat_pref = "S" 
            else:
                lat_pref = "N" 

            infile = lon_pref + str(abs(valid_lon)).zfill(3) + lat_pref + str(abs(valid_lat)).zfill(2) + ".DEM"
           
            with open(DATA_FOLDER+infile) as infile:
                data = np.fromfile(infile, np.dtype('>i2')).reshape(6000, 4800)
          
            print(valid_lat, valid_lon, "cutting data")
            data = data[valid_file_lat_range]
            data = data[:, valid_file_lon_range]
            print("storing data")
            full_data[lat_offset:lat_offset+n_row,lon_offset:lon_offset+n_col]=data

            lon_offset += n_col
            
            del data

        lat_offset += n_row

    return full_data

def truncate_colormap(cmap, minval=0.25, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def get_topomap():
    colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 2))
    colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))
    all_colors = np.vstack((colors_undersea, colors_land))
    terrain_map = colors.LinearSegmentedColormap.from_list('terrain_map', all_colors)

    terrain_map = truncate_colormap(cmap=plt.get_cmap('terrain'))
    terrain_map.set_under("#254DB3")
    terrain_map.set_bad("0.5")
    
    return terrain_map


def main(country_id, plot=True):
    pop, extent = get_population_data(country_id=country_id)
    lonmin, lonmax, latmin, latmax = extent
    print("Getting topography data from disk...")
    topo_data = get_infiles(lonmin, lonmax, latmin, latmax)
 

    print("Removing empty cols")
    contains_values = []
    for col_id in range(pop.shape[1]):
        print(col_id, pop.shape[1], end="\r")
        if np.isfinite(pop[:, col_id]).any():
            contains_values.append(col_id)

    print(len(contains_values), pop.shape)
    pop = pop[:, contains_values]
    topo_data = topo_data[:, contains_values]

    print("Removing empty rows")
    contains_values = []
    for row_id in range(pop.shape[0]):
        print(row_id, pop.shape[1], end="\r")
        if np.isfinite(pop[row_id]).any():
            contains_values.append(row_id)

    print(len(contains_values), pop.shape)
    pop = pop[contains_values]
    topo_data = topo_data[contains_values]

    print("setting invalid values...")
    #for i, _pop in enumerate(pop):
    #    print(i, len(pop), end="\r")
    topo_data[np.isnan(pop)] = np.nan

    if plot:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 9))
        
        terrain_map = get_topomap()
        
        ax1.imshow(topo_data, vmin=0, vmax=4000, cmap=terrain_map, rasterized=True)
        ax2.imshow(pop, vmin=0, vmax=100)
    
    return pop, topo_data


def distribution(pop, topo, plot=True):

    mask = np.isfinite(topo)
    topo = topo[mask]
    pop = pop[mask]

    #valid_topo = np.arange(topo.min(), topo.max() + 1, 100)
    valid_topo = np.arange(0, 41, 1)
    results = np.zeros_like(valid_topo, dtype=float)
    
    #total_population = pop.total_population()
   
    for i, elevation in enumerate(valid_topo):
        mask = topo <= elevation
        #mask = topo == elevation
        results[i] = pop[mask].sum() 
       
    total_population = np.sum(pop)
    results /= total_population

    #results = results.cumsum() / total_population

    print(results)

    if plot:
    #plt.semilogy()
        plt.plot(valid_topo, results)
        plt.xlabel("Elevation x [m above sea level]")
        plt.ylabel("Share of population living at or below x")

    return valid_topo, results


if __name__ == "__main__":
    pop, topo = main(840, plot=False)
    distribution(pop, topo, plot=False)
