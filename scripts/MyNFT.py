from web3 import Web3

class MyNFTWrapper:
    '''
        Create a new MyNFT object instance. Contains all methods of the contract MyNFT,
        as well as the methods to connect with the network and with the contract.

        Parameters
        ----------
            - pubk (str): Account Public Key
            - pk (str): Account Private Key
            - provider (str): Network Provider URL (e.g. Ganache)
            - address (str): Contract address
            - abi (dict): Contract ABI
        
        Attributes
        ----------
            - token_URI (str): Non-Fungible Token URL
            - public_key (str): Account Public Key
            - private_key (str): Account Private Key
            - provider (str): Network Provider URL (e.g. Ganache)
            - contract_address (str): Contract address
            - contract_abi (dict): Contract ABI
            - web3 (Web3): Web3 instance
            - contract (Contract): Smart Contract instance
    '''
    token_URI : str
    public_key : str
    private_key : str
    provider : str
    contract_address : str
    contract_abi : dict
    web3 : None
    contract : None
    
    def __init__(self, pubk : str, pk : str, provider : str, address : str, abi : dict):
        self.token_URI = ""
        self.public_key = pubk
        self.private_key = pk
        self.provider = provider
        self.contract_address = address
        self.contract_abi = abi
    
    def getTokenURI(self):
        '''
            Returns the Non-Fungible Token URL.

            Returns
            -------
                - tokenURI (str): Non-Fungible Token URL
        '''
        return self.token_URI
    
    def setTokenURI(self, newTokenURI : str):
        '''
            Set a new Non-Fungible Token URL.

            Parameters
            ----------
                - newTokenURI (str): The new Non-Fungible Token URL
        '''
        self.token_URI = newTokenURI
    
    def connectNetwork(self):
        '''
            Connects the provider and returns the status of the connection.

            Returns
            -------
                - status (bool): True if the connection was well-success or False is not.
        '''
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.provider))
            return self.web3.isConnected()
        except Exception as e:
            print(e)
            return False
    
    def connectContract(self):
        '''
            Connects the contract through of your address and your ABI.

            Returns
            -------
                - status (bool): True if the connection was well-success or False is not.
        '''
        try:
            self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
            return True
        except Exception as e:
            print(e)
            return False
    
    def mintNFT(self, tokenURI=""):
        '''
            Saves the Non-Fungible Token URL in the Blockchain.

            Parameters
            ----------
                - tokenURI (str): The Non-Fungible Token URL, if the URL is not set yet

            Returns
            -------
                - data (None | tuple): None if occurs an error, or a tuple containing the transaction hash
                and a dictionary with the recipient and URL of the NFT.
        '''
        try:
            if self.token_URI == "" and tokenURI == "":
                print("Set a Token URI first!")
            elif self.token_URI == "" and tokenURI != "":
                self.setTokenURI(tokenURI)
            else:
                # Getting the nounce of the account 
                nonce = self.web3.eth.get_transaction_count(self.public_key, 'latest')
                # Creating the transaction
                tx = self.contract.functions.mintNFT(self.public_key, self.token_URI).buildTransaction({"nonce": nonce, "from": self.public_key})
                # Signing the transaction with account private key
                signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
                # Retrieving the transaction hash
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                # Getting the transaction data
                transaction = self.web3.eth.get_transaction(tx_hash)
                data = dict(self.contract.decode_function_input(transaction.input)[1])
                return (tx_hash.hex(), data)
            return None
        except Exception as e:
            print(e)
            return None
