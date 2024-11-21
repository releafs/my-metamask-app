import streamlit as st
from web3 import Web3

# Connect to the Ethereum mainnet via Infura or another provider
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Function to fetch token balances
def fetch_token_balance(wallet_address, token_address):
    # ERC-20 token ABI for 'balanceOf'
    token_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        }
    ]
    token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=token_abi)
    balance = token_contract.functions.balanceOf(Web3.to_checksum_address(wallet_address)).call()
    return balance

# Streamlit app UI
st.title("View Your Tokens")
st.markdown("Connect your wallet and view your ERC-20 token balances.")

# Wallet connection
wallet_address = st.text_input("Enter your wallet address:")
if wallet_address:
    if web3.is_address(wallet_address):
        st.success(f"Connected Wallet: {wallet_address}")

        # Add token contracts you want to fetch
        tokens = {
            "USDT (Tether)": "0xdac17f958d2ee523a2206206994597c13d831ec7",  # Example: Tether (USDT) contract
            "DAI (Dai Stablecoin)": "0x6b175474e89094c44da98b954eedeac495271d0f",  # Example: DAI contract
        }

        # Display token balances
        st.markdown("### Token Balances")
        for token_name, token_address in tokens.items():
            try:
                balance = fetch_token_balance(wallet_address, token_address)
                st.write(f"{token_name}: {balance / (10 ** 18):,.4f}")
            except Exception as e:
                st.error(f"Error fetching balance for {token_name}: {e}")
    else:
        st.error("Invalid wallet address. Please enter a valid Ethereum address.")

# Footer
st.markdown(
    """
    ---
    **Disclaimer:** This app uses the Ethereum mainnet via Infura. Ensure you have an active internet connection.
    """
)
