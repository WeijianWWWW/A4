from geopy.geocoders import GoogleV3
import json, time

API_KEY = "AIzaSyBQolK7_qssb1T2n7LHGn8YjBSDVdZfwUg"
input_file = "Data/display_energy_certificate_2025.geojson"
output_file = "Data/dcc_2025_with_coords.geojson"

geolocator = GoogleV3(api_key=API_KEY)
#read data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])

#look for geo coordinates
for feature in features:
    props = feature.get("properties", {})
    building_name = props.get("Building")
    if not building_name:
        continue

    try:
        query = f"{building_name}, Dublin, Ireland"
        location = geolocator.geocode(query, timeout=10)

        if location:
            lon, lat = location.longitude, location.latitude
            feature["geometry"] = {"type": "Point", "coordinates": [lon, lat]}
            print(f"{building_name} → {lat:.5f}, {lon:.5f}")
        else:
            print(f"cannot locate: {building_name}")
    except Exception as e:
        print(f"error: {building_name}, reason: {e}")
        continue

    time.sleep(0.5)  

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"file generated: {output_file}")
