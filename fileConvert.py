import pandas as pd
import json

csv_path = "Data/display_energy_certificate_dcc_2025.csv"
df = pd.read_csv(csv_path)

features = []
for _, row in df.iterrows():
    properties = {col: str(row[col]) for col in df.columns}
    feature = {
        "type": "Feature",
        "properties": properties,
        "geometry": None  
    }
    features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

output_path = "Data/display_energy_certificate_2025.geojson"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, indent=2, ensure_ascii=False)

print(f"file generated: {output_path}")
