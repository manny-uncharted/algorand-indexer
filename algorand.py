import json
import requests
import time
import algosdk
from tinyman.v1.pools import Pool
from tinyman.v1.client import TinymanTestnetClient,TinymanMainnetClient
from algosdk.v2client import indexer



# The algorand explorer indexer address and the api key
algod_address = "https://mainnet-algorand.api.purestake.io/idx2"
headers = {
"X-API-Key": "AH6Q1FUOUq7evV549HE6aZSQkdBHH7d7w2UVqqia",
}



# The address for account and private key
account_private_key = algosdk.mnemonic.to_private_key('away remove own amateur monster nuclear favorite reason again aerobic neck easily key actor crack daughter come ancient edit flight hospital fence ball above vivid')
account = {
    'address': 'W46VNFA7YUFU7DEUXNWKPCCGGO3FERVPFMYVUPZGKBMF7J53HTFAY3TE64',
    'private_key': f'{account_private_key}', # Use algosdk.mnemonic.to_private_key(mnemonic) if necessary
}

#The api_client instantiation
indexer_client = indexer.IndexerClient("", algod_address, headers)

# Tiny man client instantiqation
client = TinymanMainnetClient()

# to fetch all the required assets

ASSET_NAMES = ['AKITA', 'TINYUSDC', 'USDC', 'PLANETS', 'OPUL', 'AWT']
ASSET_ID = [384303832, 312769, 31566704, 27165954, 287867876, 233939122]
#Zipping the assets and asset-id in a dictionary for easy accessing
ASSETS = {key: value for key, value in zip(ASSET_NAMES, ASSET_ID)}

ALGO = client.fetch_asset(0)
#Fetching assets 
ASSETS_FETCH = [] # an empty list to loop through the dictionary and append the assets
for items in list(ASSET_ID):
    ASSETS_FETCH.append(client.fetch_asset(items))


# Looping through all the assets to fetch the asset pool
POOL = [] #List of all the available pools for the assets in ASSETS
for item in ASSETS_FETCH:
    POOL.append(client.fetch_pool(item, ALGO))


address_tracking = [] # String value and hence the address should be within double quote ("")
# fetching Pool address of the tokens to monitor
for pool in POOL:
    address_tracking.append(pool.address)


URL_ASSETS =[] #Empty list to append all the url in the loop for pools to monitor 
for items in address_tracking:
    URL_ASSETS.append(f'https://algoexplorerapi.io/v2/accounts/{items}/transactions/pending')

# Appending the asset_algo quote to a dictonary to make search easier
URL_TRACKING_DICT = {key: value for key, value in zip(ASSET_NAMES, URL_ASSETS)}

#creating a dictionary that zip's assets and their pool address
ASSETS_POOL_ADDRESS = {key: value for key, value in zip(ASSET_NAMES, address_tracking)}
# The ASSET_ADDRESS_POOL dictionary was revert to make it easier to loop through
REVERSED_ASSETS_POOL_ADDRESS = {value : key for (key, value) in ASSETS_POOL_ADDRESS.items()}
reversed_assets_pool_address_key = REVERSED_ASSETS_POOL_ADDRESS.keys()


QUOTE = [] # An empty list to append all the swap quotes
for pool in POOL:
    QUOTE.append(pool.fetch_fixed_output_swap_quote(ALGO(100_000_0)))



response_asset = []

def asset_prices_get():
    response_asset.clear()

    """ 
    Base quote is usdt = QUOTE[1]
    """
    ASSET_ALGO_QUOTE = [] # Empty list to loop through QUOTE and fetch the quote of assets against algo quote price
    for quote in QUOTE:
        ASSET_ALGO_QUOTE.append((1/quote.amount_in.amount)*(QUOTE[1].amount_in.amount/QUOTE[1].amount_out.amount))

    # Appending the asset_algo quote to a dictonary to make search easier
    ASSETS_QUOTE_DICT = {key: value for key, value in zip(ASSET_NAMES, ASSET_ALGO_QUOTE)}

    # Query to fetch changes in price of assets
    for key, value in ASSETS_QUOTE_DICT.items():
        if (value > 0.05) or (value < 0.02):
            value_num = ASSETS_QUOTE_DICT[key]
            message = f"Asset prices : {key} is {str(value_num)} usdt."
            response_asset.append(message) 
    # telegram_send.send(messages=[f"{message}"])





# Function that checks liquidity pool if large assets are removed
response_whale = []
def whale_activities():

    response_whale.clear() # to clear the list after each call

    # fetching the top transactions in the blockchain
    amt = 0
    # while(1):
    for url in URL_ASSETS:
        res = requests.get(url)
        for trans in res.json()['top-transactions']:
            if 'aamt' in trans['txn']:
                print(trans['txn']['aamt'])
                if str(trans['txn']['snd']) in reversed_assets_pool_address_key:
                    if int(trans['txn']['aamt']) > 500000: # I consider any transactions more than 500000 a whale activity. Modify this number as required. 
                        if trans['txn']['arcv'] != amt:
                            amt = trans['txn']['aamt']
                            user_address = str(trans['txn']['arcv'])
                            for key, value in REVERSED_ASSETS_POOL_ADDRESS.items():
                                if (str(trans['txn']['snd']) in key):
                                    token_bought = REVERSED_ASSETS_POOL_ADDRESS[str(trans['txn']['snd'])]
                                    msg_added = f"User Address: \t{user_address}\nAdded: \t{amt} {token_bought} tokens\nLiquidity Added to : {token_bought}/ALGO pool"
                                    # print(msg)
                                    # time(180)
                                    response_whale.append(msg_added)
                                    # telegram_send.send(messages=[msg])
                elif str(trans['txn']['arcv']) in reversed_assets_pool_address_key:
                    if int(trans['txn']['aamt']) > 500000:
                        if trans['txn']['arcv'] != amt:
                            amt = trans['txn']['aamt']
                            user_address = str(trans['txn']['arcv'])
                            for key, value in REVERSED_ASSETS_POOL_ADDRESS.items():
                                if (str(trans['txn']['snd']) in key):
                                    token_bought = REVERSED_ASSETS_POOL_ADDRESS[str(trans['txn']['snd'])]
                                    msg_rem = f"User Address: \t{user_address}\nRemoved: \t{amt} {token_bought} tokens\nLiquidity Removed From : {token_bought}/ALGO pool"
                                    # print(msg)
                                    response_whale.append(msg_rem)
                
                
