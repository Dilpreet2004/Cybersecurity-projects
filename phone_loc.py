import os
from dotenv import load_dotenv
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
load_dotenv()

print("--------PHONE NUMBER TRACKER--------")
number = input("Enter the phone number: ")
key = os.environ.get("GEOCODER_KEY")
pepnumber = phonenumbers.parse(number)
location = geocoder.description_for_number(pepnumber,"en")
print(location)
print(carrier.name_for_number(pepnumber,"en"))

query = str(location)
Opencage = OpenCageGeocode(key)
res = Opencage.geocode(query)
lat = res[0]['geometry']['lat']
lng = res[0]['geometry']['lng']
print(f"latitude:{lat} longitude:{lng}")
print("disclaimer: location is based on registration, Not the real GPS location")

myMap = folium.Map(location=[lat,lng],zoom_start=9)
folium.Marker([lat,lng],popup=location).add_to(myMap)
myMap.save("location.html")
print("saved location to file: 'location.html")
