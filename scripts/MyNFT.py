from web3 import Web3
from web3.eth import Contract
from Connection import Connection

class MyNFTWrapper:
    '''
        Create a new MyNFT object instance. Contains all methods of the contract MyNFT.

        Parameters
        ----------
            - pubk (str): Account Public Key
            - pk (str): Account Private Key
            - connection (Connection): Connection instance for web3 and contract
        
        Attributes
        ----------
            - public_key (str): Account Public Key
            - private_key (str): Account Private Key
            - web3 (Web3): Web3 instance
            - contract (Contract): Smart Contract instance
    '''
    public_key : str
    private_key : str
    web3 : Web3
    contract : Contract
    
    def __init__(self, pubk : str, pk : str, connection : Connection):
        self.public_key = pubk
        self.private_key = pk
        self.web3 = connection.getWeb3Connection()
        self.contract = connection.getContractConnection()
    
    def getName(self):
        '''
            Returns the contract name.

            Returns
            -------
                - name (str | None): Contract name or None if occurs an error.
        '''
        try:
            name = self.contract.functions.name().call({'from': self.public_key})
            return str(name)
        except Exception as e:
            print(e)
            return None
    
    def getSymbol(self):
        '''
            Returns the contract symbol.

            Returns
            -------
                - symbol (str | None): Contract symbol or None if occurs an error.
        '''
        try:
            symbol = self.contract.functions.symbol().call({'from': self.public_key})
            return str(symbol)
        except Exception as e:
            print(e)
            return None
    
    def getOwner(self):
        '''
            Returns the contract owner.

            Returns
            -------
                - owner (str | None): Public key of the contract owner or None if occurs an error.
        '''
        try:
            owner = self.contract.functions.owner().call({'from': self.public_key})
            return str(owner)
        except Exception as e:
            print(e)
            return None

    def mintNFT(self, tokenURI : str):
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
            # Getting the nounce of the account 
            nonce = self.web3.eth.get_transaction_count(self.public_key, 'latest')
            # Creating the transaction
            tx = self.contract.functions.mintNFT(self.public_key, tokenURI).buildTransaction({"nonce": nonce, "from": self.public_key})
            # Signing the transaction with account private key
            signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
            # Retrieving the transaction hash
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            # Getting the transaction data
            transaction = self.web3.eth.get_transaction(tx_hash)
            data = dict(self.contract.decode_function_input(transaction.input)[1])
            return (tx_hash.hex(), data)
        except Exception as e:
            print(e)
            return None
