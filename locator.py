import googlemaps
import folium
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.environ.get("GMAP_API")
gmaps = googlemaps.Client(key=API_KEY)

def get_precise_location():
    try:
        result = gmaps.geolocate(consider_ip=True)
        
        lat = result['location']['lat']
        lng = result['location']['lng']
        accuracy = result['accuracy']
        
        print(f"Precise Latitude: {lat}")
        print(f"Precise Longitude: {lng}")
        print(f"Accuracy: Within {accuracy} meters")

        # 3. Create a map focused on the precise point
        my_map = folium.Map(location=[lat, lng], zoom_start=15)
        folium.Marker(
            [lat, lng], 
            popup=f"Accuracy: {accuracy}m",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(my_map)
        
        # Add a circle to show the 'accuracy radius'
        folium.Circle(
            location=[lat, lng],
            radius=accuracy,
            color='blue',
            fill=True,
            fill_opacity=0.1
        ).add_to(my_map)

        my_map.save("precise_location.html")
        print("Success! Open 'precise_location.html' to see your exact spot.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_precise_location()