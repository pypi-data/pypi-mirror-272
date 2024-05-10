import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import openmc
import openmc_geometry_plot  # adds extra functions to openmc.Geometry
import plotly.graph_objects as go
import streamlit as st
from matplotlib import colors
from pylab import cm, colormaps
from utils import save_uploadedfile


def header():
    st.write(
        f"""This tab makes use of the 🐍 Python package ```openmc_geometry_plot v{openmc_geometry_plot.__version__}``` which is available on [GitHub](https://github.com/fusion-energy/openmc_geometry_plot)."""
    )

header()
openmc_geometry_plot.main()
