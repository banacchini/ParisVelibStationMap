import json
import branca
import requests
import folium




info_request = requests.get("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json")
status_request = requests.get("https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json")

try:
    stations_info = info_request.json()
    stations_status = status_request.json()

except:
    with open('station_information.json', 'r') as f:
        stations_info = json.load(f)

    with open('station_status.json', 'r') as f:
        stations_status = json.load(f)

stations = stations_status['data']['stations']


def get_bike_info(station_id):
    for station in stations:
        if station['station_id'] == station_id:
            return [station['numBikesAvailable'], station['numDocksAvailable']]


m = folium.Map(location=[48.85737182651027, 2.347378276014453], zoom_start=15)

radius = 10

for station in stations_info['data']['stations']:
    bike_info = get_bike_info(station['station_id'])
    html = f"""
    <h2>{station['name']}</h2>
    <p>
    <b>Bikes Available:</b> {bike_info[0]}<br>
    <b>Docks Available:</b> {bike_info[1]}
    </p>
    """
    iframe = branca.element.IFrame(html=html, width=300, height=150)

    folium.CircleMarker(
        location=[station['lat'], station['lon']],
        radius = radius,
        color = 'cornflowerblue',
        stroke = False,
        fill = True,
        fill_opacity = 0.6,
        opacity = 1,
        popup = folium.Popup(iframe),
    ).add_to(m)

m.show_in_browser()