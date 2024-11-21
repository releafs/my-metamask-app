import streamlit as st

# Title of the app
st.title("MetaMask Integration with Streamlit")

# Embed the MetaMask frontend
st.components.v1.html(
    """
    <iframe
        src="public/index.html"
        style="border:none; width:100%; height:300px;"
        scrolling="no"
    ></iframe>
    """,
    height=400,
)
