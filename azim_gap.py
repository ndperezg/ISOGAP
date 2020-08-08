import numpy as np
import nvector as nv
import sys

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

def each_gap(lon,lat,net):
	azz=[]
	for sta in net:
		azim = azimuth(lon,lat,net[sta][0], net[sta][1])
		azz.append(azim)
	GAP = max(gaps(azz))
	return GAP

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

#--------WORKOUT--------

arc = sys.argv[1]
NET = read_stations(arc)
grid = float(raw_input('Ingrese el espaciamiento de la grilla en grados\n'))
lons = np.arange(-80,-67,grid)
lats = np.arange(-1,14,grid)
out = open('salida_%s_grid.csv'%grid, 'w')
out.write('LON,LAT,GAP\n')

for i in lons:
	for j in lats:
		az_gap = each_gap(i,j,NET)
		print(i,j,az_gap)
		out.write('%s,%s,%4.2f\n'%(i,j,az_gap))

out.close()

