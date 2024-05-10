"""
Utility module to provide utility classes and functions.

Classes:
    - Tags: Enumeration class to specify request tag.
    - SortType: Enumeration class to specify sort type.
    - Message: Class to specify the message of the status.
    - Status: Class to specify the status of the action.
    - Success: Class to specify the success of the action.
    - BinanceTicker: Class to get the latest price of a symbol.
    - Transaction: Class to represent a transaction.
    - Balance: Class to represent a balance.
    - TokenTransfer: Class to represent a token.
    - Transactions: Class to represent a list of transactions.
    - TokenTransfers: Class to represent a list of token transfers.
    - Balances: Class to represent a list of balances.

Patterns:
    - address_pattern: Pattern to match the address.
    - hash_pattern: Pattern to match the hash.

Type Objects:
    - Type: Type object for the generic types.

Used Modules:
    - enum: Enum module to create enumerations.
    - requests: Requests module to make HTTP requests.
    - user_agent: User agent module to generate user agents.
    - typing: Typing module to provide type hints.
    - re: Regular expression module to match patterns.
    - errors: Errors module to handle exceptions.
    - json: JSON module to parse JSON data.
    - math: Math module to perform mathematical operations.
    - datetime: Datetime module to handle date and time.
"""


import enum, requests, user_agent
from typing import AnyStr, Union, List, Callable, overload, Generic, TypeVar
from re import compile
from datetime import datetime
from .errors import APIError
import json, math

address_pattern = compile(r'^0x[a-fA-F0-9]{40}$')
hash_pattern = compile(r'^0x[a-fA-F0-9]{64}$')

Type = TypeVar('Type')

class Tags(enum.Enum):
    '''
    #### Tags enumeration class to specify request tag.
    ### Enums:
        EARLIEST: Get the earliest balance of the address.
        LATEST: Get the latest balance of the address.
        PENDING: Get the pending balance of the address.
    '''
    EARLIEST = enum.auto()
    LATEST = enum.auto()
    PENDING = enum.auto()

class SortType(enum.Enum):
    '''
    #### SortType enumeration class to specify sort type.
    ### Enums:
        ASC: Sort the balances in ascending order.
        DESC: Sort the balances in descending order.
    '''
    ASC = enum.auto()
    DESC = enum.auto()

class Message:
    '''
    ##### Message class to specify the message of the status.
    ### Args:
        content (str): The message content.
    ### Returns:
        str: The message content.
    '''
    content: str
    def __init__(self, content: str):
        self.content = content
    def __repr__(self):
        return f'Message(content={self.content!r})'
    def __str__(self):
        return self.content

class Status:
    '''
    ##### Status class to specify the status of the action.
    ### Args:
        message (str): The message of the status.
        status (bool): The status of the action.
    ### Returns:
        bool: The status of the action.
    '''
    message: "Message"
    status: "Success"
    def __init__(self, message: "Message", status: "Success"):
        self.message = message
        self.status = status
    def __repr__(self):
        if self.status.status and not self.message.content:
            return f'Status(status={self.status.status!r}, message=\'No description provided.\')'
        return f'Status(status={self.status.status!r}, message={self.message.content!r})'
    def __bool__(self):
        return self.status
    def __invert__(self):
        return self
    def __eq__(self, __value: object) -> bool:
        return bool(self) == bool(__value)
    def __and__(self, msg: Message):
        return Status(
            message=msg,
            status=self.status
        )

class Success(Generic[Type]):
    status: bool = True
    def __repr__(self) -> str:
        return (
            f'Status(message=\'Action completed successfully\')'
            if self.status
            else f'Status(message=\'Action failed\')'
        )

    def __bool__(self):
        return self.status
    def __invert__(self):
        self.status = not self.status
        return self
    def __eq__(self, __value: object) -> bool:
        return bool(self) == bool(__value)
    def __and__(self, msg: Message):
        return Status(
            message=msg,
            status=self
        )



