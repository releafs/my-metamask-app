import requests
import streamlit as st

INFURA_URL = "https://base-mainnet.infura.io/v3/f50128c6008d473fa2890724011b1a94"

# Function to get token balances
def get_token_balance(wallet_address, contract_address, decimals):
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
        response = requests.post(INFURA_URL, json=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        balance = int(response.json()["result"], 16)
        return balance / (10 ** decimals)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching balance: {e}")
        return None

# Streamlit interface
st.title("View Your Tokens")

wallet_address = st.text_input("Enter your wallet address:", "")
if wallet_address:
    st.write(f"Connected Wallet: {wallet_address}")

    tokens = [
        {"name": "USDT", "contract": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "decimals": 6},
        {"name": "DAI", "contract": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "decimals": 18},
    ]

    for token in tokens:
        balance = get_token_balance(wallet_address, token["contract"], token["decimals"])
        if balance is not None:
            st.write(f"{token['name']}: {balance}")
        else:
            st.error(f"Error fetching balance for {token['name']} ({token['contract']})")
