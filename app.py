import streamlit as st
import time

# Debugging log container
st.title("MetaMask Integration Debugging")
debug_logs = st.empty()

def log_debug(message):
    if "debug_logs" not in st.session_state:
        st.session_state["debug_logs"] = []
    st.session_state["debug_logs"].append(f"[{time.strftime('%H:%M:%S')}] {message}")
    with debug_logs.container():
        st.markdown("### Debug Logs")
        for log in st.session_state["debug_logs"]:
            st.code(log)

log_debug("App started.")

try:
    st.markdown("## Connecting to MetaMask")
    log_debug("Rendering MetaMask connection iframe...")
    st.components.v1.html(
        """
        <iframe
            src="frontend/public/index.html"
            style="border:none; width:100%; height:400px;"
            scrolling="no"
        ></iframe>
        """,
        height=400,
    )
    log_debug("Iframe rendered successfully.")
except Exception as e:
    log_debug(f"Error rendering iframe: {e}")
    st.error(f"Error: {e}")

log_debug("App finished rendering.")
