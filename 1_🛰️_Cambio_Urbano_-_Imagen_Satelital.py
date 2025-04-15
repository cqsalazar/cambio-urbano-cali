import os
import xarray as xr
import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_image_comparison import image_comparison

st.set_page_config(page_title='Dashboard', layout='centered', page_icon="🌎")

st.title('Cambio Urbano 2018-2024')

#st.sidebar.title('About')
#st.sidebar.info('Explore the Highway Statistics')

st.markdown(
    """
    Cambio de la cobertura del suelo urbano del Distrito de Santiago de Cali en el periodo
      2018-2024, visto a través de imágenes satelitales Sentinel-2, con una resolución espacial de 10 m.
"""
)

data_folder = 'data'

if not os.path.exists(data_folder):
    os.mkdir(data_folder)
    
sentinel2018 = 'Sentinel_Cloudless2018_Stretch2.tif'
sentinel2018 = os.path.join(data_folder, sentinel2018)
sentinel2024 = 'Sentinel_Cloudless2024_Stretch2.tif'
sentinel2024 = os.path.join(data_folder, sentinel2024)

# render image-comparison
image_comparison(
    img1=sentinel2018,
    img2=sentinel2024,
    label1="2018",
    label2="2024",
    width=500,
    starting_position=50,
    show_labels=True,
    make_responsive=True,
    in_memory=True,
)



# m = leafmap.Map(
#     zoom=20,
#     center=[3.434, -76.517],
#     zoom_control=True,
#     draw_control=False,
#     scale_control=False,
#     layers_control=False,
#     fullscreen_control=False,
#     measure_control=False,
#     toolbar_control=False
# )

#m.add_raster(sentinel2018, band=['red', 'green', 'blue'], layer_name="Sentinel2018")
#m.add_raster(sentinel2024, band=['red', 'green', 'blue'], layer_name="sentinel2024")

# m.split_map(
#     left_layer=sentinel2018,
#     right_layer=sentinel2024,
#     left_label="2018",
#     right_label="2024",
#     label_position="bottom",
#     left_args={"layer_name": "Sentinel 2018"},
#     right_args={"layer_name": "Sentinel 2024"}
# )

#m_streamlit = m.to_streamlit(600,800)