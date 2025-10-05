import streamlit as st
import math
import folium
from streamlit_folium import st_folium

# Page title
st.title("🌍 Asteroid Impact Simulator")

# Inputs
st.sidebar.header("Asteroid Parameters")
diameter = st.sidebar.slider("Diameter (m)", 10, 1000, 140)
velocity = st.sidebar.slider("Velocity (km/s)", 1, 100, 700)
density = st.sidebar.number_input("Density (kg/m³)", value=3000)
theta = st.sidebar.slider("Impact Angle (°)", 0, 90, 90)
lat = st.sidebar.number_input("Latitude", value=51.864)
lon = st.sidebar.number_input("Longitude", value=-2.238)

# Constants
rho_t = 1200
g = 9.81
TNT_1kg_to_energy = 4.184e6     #4.184*10^6 J in 1kg TNT
v_ms = velocity * 1000
v_vertical = v_ms * math.sin(math.radians(theta))
mass = (4/3) * math.pi * (diameter/2)**3 * density
KE = 0.5 * mass * v_ms**2
effective_energy = 0.5 * mass * v_vertical**2
effective_megatons_TNT = (effective_energy / TNT_1kg_to_energy) / 1e9
crater_diameter_m = 1.161 * (density/rho_t)**(1/3) * (diameter**0.78) * (v_ms**0.44) * (g**(-0.22)) * (math.sin(math.radians(theta))**(1/3))
crater_radius_m = crater_diameter_m / 2
fireball_radius = 3500 * (effective_megatons_TNT)**(0.4)  # meters

shockwave_radius = 8000 * (effective_megatons_TNT)**(1/3)


print(f"Impact location: {lat},{lon} °")
print("ASTEROID IMPACT ESTIMATES")
print("--------------------------")
print(f"Asteroid diameter: {diameter} m")
print(f"Density: {density} kg/m^3")
print(f"Velocity: {velocity:.2f} km/s")
print(f"Impact angle: {theta} degrees")

print(f"\nMass: {mass:.2e} kg")
print(f"Impact Energy: {effective_energy:.2e} J")
print(f"≈ {effective_megatons_TNT:.2f} megatons of TNT")

print(f"\nEstimated crater diameter: {crater_diameter_m/1000:.2f} km")
print(f"Estimated shockwave diameter: {shockwave_radius/1000:.2f} km")
print(f"Estimated fireball diameter: {fireball_radius/1000:.2f} km")
print("\n(Note: These are rough estimates, real impacts are more complex!)")

# Show Map
m = folium.Map(location=[lat, lon], zoom_start=12)

popuptext = f"""
<div style="width: 600px;">
    <h3>Impact Information: {lat:2f}°,{lon:2f}°</h3>
    <strong>Meteorite properties</strong><br>
    Diameter: {diameter}m<br>
    Density: {density}kg/m^3<br>
    Mass: {mass:2e}kg<br>
    Velocity: {velocity:.2f}km/s<br>
    Impact angle: {theta} degrees<br>
    <strong>Crater diameter (estimate)</strong><br>
    ~{crater_diameter_m/1000:.2f} km<br>
    <strong> Impact Energy:</strong><br> 
    {effective_energy:.2e} J
    <strong>Equivalence in TNT</strong><br>
    ≈ {effective_megatons_TNT:.2f} megatons of TNT<br>
    <br>
    <strong>Note: These are rough estimates, real impacts are more complex!</strong>
</div>
"""

iframe = folium.IFrame(popuptext, width=500, height=400)
popup = folium.Popup(iframe, max_width=500)

folium.Marker(
    [lat, lon],
    popup=popup,
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(m)
folium.Circle([lat, lon], radius=crater_radius_m, color="brown", fill=True, fill_opacity=0.6).add_to(m)
folium.Circle([lat, lon], radius=shockwave_radius, color="blue", fill=True, fill_opacity=0.3).add_to(m)
folium.Circle([lat, lon], radius=fireball_radius, color="crimson", fill=True, fill_opacity=0.4).add_to(m)

# Display map in app
st_data = st_folium(m, width=700)

