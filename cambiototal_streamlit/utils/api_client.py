import requests
import streamlit as st

# --- Constants ---
DOLAR_API_URL = "https://dolarapi.com/v1/dolares"
# The PRD specifies using Dolar Blue
DOLAR_BLUE_NAME = "blue"

# --- API Functions ---

@st.cache_data(ttl=300) # Cache the data for 5 minutes (300 seconds) as per PRD
def get_dolar_rates():
    """
    Fetches real-time dollar exchange rates from DolarAPI.

    Returns:
        A dictionary containing the buy and sell price for Dolar Blue,
        or None if an error occurs.
        e.g., {'buy': 1000.0, 'sell': 1050.0}
    """
    try:
        response = requests.get(DOLAR_API_URL, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()

        # Find the "Dolar Blue" rates in the response array
        for dolar_type in data:
            # The 'casa' key often holds the identifier
            if dolar_type.get('casa') == DOLAR_BLUE_NAME:
                return {
                    "buy": float(dolar_type.get('compra', 0)),
                    "sell": float(dolar_type.get('venta', 0)),
                    "name": dolar_type.get('nombre', 'Unknown')
                }

        # If Dolar Blue is not found
        st.error("Dolar Blue rates not found in the API response.")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from DolarAPI: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# --- Constants for Crypto ---
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

@st.cache_data(ttl=60) # Cache crypto prices for 1 minute
def get_crypto_prices(coin_ids: list[str]):
    """
    Fetches the current price of specified cryptocurrencies in USD.

    Args:
        coin_ids: A list of coin IDs as strings (e.g., ['bitcoin', 'ethereum']).

    Returns:
        A dictionary with coin IDs as keys and their USD price as values,
        or an empty dictionary if an error occurs.
        e.g., {'bitcoin': {'usd': 60000.0}, 'ethereum': {'usd': 3000.0}}
    """
    if not coin_ids:
        return {}

    params = {
        'ids': ",".join(coin_ids),
        'vs_currencies': 'usd'
    }

    try:
        response = requests.get(COINGECKO_API_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from CoinGecko API: {e}")
        return {}
    except Exception as e:
        st.error(f"An unexpected error occurred with CoinGecko API: {e}")
        return {}

if __name__ == "__main__":
    # Test for DolarAPI
    print("--- Testing DolarAPI client ---")
    dolar_rates = get_dolar_rates()
    if dolar_rates:
        print(f"Successfully fetched rates for {dolar_rates['name']}:")
        print(f"  Buy Price: {dolar_rates['buy']}")
        print(f"  Sell Price: {dolar_rates['sell']}")
    else:
        print("Failed to fetch dollar rates.")

    # Test for CoinGecko API
    print("\n--- Testing CoinGecko API client ---")
    crypto_coins = ['bitcoin', 'ethereum', 'tether']
    crypto_prices = get_crypto_prices(crypto_coins)
    if crypto_prices:
        print("Successfully fetched crypto prices:")
        for coin, data in crypto_prices.items():
            print(f"  {coin.capitalize()}: ${data['usd']:.2f}")
    else:
        print("Failed to fetch crypto prices.")
