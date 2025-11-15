import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import Dash, html, dcc,Input,Output,dash

gdf_2022 = gpd.read_file("Data/dcc_2022_with_coords.geojson")
gdf_2022["Year"] = 2022
gdf_2023 = gpd.read_file("Data/dcc_2023_with_coords.geojson")
gdf_2023["Year"] = 2023
gdf_2025 = gpd.read_file("Data/dcc_2025_with_coords.geojson")
gdf_2025["Year"] = 2025

gdf_all = pd.concat([gdf_2022, gdf_2023, gdf_2025], ignore_index=True)
gdf_all.columns = gdf_all.columns.str.replace("�", "²", regex=False)
gdf_all.columns = gdf_all.columns.str.replace("m�", "m²", regex=False)




rating_order = ["A1","A2","A3","B1","B2","B3","C1","C2","C3","D1","D2","E1","E2","F","G"]
rating_colors = {
    "A1":"#2ca25f","A2":"#3cb371","A3":"#74c476",
    "B1":"#fddc5c","B2":"#fdae61","B3":"#f46d43",
    "C1":"#e6550d","C2":"#d7301f","C3":"#b30000",
    "D1":"#8b0000","D2":"#a50f15",
    "E1":"#bcbddc","E2":"#9e9ac8","F":"#756bb1","G":"#54278f"
}

df = pd.DataFrame({
    "Building": gdf_all["Building"],
    "Rating": gdf_all["Current Rating"],
    "Electricity": gdf_all["Electricity kWh/m²/yr"],
    "Heating": gdf_all["Heating kWh/m²/yr"],
    "CO2": gdf_all["kgCO2 indicator"],
    "Area": gdf_all["Total m²"],
    "Year": gdf_all["Year"],
    "Typical": gdf_all["Typical Building kWh/m²/yr"],  
    "NextIndicator": gdf_all["Next Rating Indicator"],   
    "lat": gdf_all.geometry.y,
    "lon": gdf_all.geometry.x
})
for col in ["Electricity", "Heating", "CO2", "Area", "Typical", "NextIndicator"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df["Electricity"] = df["Electricity"].clip(upper=df["Electricity"].quantile(0.95))
df["Rating"] = pd.Categorical(df["Rating"], categories=rating_order, ordered=True)
df["TotalEnergy"] = df["Electricity"] + df["Heating"]

# ---------------- Figure Starts --------------------------------------------------------------------------------
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    color="Rating",
    size="TotalEnergy",
    size_max=25,
    hover_name="Building",
    hover_data={"Heating": True, "CO2": True, "Area": True, "Year": True},
    animation_frame="Year",
    zoom=11,
    custom_data=["Building","Year"],
    category_orders={"Rating": rating_order},
    color_discrete_map=rating_colors,
)
fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend=dict(title="Energy Rating",x=0.89, y=1,bgcolor="rgba(255,255,255,0.7)",bordercolor="rgba(0,0,0,0.2)",borderwidth=1,font=dict(size=12),itemsizing="constant" ),
    legend_tracegroupgap=0,
    mapbox=dict(
        center=dict(lat=53.35, lon=-6.27),
        zoom=11,
        domain={"x": [0.0, 1.0], "y": [0, 1.0]} 
    ),
     sliders=[{
        "pad": {"b": -10, "t": 0}, 
        "len": 0.88,
        "x": 0.06,
        "xanchor": "left",
        "y": 0.03,  
        "yanchor": "bottom"
    }],
    updatemenus=[{
        "buttons": [
            {"args": [None, {"frame": {"duration": 1200, "redraw": True}, "fromcurrent": True}],
             "label": "▶ Play", "method": "animate"},
            {"args": [[None], {"frame": {"duration": 0}, "mode": "immediate", "transition": {"duration": 0}}],
             "label": "⏸ Pause", "method": "animate"}
        ],
        "direction": "left",
        "pad": {"r": 10, "t": -30},  
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "left",
        "y": 0.01,
        "yanchor": "bottom"
    }]
)


#------------------Figure 1 finished-----------------------------------------------------------------------------


