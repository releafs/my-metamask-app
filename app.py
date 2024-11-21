import streamlit as st
import requests
import time

# Constants
INFURA_URL = "https://base-mainnet.infura.io/v3/f50128c6008d473fa2890724011b1a94"

# Debugging log container
st.title("MetaMask Integration with Token Balances")
debug_logs = st.empty()

def log_debug(message):
    """Logs debug messages to the Streamlit app."""
    if "debug_logs" not in st.session_state:
        st.session_state["debug_logs"] = []
    st.session_state["debug_logs"].append(f"[{time.strftime('%H:%M:%S')}] {message}")
    with debug_logs.container():
        st.markdown("### Debug Logs")
        for log in st.session_state["debug_logs"]:
            st.code(log)

log_debug("App started.")

# Function to fetch token balances
def get_token_balance(wallet_address, contract_address, decimals):
    """
    Fetches the balance of a specific ERC-20 token for a wallet address.
    """
    data = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": f"0x70a08231000000000000000000000000{wallet_address[2:]}"
            },
            "latest"
        ],
        "id": 1
    }

    try:
        log_debug(f"Requesting balance for wallet {wallet_address} at contract {contract_address}")
        response = requests.post(INFURA_URL, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses
        result = response.json().get("result", "0x")

        if result == "0x":
            log_debug(f"No balance found for contract {contract_address}")
            return 0
        balance = int(result, 16)
        log_debug(f"Balance fetched successfully: {balance}")
        return balance / (10 ** decimals)
    except ValueError as e:
        log_debug(f"Error parsing balance: {e}")
        st.error(f"Error parsing balance: {e}")
    except requests.exceptions.RequestException as e:
        log_debug(f"Request error: {e}")
        st.error(f"Request error: {e}")
    return None

# App UI
st.markdown("## View Your Tokens")
st.markdown("Connect your wallet and view your ERC-20 token balances.")

wallet_address = st.text_input("Enter your wallet address:")
if wallet_address:
    st.success(f"Connected Wallet: {wallet_address}")

    # ERC-20 Tokens to check
    tokens = [
        {"name": "USDT (Tether)", "contract": "0xdac17f958d2ee523a2206206994597c13d831ec7", "decimals": 6},
        {"name": "DAI (Dai Stablecoin)", "contract": "0x6b175474e89094c44da98b954eedeac495271d0f", "decimals": 18},
    ]

    # Display token balances
    st.markdown("### Token Balances")
    for token in tokens:
        balance = get_token_balance(wallet_address, token["contract"], token["decimals"])
        if balance is not None:
            st.write(f"{token['name']}: {balance}")
        else:
            st.write(f"Error fetching balance for {token['name']}.")

# Add a footer for information
st.markdown(
    """
    ---
    **Disclaimer**: This app uses the Ethereum mainnet via Infura. Ensure you have an active internet connection.
    """
)

log_debug("App finished rendering.")
