import openmc
import streamlit as st
from openmc_cylindrical_mesh_plotter import main
from utils import save_uploadedfile

st.write(
    """
        This tab makes use of the 🐍 Python package [openmc_cylindrical_mesh_plotter](https://github.com/fusion-energy/openmc_cylindrical_mesh_plotter) which is available on GitHub.
    """
)
main()
