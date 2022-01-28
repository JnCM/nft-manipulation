import json
from environs import Env
from MyNFT import MyNFTWrapper

# Getting environment variables
env = Env()
path_to_env = '.env'
env.read_env(path_to_env)

# Initializing the constants
PUBLIC_KEY = env.str("PUBLIC_KEY")
PRIVATE_KEY = env.str("PRIVATE_KEY")
CHAIN_URL = env.str("CHAIN_URL")
CONTRACT_ADDRESS = env.str("CONTRACT_ADDRESS")
CONTRACT_ABI = json.loads(env.str("CONTRACT_ABI"))

def main():
    print("-----------------")
    token_URI = input("Paste here your Non-Fungible Token URL: ")
    print("-----------------")
    nft_instance = MyNFTWrapper(PUBLIC_KEY, PRIVATE_KEY, CHAIN_URL, CONTRACT_ADDRESS, CONTRACT_ABI)
    if nft_instance.connectNetwork():
        print("Provider connected successfully!")
        print("-----------------")
        if nft_instance.connectContract():
            print("Contract connected successfully")
            print("-----------------")
            nft_instance.setTokenURI(token_URI)
            data = nft_instance.mintNFT()
            if data == None:
                print("An error occurred! Check the error description.")
            else:
                print("----- Transaction Hash -----")
                print(data[0])
                print("----- NFT Data -----")
                print("Recebedor: {}".format(data[1]["recipient"]))
                print("Token URI: {}".format(data[1]["tokenURI"]))
        else:
            print("An error occurred! Check the connection with smart contract.")
    else:
        print("An error occurred! Check the connection with provider.")


if __name__ == "__main__":
    main()
