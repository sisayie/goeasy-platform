import gmplot 
import routes_data as rd

gmap3 = gmplot.GoogleMapPlotter(rd.lat[0], rd.lon[0], 13) 

#gmap3.scatter( rd.lat, rd.lon, '# FF0000', size = 40, marker = False ) 

gmap3.plot(rd.lat, rd.lon, 'cornflowerblue', edge_width = 2.5) 

gmap3.draw( "output/mapplot.html" )