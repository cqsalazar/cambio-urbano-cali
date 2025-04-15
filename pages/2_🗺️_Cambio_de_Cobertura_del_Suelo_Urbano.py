import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap
from streamlit_image_comparison import image_comparison

st.set_page_config(page_title='Dashboard', layout='centered', page_icon="🗺️")

st.title('Cambio de cobertura del suelo')

multi = '''Cambio de las coberturas del suelo del Distrito de Santiago de Cali
 en el periodo 2018-2024.  
      :grey[_Las coberturas del suelo se determinaron a partir de imágenes satelitales Sentinel-2, usando  
      herramientas Deep Learning de ArcGIS Pro y un modelo preentrenado de Corine Land Cover_.]
'''
st.markdown(multi)
#st.markdown(")

data_folder = 'data'

if not os.path.exists(data_folder):
    os.mkdir(data_folder)

cob_sentinel2018 = 'Coberturas2018.tif'
cob_sentinel2018 = os.path.join(data_folder, cob_sentinel2018)
cob_sentinel2024 = 'Coberturas2024.tif'
cob_sentinel2024 = os.path.join(data_folder, cob_sentinel2024)

# render image-comparison
image_comparison(
    img1=cob_sentinel2018,
    img2=cob_sentinel2024,
    label1="2018",
    label2="2024",
    width=500,
    starting_position=50,
    show_labels=True,
    make_responsive=True,
    in_memory=True
)

# Chart
difference_table = 'difference_cover_land.xlsx'
difference_table = pd.read_excel(os.path.join(data_folder, difference_table))
df = pd.DataFrame(difference_table)
df = df.sort_values(by='ID')
colores = df['Color'].values.tolist()

fig, ax = plt.subplots(1, 1)
bars = df.plot(y='Dif_Porc', x='Cobertura', kind='bar', ax=ax, color=colores,
                       ylabel='', xlabel='')

# Extra: Add labels on bars
for bar in bars.patches:
    height = bar.get_height()
    if height <= 1:
        ax.annotate(
            f"{height}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, -15),
            fontsize=10,
            color='white',
            textcoords="offset points", ha='center', va='bottom'
        )
    else:
        ax.annotate(
            f"+{height}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 10),
            fontsize=10,
            color='white',
            textcoords="offset points", ha='center', va='bottom'
        )
        
plt.axhline(y=0, color='gray', linestyle='-')

ax.set_title('Cambios en la cobertura terrestre entre 2018 y 2024\n\n', fontsize=12, 
             color='white', fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(labelbottom=True, color='none')
ax.set_yticklabels([])
ax.set_facecolor('none')
ax.legend().remove()
fig.patch.set_facecolor('none')
plt.xticks(rotation=45, color='white')

st.sidebar.pyplot(fig)   