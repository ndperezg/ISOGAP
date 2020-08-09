#                           ISOGAP 0.1
#This script calculates the primary azimuthal gap for a certain network geometry
#Input:
#- A csv file with station name, longitude and latitude columns
#- Corners of a rectangle to create the grided area
#- Grid step
## Author: Nelson David Perez e-mail:ndperezg@gmail.com 


import numpy as np
import nvector as nv
import sys

#Calculates gaps for a list of azimuths 
def gaps(Azz):
	azz = sorted(Azz)
	gaps_ = []
	for i in range(len(azz)):
		if i != 0:
			alpha = azz[i]-azz[i-1]
		else:
			alpha = azz[0]+ 360 - azz[-1]
		gaps_.append(alpha)
	return gaps_

#Calculates azimuths between two points
def azimuth(Lon1,Lat1,Lon2,Lat2):
	wgs84 = nv.FrameE(name='WGS84')
	pointA = wgs84.GeoPoint(latitude=Lat1, longitude=Lon1, z=0, degrees=True)
	pointB = wgs84.GeoPoint(latitude=Lat2, longitude=Lon2, z=0, degrees=True)
	p_AB_N = pointA.delta_to(pointB)
	azim = p_AB_N.azimuth_deg[0]
	if azim < 0:
		azim += 360
	else:
		pass
	return azim

#calculates isogap for each point
def each_gap(lon,lat,net):
	azz=[]
	for sta in net:
		azim = azimuth(lon,lat,net[sta][0], net[sta][1])
		azz.append(azim)
	GAP = max(gaps(azz))
	return GAP

#reads stations file
def read_stations(arc):
	with open(arc) as fl:
		count = 0
		NET = {}
		for line in fl.readlines():
			point=[]
			if count > 0:
				sta = line.strip().split(',')[0]
				lon = float(line.strip().split(',')[1])
				lat = float(line.strip().split(',')[2])
				point.append(lon)
				point.append(lat)
				NET[sta] = point
			count += 1
	return NET


#Ask for longitudes and latitudes for the study area
def input_area():
	lons= raw_input("Enter min and max longitudes separated by a comma:\n")
	lats= raw_input("Enter min and max latitudes separated by a comma:\n")
	if len(lons.split(','))!=2 or len(lats.split(','))!=2:
		print("Bad input, try again\n")
		sys.exit()
	minlon = float(lons.split(',')[0])
	maxlon = float(lons.split(',')[1])
	minlat = float(lats.split(',')[0])
	maxlat = float(lats.split(',')[1])
	if (minlon>=maxlon) or (minlat>=maxlat):
		print("Wrong values, try again\n")
		sys.exit()
	return minlon, maxlon, minlat, maxlat

#--------WORKOUT--------
if len(sys.argv)<2:
	print("No input file\n")
	sys.exit()

arc = sys.argv[1]
NET = read_stations(arc)
minlon, maxlon, minlat, maxlat = input_area()
grid = float(raw_input('Enter grid step in degrees:\n'))
Lons = np.arange(minlon,maxlon,grid)
Lats = np.arange(minlat,maxlat,grid)
#Lons = np.arange(-80,-67,grid)
#Lats = np.arange(-1,14,grid)
out = open('output_%s_grid.csv'%grid, 'w')
out.write('LON,LAT,GAP\n')

for i in Lons:
	for j in Lats:
		az_gap = each_gap(i,j,NET)
		print(i,j,az_gap)
		out.write('%s,%s,%4.2f\n'%(i,j,az_gap))

out.close()

