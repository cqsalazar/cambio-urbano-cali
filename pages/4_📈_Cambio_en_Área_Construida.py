import os
import folium
import rasterio
import numpy as np
import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static

st.title('Cambio en Área Construida')

data_folder = 'data'

if not os.path.exists(data_folder):
    os.mkdir(data_folder)

m = leafmap.Map(
    center=[3.409, -76.526],
    zoom=14,
    zoom_control=True,
    draw_control=False,
    scale_control=False,
    layers_control=True,
    fullscreen_control=False,
    measure_control=False,
    toolbar_control=False
)

m.add_basemap("CartoDB.DarkMatter")

gpkg_file = 'cali.gpkg'
gpkg_filepath = os.path.join(data_folder, gpkg_file)

perim_mun = gpd.read_file(gpkg_filepath, layer='Perimetro_Municipal')
comunas = gpd.read_file(gpkg_filepath, layer='Comunas')
cen_pob = gpd.read_file(gpkg_filepath, layer='bcs_centros_poblados')
area_exp = gpd.read_file(gpkg_filepath, layer='area_expansion')
dif_a_cons = gpd.read_file(gpkg_filepath, layer='AreaConstruida_Barrios')

callback = lambda feat: {"color": feat["properties"]["SIMBOLOGY"], "fillOpacity": 1, 'weight':2}
m.add_gdf(dif_a_cons, layer_name='Cambio en Área Construida', style_callback=callback, visible=False)

m.add_gdf(comunas, layer_name='Comunas', style={'color':'gray', 'fill':None, 'weight':1})
m.add_gdf(cen_pob, layer_name='Centros Poblados', style={'color':'white', 'fill':None, 'weight':1})
m.add_gdf(area_exp, layer_name='Área de Expansión', style={'color':'olive', 'fill':None, 'weight':1})
m.add_gdf(perim_mun, layer_name='Perímetro Municipal', style={'color':'silver', 'fill': None, 'weight':2})

legend_dict = {
    "Sin cambio": "#FFFFE5",
    "0 - 10 ha": "#FEE391",
    "10 - 20 ha": "dec5c5",
    "20 - 30 ha": "d99282",
    "30 - 40 ha": "eb0000"
}

# Add the legend to the map
m.add_legend(title='Cambio en Área Construida', legend_dict=legend_dict)

bounds = [-76.552734, 3.480119, -76.480231, 3.330466]
m.zoom_to_bounds(bounds)

m_streamlit = m.to_streamlit(600, 800)
