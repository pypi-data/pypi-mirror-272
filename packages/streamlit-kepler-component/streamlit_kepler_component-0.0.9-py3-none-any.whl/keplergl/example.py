import os
import sys

# Add the project root directory to the sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import time
import json
import streamlit as st

from keplergl import keplergl
from sample_small_geojson import sf_zip_geo
from sample_geojson_points import bart_stops_geo
from sample_geojson_config import sampleGeojsonConfig
from sample_hex_id_csv import sampleH3Data, h3MapConfig

st.subheader("Kepler Bidirectional Communication Demo")

if "datasets" not in st.session_state:
    st.session_state.datasets = []

options = {"keepExistingConfig": True}

map_config = keplergl(st.session_state.datasets, options=options, height=400)
time.sleep(1)
session_data_ids = []
if map_config:
    map_config_json = json.loads(map_config)

    # check if any datasets were deleted
    map_data_ids = [layer["config"]["dataId"] for layer in map_config_json["visState"]["layers"]]
    session_data_ids = [dataset['info']['id'] for dataset in st.session_state.datasets]
    indices_to_remove = [i for i, dataset in enumerate(st.session_state.datasets) if
                         not dataset['info']['id'] in map_data_ids]
    for i in reversed(indices_to_remove):
        del st.session_state.datasets[i]

    session_data_ids = [dataset['info']['id'] for dataset in st.session_state.datasets]

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    san_diego_button_clicked = st.button('Add Bart Stops Geo', disabled=("bart-stops-geo" in session_data_ids))
    if san_diego_button_clicked:
        st.session_state.datasets.append({
            "info": {"label": "Bart Stops Geo", "id": "bart-stops-geo", "type": "geojson"},
            "data": bart_stops_geo
        })
        st.rerun()

with col2:
    bart_button_clicked = st.button('Add SF Zip Geo', disabled=("sf-zip-geo" in session_data_ids))
    if bart_button_clicked:
        st.session_state.datasets.append({
            "info": {"label": "SF Zip Geo", "id": "sf-zip-geo"},
            "data": sf_zip_geo
        })
        st.rerun()

with col3:
    h3_button_clicked = st.button('Add H3 Hexagons V2', disabled=("h3-hex-id" in session_data_ids))
    if h3_button_clicked:
        st.session_state.datasets.append({
            "info": {"label": "H3 Hexagons V2", "id": "h3-hex-id"},
            "data": sampleH3Data
        })
        st.rerun()

if map_config:
    st.code(json.dumps(map_config_json, indent=4))