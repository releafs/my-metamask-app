import streamlit as st

# Title of the app
st.title("MetaMask Integration with Debugging")

# Debug log container
debug_logs = st.empty()

# Define a container for the wallet connection UI
st.markdown("## Wallet Connection")
st.components.v1.html(
    """
    <iframe
        src="public/index.html"
        style="border:none; width:100%; height:300px;"
        scrolling="no"
    ></iframe>
    <script>
      window.addEventListener('message', (event) => {
        if (event.origin !== window.location.origin) return;

        const message = event.data;

        // Send debug logs back to Streamlit
        fetch('/debug', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(message),
        });
      });
    </script>
    """,
    height=400,
)

# Display incoming debug messages
if "debug_logs" not in st.session_state:
    st.session_state["debug_logs"] = []

# Update debug logs from the incoming messages
if "debug" in st.query_params:
    debug_message = st.query_params["debug"][0]
    st.session_state["debug_logs"].append(debug_message)

# Show debug logs
with debug_logs.container():
    st.markdown("### Debug Logs")
    for log in st.session_state["debug_logs"]:
        st.code(log)
