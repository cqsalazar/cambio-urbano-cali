import os
import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap

st.title('Crecimiento Urbano 2018-2024')

multi = '''Entre **2018** y **2024**, la huella urbana de la ciudad se expandió
aproximadamente un 6%.
'''
st.markdown(multi)

data_folder = 'data'

if not os.path.exists(data_folder):
    os.mkdir(data_folder)

m = leafmap.Map(
    add_google_map=False,
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

urbano2018 = 'Urbano2018.tif'
urbano2018 = os.path.join(data_folder, urbano2018)
urbano2024 = 'Urbano2024.tif'
urbano2024 = os.path.join(data_folder, urbano2024)

m.add_raster(urbano2024, colormap=["blue", "red"], layer_name="Urbano 2024", nodata=0)
m.add_raster(urbano2018, colormap=["blue", "darkred"], layer_name="Urbano 2018", nodata=0)

gpkg_file = 'cali.gpkg'
gpkg_filepath = os.path.join(data_folder, gpkg_file)


perim_mun = gpd.read_file(gpkg_filepath, layer='Perimetro_Municipal')
comunas = gpd.read_file(gpkg_filepath, layer='Comunas')
cen_pob = gpd.read_file(gpkg_filepath, layer='bcs_centros_poblados')
area_exp = gpd.read_file(gpkg_filepath, layer='area_expansion')

m.add_gdf(comunas, layer_name='Comunas', style={'color':'gray', 'fill':'white', 'weight':1})
m.add_gdf(cen_pob, layer_name='Centros Poblados', style={'color':'white', 'fill':None, 'weight':1})
m.add_gdf(area_exp, layer_name='Área de Expansión', style={'color':'olive', 'fill':None, 'weight':1})
m.add_gdf(perim_mun, layer_name='Perímetro Municipal', style={'color':'silver', 'fill': None, 'weight':2})

m.add_labels(
    comunas,
    "COMUNA",
    font_size="12pt",
    font_color="blue",
    font_family="arial",
    font_weight="bold"
)

# Define the legend
legend_dict = {
    'Urbano 2018': 'darkred',
    'Urbano 2024': 'red'
}

# Add the legend to the map
m.add_legend(title='', legend_dict=legend_dict)

bounds = [-76.552734, 3.480119, -76.480231, 3.330466]
m.zoom_to_bounds(bounds)

m_streamlit = m.to_streamlit(600, 800)