class BinanceTicker(object):
    '''
    ##### Binance Ticker class to get the latest price of a symbol.

    ### Args:
        symbol (str): The symbol of the coin pair.
    
    ### Returns:
        float: The latest price of the symbol.
    '''
    price: float
    symbol: str
    __data__ = None
    def __new__(cls, symbol: str):
        cls.symbol = symbol.upper()
        res = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={cls.symbol}')
        cls.price = float(res.json()['price'])
        cls.__response__ = res.json()
        return super().__new__(cls) 
    def get_raw_data(self):
        return self.__data__

class Transaction:
    blockNumber: int = None
    timeStamp: int = None
    hash: str = None
    nonce: int = None
    blockHash: str = None
    transactionIndex: int = None
    from_: str = None
    to: str = None
    value: int = None
    gas: int = None
    gasPrice: int = None
    isError: int = None
    txreceipt_status: int = None
    input: str = None
    contractAddress: str = None
    cumulativeGasUsed: int = None
    gasUsed: int = None
    confirmations: int = None
    methodId: str = None
    functionName: str = None
    def __init__(self, data: dict):
        self.data = data
        for key, value in data.items():
            setattr(self, key if key != 'from' else 'from_', value)
    def __str__(self):
        bl = Balance(int(self.value), self.from_)
        usdbalance = bl.get_usd_balance()
        txtime = datetime.utcfromtimestamp(float(self.timeStamp)).strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.from_} -> {self.to} : ${usdbalance:.5f} on {txtime}'
    def __repr__(self):
        return f'Transaction({self.data!r})'



class Transactions:
    '''
    ##### Transactions class belongs to the transactions of the addresses.
    ### Args:
        transactions (list[Transactions]): The list of transactions.
    ### Methods:
        first: Get the first transaction of the list.
        last: Get the last transaction of the list.
        filter: Filter the transactions by the address.
    
    ### Returns:
        Balance: The first or last transaction of the list.
        Transactions: The filtered transactions.
    
    ### Raises:
        APIError: If the address is not found in the list.
    '''
    def __init__(self, transactions: list[Transaction]):
        self.transactions = transactions
        self._order = 0
        if not transactions:
            raise Exception('The address is not found in the list.')
    def __iter__(self):
        return iter(self.transactions)
    def __bool__(self):
        return bool(self.transactions)
    def __len__(self):
        return len(self.transactions)
    def __getitem__(self, index: int):
        return self.transactions[index]
    def __repr__(self):
        return f'Transactions(length={len(self.transactions)}, hash={hex(id(self.transactions))})'
    def as_list(self):
        '''
        ##### Get the balances as list.
        ### Returns:
            Transactions: The transactions as list.
        '''
        return self.transactions
    def prev(self):
        '''
        ##### Get the previous transaction of the list.
        ### Returns:
            Transaction: The previous transaction of the list.
        '''
        self._order -= 1
        data = self.transactions[self._order]
        return data
    def has_prev(self):
        '''
        ##### Check if the list has previous transaction.
        ### Returns:
            bool: True if the list has previous transaction, False otherwise.
        '''
        return self._order > 0
    def next(self):
        '''
        ##### Get the next transaction of the list.
        ### Returns:
            Transaction: The next transaction of the list.
        '''
        data = self.transactions[self._order]
        self._order += 1
        return data
    def has_next(self):
        '''
        ##### Check if the list has next transaction.
        ### Returns:
            bool: True if the list has next transaction, False otherwise.
        '''
        return self._order < len(self.transactions)
    def first(self):
        '''
        ##### Get the first transaction of the list.
        ### Returns:
            Transaction: The first transaction of the list.
        '''
        return self.transactions[0]
    def last(self):
        '''
        ##### Get the last transaction of the list.
        ### Returns:
            Transaction: The last transaction of the list.'''
        return self.transactions[-1]
    def filter(self, predicate: Callable[[Transaction], bool]):
        '''
        ##### Filter the transactions by the predicate.
        ### Args:
            predicate (Callable[[Transaction], bool]): The predicate to filter the transactions.
        ### Returns:
            Transactions: The filtered transactions.'''
        return Transactions(list(filter(predicate, self.transactions)))

    def filter_by(self, address: str):
        '''
        ##### Filter the transactions by the address.
        ### Args:
            address (str): The address to filter the transactions.
        ### Returns:
            Transactions: The filtered transactions.
        '''
        return Transactions(list(filter(lambda acc: acc.address.lower() in address.lower(), self.transactions)))


