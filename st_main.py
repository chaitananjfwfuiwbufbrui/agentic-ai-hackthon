import streamlit as st

st.title("hackthon")


picture = st.camera_input("Take a  picture")
if picture :
    st.image(picture)



