import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_prod(height):
    if height < 1000:
        return 'green'
    elif 1000 <=height < 3000:
        return 'orange'
    else:
        return 'red'

html = """<h4>Volcano information:</h4>
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Elevation: %s m
"""

map =  folium.Map(location=[39.838519, -114.089139], zoom_start=5, tiles="Stamen Terrain")

fgv=folium.FeatureGroup(name="Volcanoes in the US")

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 6, 
    popup=folium.Popup(iframe, parse_html=True), fill_color=color_prod(el), color = 'grey', fill_opacity = 0.7))

fgp=folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red' }))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")