class Creation:
    contractCreator: str = None
    contractAddress: str = None
    txHash: str = None
    def __init__(self, data: dict):
        self.data = data
        for key, value in data.items():
            setattr(self, key if key != 'from' else 'from_', value)
    def __repr__(self):
        return f'Creation(contractCreator={self.contractCreator}, contractAddress={self.contractAddress}, txHash={self.txHash})'
    def __str__(self):
        return f'{self.contractCreator} created {self.contractAddress} with txHash {self.txHash}'

class Creations:
    def __init__(self, creations: list[Creation]):
        self._order = 0
        self.creations = creations
        if not creations:
            raise Exception('No creations found.')
    def __repr__(self) -> str:
        return f'Creations(length={len(self.creations)}, token={self.creations[0].tokenSymbol})'
    def __iter__(self):
        return iter(self.creations)
    def __bool__(self):
        return bool(self.creations)
    def __len__(self):
        return len(self.creations)
    def __getitem__(self, index: int):
        return self.creations[index]
    def as_list(self):
        '''
        ##### Get the balances as list.
        ### Returns:
            Creations: The creations as list.
        '''
        return self.creations
    def prev(self):
        '''
        ##### Get the previous creation of the list.
        ### Returns:
            Creation: The previous creation of the list.
        '''
        self._order -= 1
        data = self.transactions[self._order]
        return data
    def has_prev(self):
        '''
        ##### Check if the list has previous creation.
        ### Returns:
            bool: True if the list has previous creation, False otherwise.
        '''
        return self._order > 0
    def next(self):
        '''
        ##### Get the next creation of the list.
        ### Returns:
            Creation: The next creation of the list.
        '''
        data = self.creations[self._order]
        self._order += 1
        return data
    def has_next(self):
        '''
        ##### Check if the list has next creation.
        ### Returns:
            bool: True if the list has next creation, False otherwise.
        '''
        return self._order < len(self.creations)
    def first(self):
        '''
        ##### Get the first creation of the list.
        ### Returns:
            Creation: The first creation of the list.
        '''
        return self.creations[0]
    def last(self):
        '''
        ##### Get the last creation of the list.
        ### Returns:
            Creation: The last creation of the list.'''
        return self.transactions[-1]
    def filter(self, predicate: Callable[[Creation], bool]):
        '''
        ##### Filter the transactions by the predicate.
        ### Args:
            predicate (Callable[[creation], bool]): The predicate to filter the creations.
        ### Returns:
            Creations: The filtered creations.'''
        return Creations(list(filter(predicate, self.creations)))


class TokenTransfer:
    blockNumber: int = None
    timeStamp: int = None
    hash: str = None
    nonce: int = None
    blockHash: str = None
    from_: str = None
    contractAddress: str = None
    to: str = None
    value: int = None
    tokenName: str = None
    tokenSymbol: str = None
    tokenDecimal: int = None
    transactionIndex: int = None
    gas: int = None
    gasPrice: int = None
    gasUsed: int = None
    cumulativeGasUsed: int = None
    input: str = None
    confirmations: int = None

    def __init__(self, data: dict):
        self.data = data
        for key, value in data.items():
            setattr(self, key if key != 'from' else 'from_', value)
    def __repr__(self):
        return f'TokenTransfer(from={self.from_}, to={self.to}, value={int(self.value) / 10**18}, tokenSymbol={self.tokenSymbol})'
    def __str__(self):
        return f'{self.from_} -> {self.to} ({int(self.value) / 10**18} {self.tokenSymbol})'

