import requests
import folium

def get_current_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        location = data['loc'].split(',')
        lat, lng = float(location[0]), float(location[1])
        city = data.get('city', 'Unknown City')
        region = data.get('region', 'Unknown Region')
        print(f"Detected Current Location: {city}, {region}")
        print(f"Latitude: {lat}, Longitude: {lng}")
        
        my_map = folium.Map(location=[lat, lng], zoom_start=12)
        folium.Marker([lat, lng], popup=f"{city}, {region}").add_to(my_map)
        
        file_name = "current_location.html"
        my_map.save(file_name)
        print(f"Map saved to {file_name}")
        
    except Exception as e:
        print(f"Error fetching location: {e}")

get_current_location()