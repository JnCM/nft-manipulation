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
    print("| 5 - Search a NFT by ID;           |")
    print("| 6 - View NFT owner by Token ID;   |")
    print("| 7 - Amount of NFTs of an account; |")
    print("| 8 - Transfer a NFT;               |")
    print("| 9 - Pay a NFT;                    |")
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
                print("Token ID: {}".format(data[0]))
                print("Transaction Hash: {}".format(data[1]))
                print("Owner: {}".format(data[2]["recipient"]))
                print("Token URI: {}".format(data[2]["tokenURI"]))
        elif choice == 2:
            owner = nft_instance.getOwner()
            print("Contract Owner: {}".format(owner if owner is not None else "-"))
        elif choice == 3:
            name = nft_instance.getName()
            print("Contract Name: {}".format(name if name is not None else "-"))
        elif choice == 4:
            symbol = nft_instance.getSymbol()
            print("Contract Symbol: {}".format(symbol if symbol is not None else "-"))
        elif choice == 5:
            try:
                token_id = int(input("Type here your Non-Fungible Token ID: "))
            except:
                token_id = -1
            print("=====================================")
            if token_id > 0:
                tokenURI = nft_instance.getTokenURIById(token_id)
                print("Token URI: {}".format(tokenURI if tokenURI is not None else "-"))
            else:
                print("Just enter valid IDs!")
        elif choice == 6:
            try:
                token_id = int(input("Type here your Non-Fungible Token ID: "))
            except:
                token_id = -1
            print("=====================================")
            if token_id > 0:
                owner = nft_instance.getOwnerOfByTokenId(token_id)
                print("NFT Owner: {}".format(owner if owner is not None else "-"))
            else:
                print("Just enter valid IDs!")   
        elif choice == 7:
            address = input("Paste here your account address: ")
            print("=====================================")
            balance = nft_instance.getBalanceOfAOwner(address)
            print("Amount of tokens: {}".format(balance if balance is not None else "-"))
        elif choice == 8:
            address = input("Paste here the receiver account address: ")
            try:
                token_id = int(input("Type here your Non-Fungible Token ID: "))
            except:
                token_id = -1
            print("=====================================")
            if token_id > 0:
                result = nft_instance.transferFrom(address, token_id)
                print("Transfer result: {}".format(result if result is not None else "An error occurred."))
            else:
                print("Just enter valid IDs!")
        elif choice == 9:
            address = input("Paste here the receiver account address: ")
            print("=====================================")
            result = nft_instance.payNft(address, 0.02)
            print("Transfer result: {}".format(result if result is not None else "An error occurred."))
        else:
            print("Just enter valid choices!")


if __name__ == "__main__":
    main()