class TokenTransfers:
    def __init__(self, transfers: list[TokenTransfer]):
        self._order = 0
        self.transfers = transfers
        if not transfers:
            raise Exception('No transfers found.')
    def __repr__(self) -> str:
        return f'TokenTransfers(length={len(self.transfers)}, token={self.transfers[0].tokenSymbol})'
    def __iter__(self):
        return iter(self.transfers)
    def __bool__(self):
        return bool(self.transfers)
    def __len__(self):
        return len(self.transfers)
    def __getitem__(self, index: int):
        return self.transfers[index]
    def sells(self):
        return TokenTransfers([transfer for transfer in self.transfers if transfer.from_ == '0xaecd446602f33355c0d0358cc1a0d673f6a9ef75'])
    def as_list(self):
        '''
        ##### Get the balances as list.
        ### Returns:
            TokenTransfers: The transfers as list.
        '''
        return self.transfers
    def prev(self):
        '''
        ##### Get the previous transfer of the list.
        ### Returns:
            TokenTransfer: The previous transfer of the list.
        '''
        self._order -= 1
        data = self.transactions[self._order]
        return data
    def has_prev(self):
        '''
        ##### Check if the list has previous transfer.
        ### Returns:
            bool: True if the list has previous transfer, False otherwise.
        '''
        return self._order > 0
    def next(self):
        '''
        ##### Get the next transfer of the list.
        ### Returns:
            Transfer: The next transfer of the list.
        '''
        data = self.transfers[self._order]
        self._order += 1
        return data
    def has_next(self):
        '''
        ##### Check if the list has next transfer.
        ### Returns:
            bool: True if the list has next transfer, False otherwise.
        '''
        return self._order < len(self.transfers)
    def first(self):
        '''
        ##### Get the first transfer of the list.
        ### Returns:
            TokenTransfer: The first transfer of the list.
        '''
        return self.transfers[0]
    def last(self):
        '''
        ##### Get the last transfer of the list.
        ### Returns:
            TokenTransfer: The last transfer of the list.'''
        return self.transactions[-1]
    def filter(self, predicate: Callable[[TokenTransfer], bool]):
        '''
        ##### Filter the transactions by the predicate.
        ### Args:
            predicate (Callable[[TokenTransfer], bool]): The predicate to filter the transfers.
        ### Returns:
            TokenTransfers: The filtered transfers.'''
        return TokenTransfers(list(filter(predicate, self.transfers)))


class Balance:
    '''
    ##### Balance class to get the balance of an address.
    ### Args:
        value (int | float): The balance of the address.
    ### Represents:
        str: The balance of the address in ETH, USD and TRY.
    ### Methods:
        get_usd_balance: Get the balance of the address in USD.
        get_eth_balance: Get the balance of the address in ETH.
        get_try_balance: Get the balance of the address in TRY.
    ### Converts:
        int: The balance of the address as raw integer value.
        float: The balance of the address as raw float value.
    '''
    def __init__(self, value: int | float, address: str, token_balance: bool = False):
        self.value = value / (10**18 if token_balance else 1)
        self.address = address
        self.token_balance = token_balance
        if token_balance:
            self.value = math.floor(self.value)
            self.get_usd_balance = None
            self.get_eth_balance = None
            self.get_try_balance = None
            
    def __str__(self):
        if not self.token_balance:
            return f'{self.get_eth_balance():.11f} ETH ~~ {self.get_usd_balance():.2f} USD ~~ {self.get_try_balance():.2f} TRY'
        return f'{self.value} {self.address}'
    def __repr__(self):
        if not self.token_balance:
            return f'Balance(address={self.address}, usd={self.get_usd_balance():.2f}, eth={self.get_eth_balance():.11f}, try={self.get_try_balance():.2f})'
        return f'Balance(address={self.address}, value={self.value})'
    def __int__(self):
        return self.value
    def __float__(self):
        return self.value.__float__()
    def get_usd_balance(self):
        ticker = BinanceTicker('ethusdt')
        return float(ticker.price * (self.value / 10**18))
    def get_eth_balance(self):
        return self.value / 10**18
    def get_try_balance(self):
        ticker = BinanceTicker('usdttry')
        return float(ticker.price * self.get_usd_balance())
    
