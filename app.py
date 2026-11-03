
import streamlit as st
import folium
from streamlit_folium import st_folium

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="DHARA | Earth Intelligence",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------
# CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #080D16;
    color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background-color: #101827;
}

h1, h2, h3 {
    color: #FFFFFF;
}

div[data-testid="stMetric"] {
    background-color: #121D2C;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #26354A;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.title("🌍 DHARA")

st.sidebar.caption("Earth Intelligence Platform")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Global Overview",
        "Change Detection",
        "Flood Monitoring",
        "Forest Monitoring",
        "AI Insights",
        "About DHARA"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Powered by NASA-ISRO NISAR")

# ---------------------------------
# GLOBAL OVERVIEW
# ---------------------------------

if page == "Global Overview":

    st.title("DHARA")
    st.caption(
        "Understand the Earth. Discover its Changes."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Satellite Mission", "NISAR")
    col2.metric("Monitoring Scope", "Global")
    col3.metric("Platform Status", "Prototype")

    st.subheader("Explore Our Planet")

    earth_map = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles="CartoDB dark_matter"
    )

    st_folium(
        earth_map,
        width=None,
        height=520
    )

    st.info(
        "Satellite observations and environmental "
        "change analysis will be integrated here."
    )

# ---------------------------------
# CHANGE DETECTION
# ---------------------------------

elif page == "Change Detection":

    st.title("Change Detection")

    st.write(
        "Compare satellite observations "
        "to identify Earth's surface changes."
    )

# ---------------------------------
# FLOOD MONITORING
# ---------------------------------

elif page == "Flood Monitoring":

    st.title("Flood Monitoring")

    st.write(
        "Monitor water-body changes using "
        "radar satellite observations."
    )

# ---------------------------------
# FOREST MONITORING
# ---------------------------------

elif page == "Forest Monitoring":

    st.title("Forest Monitoring")

    st.write(
        "Explore changes in forest and vegetation."
    )

# ---------------------------------
# AI INSIGHTS
# ---------------------------------

elif page == "AI Insights":

    st.title("AI Environmental Insights")

    st.write(
        "Understand environmental changes "
        "through AI-assisted analysis."
    )

# ---------------------------------
# ABOUT
# ---------------------------------

elif page == "About DHARA":

    st.title("About DHARA")

    st.write(
        "DHARA is an Earth observation platform "
        "designed to analyse environmental changes "
        "using NASA-ISRO NISAR satellite data."
    )

    st.caption(
        "NASA Space Apps Challenge 2026"
    )
