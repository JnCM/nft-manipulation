import os, json
from environs import Env
from MyNFT import MyNFTWrapper
from Connection import Connection

# Getting environment variables
env = Env()
path_to_env = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\.env"
env.read_env(path_to_env)

# Initializing the constants
PUBLIC_KEY = env.str("PUBLIC_KEY")
PRIVATE_KEY = env.str("PRIVATE_KEY")
CHAIN_URL = env.str("CHAIN_URL")
CONTRACT_ADDRESS = env.str("CONTRACT_ADDRESS")
CONTRACT_ABI = json.loads(env.str("CONTRACT_ABI"))


def menu():
    print("\n========= NFT Usage Example =========")
    print("| 1 - Mint a NFT;                   |")
    print("| 2 - View the contract owner;      |")
    print("| 3 - View the contract name;       |")
    print("| 4 - View the contract symbol;     |")
    print("| 0 - Exit.                         |")
    print("=====================================\n")


def init():
    conn = Connection(CHAIN_URL, CONTRACT_ADDRESS, CONTRACT_ABI)
    status_provider = conn.connectNetwork()
    status_contract = conn.connectContract()
    if status_provider and status_contract:
        nft_instance = MyNFTWrapper(PUBLIC_KEY, PRIVATE_KEY, conn)
        return nft_instance
    elif not status_provider:
        print("An error occurred! Check the connection with provider.")
    else:
        print("An error occurred! Check the connection with smart contract.")
    return None


def main():
    nft_instance = init()
    
    while True:
        menu()
        
        try:
            choice = int(input("Enter your choice: "))
        except:
            choice = -1
        print("=====================================")
        
        if choice == 0:
            break
        elif choice == 1:
            token_URI = input("Paste here your Non-Fungible Token URL: ")
            print("=====================================")
            data = nft_instance.mintNFT(token_URI)
            if data == None:
                print("An error occurred! Check the error description.")
            else:
                print("Transaction Hash: {}".format(data[0]))
                print("Owner: {}".format(data[1]["recipient"]))
                print("Token URI: {}".format(data[1]["tokenURI"]))
        elif choice == 2:
            owner = nft_instance.getOwner()
            print("Contract Owner: {}".format(owner if owner is not None else "-"))
        elif choice == 3:
            name = nft_instance.getName()
            print("Contract Name: {}".format(name if name is not None else "-"))
        elif choice == 4:
            symbol = nft_instance.getSymbol()
            print("Contract Symbol: {}".format(symbol if symbol is not None else "-"))
        else:
            print("Just enter valid choices!")


if __name__ == "__main__":
    main()