class Balances:
    '''
    ##### Balances class belongs to the balances of the addresses.
    ### Args:
        balances (list[Balance]): The list of balances.
    ### Methods:
        first: Get the first balance of the list.
        last: Get the last balance of the list.
        filter: Filter the balances by the address.
        filter_by_usd: Filter the balances by the USD balance.
        filter_by_eth: Filter the balances by the ETH balance.
    
    ### Returns:
        Balance: The first or last balance of the list.
        Balances: The filtered balances.
    
    ### Raises:
        APIError: If the address is not found in the list.
    '''
    def __init__(self, balances: List[Balance]):
        self.balances = balances
        self._order = 0
        if not balances:
            raise Exception('The address is not found in the list.')
    def __iter__(self):
        return iter(self.balances)
    def __bool__(self):
        return bool(self.balances)
    def __len__(self):
        return len(self.balances)
    def __getitem__(self, index: int):
        return self.balances[index]
    def __repr__(self):
        return f'Balances(data={self.balances})'
    def as_list(self):
        '''
        ##### Get the balances as list.
        ### Returns:
            Balances: The balances as list.
        '''
        return self.balances
    def prev(self):
        '''
        ##### Get the previous transaction of the list.
        ### Returns:
            Transaction: The previous transaction of the list.
        '''
        self._order -= 1
        data = self.balances[self._order]
        return data
    def has_prev(self):
        '''
        ##### Check if the list has previous transaction.
        ### Returns:
            bool: True if the list has previous transaction, False otherwise.
        '''
        return self._order > 0
    def next(self):
        '''
        ##### Get the next transaction of the list.
        ### Returns:
            Transaction: The next transaction of the list.
        '''
        data = self.balances[self._order]
        self._order += 1
        return data
    def has_next(self):
        '''
        ##### Check if the list has next transaction.
        ### Returns:
            bool: True if the list has next transaction, False otherwise.
        '''
        return self._order < len(self.balances)
    def first(self):
        '''
        ##### Get the first balance of the list.
        ### Returns:
            Balance: The first balance of the list.
        '''
        return self.balances[0]
    def last(self):
        '''
        ##### Get the last balance of the list.
        ### Returns:
            Balance: The last balance of the list.'''
        return self.balances[-1]
    def filter(self, predicate: Callable[[Balance], bool]):
        '''
        ##### Filter the balances by the predicate.
        ### Args:
            predicate (Callable[[Balance], bool]): The predicate to filter the balances.
        ### Returns:
            Balances: The filtered balances.'''
        return Balances(list(filter(predicate, self.balances)))

    def filter_by(self, address: str):
        '''
        ##### Filter the balances by the address.
        ### Args:
            address (str): The address to filter the balances.
        ### Returns:
            Balances: The filtered balances.
        '''
        return Balances(list(filter(lambda acc: acc.address.lower() in address.lower(), self.balances)))



