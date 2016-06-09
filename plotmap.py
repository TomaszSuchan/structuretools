#! /usr/bin/env python3
try:
    import pandas
except ImportError:
    raise ImportError("Pandas package not found, please install using: pip3 install pandas")

try:
    import palettable
except ImportError:
    raise ImportError("Palettable package not found, please install using: pip3 install palettable")

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("Matplotlib package not found, please install using: pip3 install matplotlib")

try:
    import numpy as np
except ImportError:
    raise ImportError("Numpy package not found, please install using: pip3 install matplotlib")

try:
    from mpl_toolkits.basemap import Basemap
except ImportError:
    raise ImportError("Basemap package not found, please install from https://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/")

try:
    from palettable.tableau import Tableau_10
except ImportError:
    raise ImportError("Basemap package not found, please install using: pip3 install palettable")

import math
import argparse

def parse_args():
    # Parse arguments
    parser = argparse.ArgumentParser(
            description='Produces a map from str2map.py output.')

    parser.add_argument('-i',
            type=argparse.FileType('r'),
            dest='input',
            default='-',
            help='Input file or STDIN (default), with pop, lon, lat and population assigment columns; as produced by str2map.py script.')
            
    parser.add_argument('-o',
            type=str,
            dest='output',
            help='Output file name; supports png, pdf, ps, eps and svg.')

    parser.add_argument('-c',
            dest='coords',
            default=False,
            action='store_true',
            help='Uses point coordinates to calculate map extent. If not provided, the extent is Europe.')

    parser.add_argument('-p',
            dest='piesize',
            default=300,
            type=int,
            help='Size of the piecharts; default = 300.')

    parser.add_argument('-a',
            dest='alpha',
            default=1.0,
            type=float,
            help='Opacity of piecharts; 0.0 transparent through 1.0 opaque (default).')

    return parser.parse_args()

def draw_pie(ax, ratios, X, Y, size, alpha):
    N = len(ratios)
    colors = Tableau_10.mpl_colors
    
    xy = []
 
    start = 0.
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start, 2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start, 2*math.pi*(start+ratio), 30)).tolist()
        xy1 = list(zip(x,y))
        xy.append(xy1)
        start += ratio
 
    for i, xyi in enumerate(xy):
        ax.scatter([X], [Y], marker=(xyi,0), s=size, facecolor=colors[i], zorder=3, alpha=alpha)

def rendermap(llLon=-11.0, llLat=34.0, urLon=40.0, urLat=71.5, projection='mill', drawgrid=False):
    '''Draws a map in Lambert Equal Area projection.
    Takes the map extent in the form of lower left corner lon/lat, upper right corner lon/lat.
    Has options to show geographical grid and save the resulting file.
    '''
    lat0 =  (urLat - llLat) / 2 + llLat # def 51.0
    lon0 =  (urLon - llLon) / 2 + llLon # def 13.0
    
    map=Basemap(llcrnrlon=llLon, \
            llcrnrlat=llLat, \
            urcrnrlon=urLon, \
            urcrnrlat=urLat, \
            llcrnrx=None, \
            llcrnry=None, \
            urcrnrx=None, \
            urcrnry=None, \
            width=None, \
            height=None, \
            projection=projection, \
            resolution='h', \
            area_thresh=1000, \
            rsphere=6370997.0, \
            ellps=None, \
            lat_ts=None, \
            lat_1=None, \
            lat_2=None, \
            lat_0=lat0, \
            lon_0=lon0, \
            lon_1=None, \
            lon_2=None, \
            o_lon_p=None, \
            o_lat_p=None, \
            k_0=None, \
            no_rot=True, \
            suppress_ticks=True, \
            satellite_height=35786000, \
            boundinglat=None, \
            fix_aspect=True, \
            anchor='C', \
            celestial=False, \
            round=False, \
            epsg=None, \
            ax=None)
    
    map.fillcontinents(color='darkgrey',lake_color='white')
    map.drawcountries(linewidth=0.5, antialiased=1, color='lightgrey')
    # Draw a map scale
    #map.drawmapscale(lon, lat, lon0, lat0, length=, zorder=5)
	
    if drawgrid == True:
    	map.drawparallels(np.arange(-90.,120.,10.),labels=[1,0,0,0],labelstyle='+/-',linewidth=0.1)
    	map.drawmeridians(np.arange(0.,420.,10.),labels=[0,0,0,1],labelstyle='+/-',linewidth=0.1)
     
    return map
    
def main():
    args = parse_args()

    pops = pandas.read_table(args.input, delim_whitespace=True)
    
    # Plot basemap
    if args.coords == True:
        #Compute map canvas + marigins
        urLat = pops.lat.max()
        urLon = pops.lon.max()
        llLat = pops.lat.min()
        llLon = pops.lon.min()
    
        w, h = urLon - llLon, urLat - llLat
    
        urLat = pops.lat.max() + 0.1 * w
        urLon = pops.lon.max() + 0.1 * h
        llLat = pops.lat.min() - 0.1 * w
        llLon = pops.lon.min() - 0.1 * h
        
        map = rendermap(llLon, llLat, urLon, urLat, drawgrid=True)
    else:
        map = rendermap(drawgrid=True)

    #Change the columns with assignment to proportions
    assignments = pops[pops.columns[3:pops.shape[1]]]
    #change to proportions
    total = assignments.sum(axis=1) #sum of rows
    assignments = assignments.div(total, axis='index')
    pops[pops.columns[3:pops.shape[1]]] = assignments
    
    ax = plt.subplot()
    for popx, pop in pops.iterrows():
        X, Y = map(pop.lon, pop.lat)
        # Get proportions
        proportions = list(pop[3:pop.shape[0]])
        # Plot piecharts
        draw_pie(ax,proportions, X, Y, size=args.piesize, alpha=args.alpha)
	
	# Save or show the plot
    if args.output:
    	plt.savefig(args.output, dpi=300)
    else:
    	plt.show()

if __name__ == "__main__":
    main()
