import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:
        return  'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location = [38.58, -99.08], zoom_start = 3, tiles = "Stamen Terrain") 

fg1 = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, nm, el in zip(lat,lon,name,elev):
    iframe = folium.IFrame(html=html % (nm, nm, el), width=200, height=100)
    fg1.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, popup=folium.Popup(iframe), fill_color = color_producer(el), color = 'grey', fill_opacity = 0.7))

fg2 = folium.FeatureGroup(name = "Population")

fg2.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(), 
style_function = lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fg1)
map.add_child(fg2)
map.add_child(folium.LayerControl())

map.save("Map1.html")