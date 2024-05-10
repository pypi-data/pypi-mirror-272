"""
BaseScan API Wrapper for Python.

BaseScan is a block explorer of the Base Chain. This API Wrapper is a Python implementation of the BaseScan API.

See contents of library below:

Modules:
    - errors.py
    - utils.py

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

Errors:
    - APIError: Exception class for API errors.
"""

__version__ = "0.1.0"
__all__ = [
    "Tags",
    "SortType",
    "Message",
    "Status",
    "Success",
    "BinanceTicker",
    "Transaction",
    "Balance",
    "TokenTransfer",
    "Transactions",
    "TokenTransfers",
    "Balances",
    "APIError"
]
import os
from .errors import APIError, InvalidAPIKey
from .utils import (
    Tags,
    SortType,
    Message,
    Status,
    Success,
    BinanceTicker,
    Transaction,
    Balance,
    TokenTransfer,
    Transactions,
    TokenTransfers,
    Balances
)


env = os.environ
API_KEY = env.get("API_KEY")
if not API_KEY:
    raise InvalidAPIKey("API_KEY variable not found in environment variables.", str(API_KEY))