# ---------------- Dash layout ----------------
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        
        #figure 1 layout
        html.Div
        ([
            html.Div(
        "Dublin City Council Building Performance (2022–2025)",
        style={
            "position": "absolute",      
            "top": "8px",                 
            "left": "500px",                
            "transform": "translateX(-50%)",
            "zIndex": "10",               
            "color": "#1f3b64",
            "fontWeight": "bold",
            "fontSize": "18px",
            "background": "rgba(255,255,255,0.3)",  
            "padding": "4px 10px",
            "borderRadius": "5px"
        }
    ),
            dcc.Graph(figure=fig, id="map",style={"height": "100%", "width": "100%","padding":"0px"},config={"displayModeBar": False})
        ], style={
            "width": "65%",
            "height": "100%",
            "background": "#f0f0f0",
            "display": "inline-block",
            "verticalAlign": "top"
        }),

        html.Div(
            [
            dcc.Graph(id="fig_energy",config={"displayModeBar": False}, style={"height": "50%", "width": "100%"}),
            dcc.Graph(id="fig_co2",config={"displayModeBar": False}, style={"height": "50%", "width": "100%"})],style={
                "width": "35%",
                "height": "100%",
                "background": "#ffeeba",
                "display": "inline-block",
                "verticalAlign": "top",
                "textAlign": "center",
                "fontSize": "20px"
            } )
    ], style={
        "height": "65vh", 
        "width": "100%",
        "display": "block",
        "background":"grey"
    }),




#     butttom figure--------------------------------------------------------------------
     html.Div([
        # 
        html.Div(dcc.Graph(id="bar3", style={
            "height": "100%",     
            "width": "100%",      
            "padding": "0",       
            "margin": "0"        
        },config={"displayModeBar": False}),style={
        "width": "65%","height": "100%","background": "#d4edda","display": "inline-block","verticalAlign": "top","textAlign": "center","padding": "0","margin": "0","overflow": "hidden"}
        
        ),


        html.Div([
        dcc.Graph(id="figure4", style={"height": "100%", "width": "100%"}, config={"displayModeBar": False})
    ],
          style={
        "width": "35%",
        "height": "100%",
        "background": "#e9ecef", 
        "display": "inline-block",
        "verticalAlign": "top",
        "textAlign": "center",
        "padding": "0px"
         })
    ], style={
        "height": "35vh",  
        "width": "100%",
        "display": "block"
    })]  , style={
    "height": "100vh",  
    "width": "100vw",
    "margin": "0",
    "overflow": "hidden"
})


common_font = common_font = dict(
    family="Arial, sans-serif",   
    color="#1f3b64",              
    size=11                      
)
@app.callback(
    Output("fig_energy","figure"),
    Output("fig_co2","figure"),
    Input("map", "clickData")
)
def update_building(clickData):
    import plotly.graph_objects as go
    if not clickData:
        empty = go.Figure()
        empty.update_layout(
        paper_bgcolor="#f5f6fa",  
        plot_bgcolor="#f5f6fa",   
        xaxis=dict(
            title="Year",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",  
            zeroline=False,
            showline=True,
            linecolor="rgba(0,0,0,0.2)",  
            tickfont=dict(color="#555", size=11),
            titlefont=dict(color="#1f3b64", size=12)
        ),
        yaxis=dict(
            title="Value",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False,
            showline=True,
            linecolor="rgba(0,0,0,0.2)",
            tickfont=dict(color="#555", size=11),
            titlefont=dict(color="#1f3b64", size=12)
        ),
        margin=dict(l=40, r=10, t=10, b=30)
    )
        return empty, empty
    
    building = clickData["points"][0]["customdata"][0]
    print("Clicked building:", building)

    subset = df[df["Building"] == building].sort_values("Year")

    fig_energy = go.Figure()
    fig_energy.add_trace(go.Scatter(
        x=subset["Year"],
        y=subset["Electricity"] + subset["Heating"],
        mode="lines+markers",
        line=dict(width=3,color="#1f3b64"),
        marker=dict(size=8, color="#2e8b57"),
        hovertemplate="Year: %{x}<br>Total Energy: %{y:.1f} kWh/m²<extra></extra>"
    ))
    fig_energy.update_layout(
        title=f"Total Energy Consumption — {building}",
        xaxis_title="Year",
        yaxis_title="kWh/m²/yr",
        font=common_font,
        paper_bgcolor="#f5f6fa",  
        plot_bgcolor="white",
        template="plotly_white",
        margin=dict(l=40, r=20, t=40, b=40)
    )

    fig_co2 = go.Figure()
    fig_co2.add_trace(go.Scatter(
        x=subset["Year"],
        y=subset["CO2"],
        mode="lines+markers",
        line=dict(width=3,color="#1f3b64"),
        marker=dict(size=8, color="#6a51a3"),
        hovertemplate="Year: %{x}<br>CO₂ Emission: %{y:.1f} kg/m²<extra></extra>"
    ))
    fig_co2.update_layout(
        title=f"CO₂ Emission — {building}",
        xaxis_title="Year",
        yaxis_title="kg/m²/yr",
        font = common_font,
        paper_bgcolor="#f5f6fa",
        plot_bgcolor="white",
        template="plotly_white",
        margin=dict(l=40, r=20, t=40, b=40)
    )
    return fig_energy, fig_co2
    