class BaseScan:
    '''
    ##### BaseScan class to get the balance of an address.
    
    ### Args:
        apikey (str): The API key of the BaseScan API.
    
    ### Mehtods:
        request: Send a request to the BaseScan API.
        get_account_balance: Get the balance of the address.
    '''
    def __init__(self, apikey: str):
        self.apikey = apikey
        self.url = 'https://api.basescan.org/api'
        self.headers = {'Content-Type': 'application/json'}
        self.params = {'apikey': self.apikey}
    def request(self, params: dict, headers: dict, data=None):
        self.params.update(params)
        self.headers.update(headers)
        response = requests.get(self.url, data=data, params=self.params, headers=self.headers)
        # print(response.url, response.text)
        return response.json()

    def _internal_transactions_by_tx(self, txhash: str):
        '''
        ##### Get the transactions of the account by the transaction hash.
        
        ### Args:
            txhash (str): The transaction hash.
        
        ### Returns:
            Transactions: The transactions of the account.
        
        ### Raises:
            ValueError: If the transaction hash is not in valid format.
            APIError: If the API returns an error.
        '''
        if not hash_pattern.match(txhash):
            raise ValueError('The transaction hash has to match with valid transaction hash format.')
        res = self.request({
            'module': 'account',
            'action': 'txlistinternal',
            'txhash': txhash
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })
        if res['status'] == '0':
            raise APIError(res['message'])
        return Transactions(list(map(Transaction, res['result'])))

    def _internal_transactions(self, address: str, start_block: int, end_block: int, sort_type: SortType | str, page: int, offset: int, tag: str):
        '''
        ##### Get the transactions of the account.
        ### Args:
            address (str): The address of the account.
            tag (str | Tags): The tag of the process. Use Tags enum to see earliest, latest and pending transactions.
        
        ### Returns:
            Transactions: The transactions of the account.
        
        ### Raises:
            ValueError: If the address is not in valid format.
            APIError: If the API returns an error.
        '''
        if not address_pattern.match(address):
            raise ValueError('The address has to match with valid wallet address format.')
        res = self.request({
            'module': 'account',
            'action': 'txlistinternal',
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'offset': offset,
            'sort': sort_type.name.lower() if isinstance(sort_type, SortType) else sort_type.lower(),
            'page': page,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        }, {})

        if res['status'] == '0':
            raise APIError(res['result'])
        
        return Transactions(list(map(Transaction, res['result'])))
    
    @overload
    def get_internal_transactions(self, address: str, start_block: int, end_block: int, sort_type: SortType | str, page: int, offset: int, tag: str) -> Transactions:
        '''
        ##### Get the transactions of the account.
        ### Args:
            address (str): The address of the account.
            tag (str | Tags): The tag of the process. Use Tags enum to see earliest, latest and pending transactions.
        
        ### Returns:
            Transactions: The transactions of the account.
        
        ### Raises:
            ValueError: If the address is not in valid format.
            APIError: If the API returns an error.
        '''
        pass
    @overload
    def get_internal_transactions(self, txhash: str) -> Transactions:
        '''
        ##### Get the transactions of the account by the transaction hash.
        
        ### Args:
            txhash (str): The transaction hash.
        
        ### Returns:
            Transactions: The transactions of the account.
        
        ### Raises:
            ValueError: If the transaction hash is not in valid format.
            APIError: If the API returns an error.
        '''
        pass
    def get_internal_transactions(self, *args, **kwargs):
        argcount = len(args) + len(kwargs)
        txhash = (args[0] if args else kwargs.get('txhash', ''))
        if argcount == 1 and hash_pattern.match(txhash):
            return self._internal_transactions_by_tx(*args, **kwargs)
        return self._internal_transactions(*args, **kwargs)

    
    
    def get_account_transactions(self, address: str, start_block: int, end_block: int, sort_type: SortType | str, page: int, offset: int, tag: str):
        '''
        ##### Get the transactions of the account.
        ### Args:
            address (str): The address of the account.
            tag (str | Tags): The tag of the process. Use Tags enum to see earliest, latest and pending transactions.
        
        ### Returns:
            Transactions: The transactions of the account.
        
        ### Raises:
            ValueError: If the address is not in valid format.
            APIError: If the API returns an error.
        '''
        if not address_pattern.match(address):
            raise ValueError('The address has to match with valid wallet address format.')
        res = self.request({
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'offset': offset,
            'sort': sort_type.name.lower() if isinstance(sort_type, SortType) else sort_type.lower(),
            'page': page,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        }, {})

        if res['status'] == '0':
            raise APIError(res['result'])
        
        return Transactions(list(map(Transaction, res['result'])))

    def get_token_transfers(self, contract_address: str, address: str, start_block: int, end_block: int, sort_type: SortType | str, page: int, offset: int, tag: AnyStr | Tags):
        res = self.request({
            'module': 'account',
            'action': 'tokentx',
            'contractaddress': contract_address,
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'offset': offset,
            'sort': sort_type.name.lower() if isinstance(sort_type, SortType) else sort_type.lower(),
            'page': page,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0':
            raise APIError(res['result'])
        
        transfers = TokenTransfers(list(map(TokenTransfer, res['result'])))
        transfers.account = address
        return transfers
    
    def get_erc721_transfers(self, contract_address: str, address: str, start_block: int, end_block: int, sort_type: SortType | str, page: int, offset: int, tag: AnyStr | Tags):
        res = self.request({
            'module': 'account',
            'action': 'tokennfttx',
            'contractaddress': contract_address,
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'offset': offset,
            'sort': sort_type.name.lower() if isinstance(sort_type, SortType) else sort_type.lower(),
            'page': page,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0' and not isinstance(res['result'], list):
            raise APIError(res['result'])
        
        transfers = TokenTransfers(list(map(TokenTransfer, res['result'])))
        transfers.account = address
        return transfers
    
    def get_erc1155_transfers(self, contract_address: str, address: str, start_block: int, end_block: int, sort_type: SortType | str, page: int, offset: int, tag: AnyStr | Tags):
        res = self.request({
            'module': 'account',
            'action': 'token1155tx',
            'contractaddress': contract_address,
            'address': address,
            'startblock': start_block,
            'endblock': end_block,
            'offset': offset,
            'sort': sort_type.name.lower() if isinstance(sort_type, SortType) else sort_type.lower(),
            'page': page,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0' and not isinstance(res['result'], list):
            raise APIError(res['result'])
        
        transfers = TokenTransfers(list(map(TokenTransfer, res['result'])))
        transfers.account = address
        return transfers
    
    def get_account_balance(self, address: list | str, tag: AnyStr | Tags = Tags.LATEST) -> Union[Balance, Balances]:
        '''
        ##### Get the balance(s) of the account(s) up to 20.
        ### Args:
            address (str | list): The address of the account or a list of addresses.
            tag (str | Tags): The tag of the process. Use Tags enum to see earliest, latest and pending balance.
        
        ### Returns:
            Balance | Balances: The balance of the account or a list of balances.
        
        ### Raises:
            ValueError: If the address is not in valid format.
            APIError: If the API returns an error.
        '''
        if isinstance(address, (list, tuple)):
            if not all(address_pattern.match(item) for item in address):
                raise ValueError('All addresses have to match with valid wallet address format.')
            if len(address) > 20:
                print('You can\'t get the balance of more than 20 addresses at once. First 20 addresses will be used.')
            res = self.request({
            'module': 'account',
            'action':'balancemulti',
            'address': ','.join(address),
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
            },{
                'User-Agent': user_agent.generate_user_agent()
            })
            print(res)
            if not res['status'] == '1':
                raise APIError(res['result'], res['message'])
            return Balances(list(map(lambda item: Balance(int(item['balance']), item['account']), res['result'])))
        else:
            if not address_pattern.match(address):
                raise ValueError('Invalid address format.')
            res = self.request({
            'module': 'account',
            'action':'balance',
            'address': address,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
            },{
                'User-Agent': user_agent.generate_user_agent()
            })
            if not res['status'] == '1':
                raise APIError(res['result'], res['message'])
            return Balance(int(res['result']), address)
    def get_contract_abi(self, contract_address: str) -> dict:
        res = self.request({
            'module': 'contract',
            'action': 'getabi',
            'address': contract_address
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0' and not isinstance(res['result'], list):
            raise APIError(res['result'])
        return json.loads(res['result'])
    
    def get_contract_source_code(self, contract_address: str) -> dict:
        res = self.request({
            'module': 'contract',
            'action': 'getsourcecode',
            'address': contract_address
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0' and not isinstance(res['result'], list):
            raise APIError(res['result'])
        return res['result']
    
    def get_contract_creation_hash(self, contract_addresses: str | list[str]) -> Creation | Creations:
        if isinstance(contract_addresses, (list, tuple)):
            if not all(address_pattern.match(item) for item in contract_addresses):
                raise ValueError('All addresses have to match with valid wallet address format.')
            res = self.request({
            'module': 'logs',
            'action':'getcontractcreation',
            'address': ','.join(contract_addresses)
            },{
                'User-Agent': user_agent.generate_user_agent()
            })
            if not res['status'] == '1' and not isinstance(res['result'], list):
                raise APIError(res['result'])
            return Creations(list(map(Creation, res['result'])))
        else:
            if not address_pattern.match(contract_addresses):
                raise ValueError('Invalid address format.')
            res = self.request({
            'module': 'contract',
            'action':'getcontractcreation',
            'contractaddresses': contract_addresses
            },{
                'User-Agent': user_agent.generate_user_agent()
            })
            if not res['status'] == '1' and not isinstance(res['result'], list):
                raise APIError(res['result'])
            return Creation(res['result'][0])
    def check_transaction_receipt_status(self, tx_hash: str) -> Success[bool]:
        res = self.request({
            'module': 'transaction',
            'action': 'gettxreceiptstatus',
            'txhash': tx_hash
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0':
            raise APIError(res['result'])
        return (
            Success()
            if res['result']['status'] == '1'
            else ~Success()
        )
    def check_contract_execution_status(self, txhash: str) -> Success[bool]:
        res = self.request({
            'module': 'transaction',
            'action': 'getstatus',
            'txhash': txhash
        }, {
            'User-Agent': user_agent.generate_user_agent()
        })

        if res['status'] == '0':
            raise APIError(res['result'])
        if res['result']['isError'] == '0':
            return Success() & Message(res['result']['errDescription'])
        return ~Success() & Message(res['result']['errDescription'])
    def get_token_account_balance(self, contract_address: str, address: str, tag: AnyStr | Tags = Tags.LATEST) -> Balance:
        '''
        ##### Get the balance of the account for the ERC20-Token.
        ### Args:
            contract_address (str): The address of the ERC20-Token contract.
            address (str): The address of the account.
            tag (str | Tags): The tag of the process. Use Tags enum to see earliest, latest and pending balance.
        
        ### Returns:
            Balance: The balance of the account.
        
        ### Raises:
            ValueError: If the address is not in valid format.
            APIError: If the API returns an error.
        '''
        if not address_pattern.match(address):
            raise ValueError('Invalid address format.')
        res = self.request({
            'module': 'account',
            'action':'tokenbalance',
            'contractaddress': contract_address,
            'address': address,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        },{
            'User-Agent': user_agent.generate_user_agent()
        })
        print(res)
        if not res['status'] == '1':
            raise APIError(res['result'], res['message'])
        return Balance(int(res['result']), address, token_balance=True)
    def get_token_total_supply(self, contract_address: str, tag: AnyStr | Tags = Tags.LATEST) -> Balance:
        '''
        ##### Get the total supply of the ERC20-Token.
        ### Args:
            contract_address (str): The address of the ERC20-Token contract.
            tag (str | Tags): The tag of the process. Use Tags enum to see earliest, latest and pending balance.
        
        ### Returns:
            Balance: The total supply of the token.
        
        ### Raises:
            APIError: If the API returns an error.
        '''
        res = self.request({
            'module': 'stats',
            'action':'tokensupply',
            'contractaddress': contract_address,
            'tag': tag.name.lower() if isinstance(tag, Tags) else tag.lower()
        },{
            'User-Agent': user_agent.generate_user_agent()
        })
        if not res['status'] == '1':
            raise APIError(res['result'], res['message'])
        return Balance(int(res['result']), contract_address, token_balance=True)