@app.callback(
    Output("bar3", "figure"),   
    Input("map", "figure"),
    Input("map", "relayoutData")
)
def update_bar_from_year(fig, relayoutData):
    year = 2022  
    if fig and "layout" in fig and "sliders" in fig["layout"]:
        try:
            idx = fig["layout"]["sliders"][0]["active"]
            year = int(fig["frames"][idx]["name"])
        except Exception:
            pass
    
    if relayoutData:
        if "sliders[0].active" in relayoutData:
            try:
                year = 2022 + relayoutData["sliders[0].active"]
            except Exception:
                pass
        elif "sliders[0].currentvalue" in relayoutData:
            try:
                year = int(relayoutData["sliders[0].currentvalue"]["label"])
            except Exception:
                pass
    
    print("Current Year:", year)

    df_year = df[df["Year"] == year]

    energy_data = pd.DataFrame({
        "Category": ["Electricity", "Heating", "CO₂", "TotalEnergy"],
        "Value": [
            df_year["Electricity"].mean(),
            df_year["Heating"].mean(),
            df_year["CO2"].mean(),
            df_year["TotalEnergy"].mean()
        ]
    })

    fig_bar = px.bar(
        energy_data,
        x="Category",
        y="Value",
        text="Value",
        color_discrete_sequence=["#1f3b64"],  # 与 map 一致的蓝色系
        title=f"Average Energy Consumption ({year})"
    )
    fig_bar.update_traces(texttemplate="%{text:.1f}",textposition="auto")
    fig_bar.update_layout(
        plot_bgcolor="#f5f6fa",
        paper_bgcolor="#f5f6fa",
        font=common_font,
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=40),
    )

    return fig_bar


@app.callback(
    Output("figure4", "figure"),
    Input("map", "clickData")
)
def update_radar_chart(clickData):
    import plotly.graph_objects as go
    if not clickData:
        fig = go.Figure()
        fig.update_layout(
            title="Energy Performance Radar (Select a Building)",
            title_x=0.5,
            paper_bgcolor="rgba(233,236,239,0.6)",
            font=dict(family="Arial", color="#1f3b64", size=13),
            polar=dict(radialaxis=dict(visible=True))
        )
        return fig
    
    building_name = clickData["points"][0]["customdata"][0]
    frame_year = int(clickData["points"][0]["customdata"][1])
    b = df[(df["Building"] == building_name) & (df["Year"] == frame_year)]
    if b.empty:
        return go.Figure()
    b = b.iloc[0]


    categories = ["Electricity", "Heating", "CO₂"]
    values = [float(b["Electricity"]), float(b["Heating"]), float(b["CO2"])]

    typical_total = float(b["Typical"])
    total_actual = sum(values)
    scale = typical_total / total_actual if total_actual != 0 else 1
    standard_values = [v * scale for v in values]

    for arr in (values, standard_values):
        arr.append(arr[0])
    categories += [categories[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        name=f"{building_name} ({frame_year})",
        line_color="#1f3b64",
        fillcolor="rgba(31,59,100,0.3)"
    ))

    fig.add_trace(go.Scatterpolar(
        r=standard_values,
        theta=categories,
        fill="toself",
        name="Industry Standard",
        line_color="#2E8B57",
        fillcolor="rgba(46,139,87,0.25)"
    ))

    fig.update_layout(
        title=f"Energy Performance Radar — {building_name} ({frame_year})",
        title_x=0.5,
         paper_bgcolor="rgba(233,236,239,0.6)",
        font=dict(family="Arial", color="#1f3b64", size=13),
        legend=dict(
            x=0.7, y=1.15,
            bgcolor="rgba(255,255,255,0.6)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
            font=dict(size=11)
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor="lightgray",
                linecolor="rgba(0,0,0,0.3)",
                tickfont=dict(size=12)
            ),
            angularaxis=dict(
                tickfont=dict(size=13, color="#1f3b64")
            )
        ),
        margin=dict(l=30, r=30, t=70, b=30)
    )
   
    return fig



server = app.server
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8000, debug=False)