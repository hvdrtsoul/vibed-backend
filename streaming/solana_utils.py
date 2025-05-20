from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
from spl.token.instructions import (
    get_associated_token_address,
    create_associated_token_account,
    transfer,
    TransferParams
)
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from dotenv import load_dotenv
import os
import json

load_dotenv()

SOLANA_URL = os.getenv("SOLANA_URL", "https://api.devnet.solana.com")
TOKEN_ADDRESS = PublicKey(os.getenv("SOLANA_TOKEN_ADDRESS"))
SENDER_KEYPAIR_PATH = os.getenv("SOLANA_KEYPAIR_PATH")
SENDER_TOKEN_ACCOUNT = PublicKey(os.getenv("SOLANA_OWNER_ACCOUNT"))
client = Client(SOLANA_URL)

def load_keypair_from_file(path):
    with open(path, "r") as f:
        secret = json.load(f)
    return Keypair.from_secret_key(bytes(secret))

def reward_user_with_tokens(user_wallet_str: str, amount: float = 1.0):
    user_wallet = PublicKey(user_wallet_str)
    sender = load_keypair_from_file(SENDER_KEYPAIR_PATH)

    user_token_account = get_associated_token_address(user_wallet, TOKEN_ADDRESS)

    resp = client.get_account_info(user_token_account)
    if resp["result"]["value"] is None:
        print("Создаём ATA для пользователя...")
        tx = Transaction()
        tx.add(
            create_associated_token_account(
                payer=sender.public_key,
                owner=user_wallet,
                mint=TOKEN_ADDRESS
            )
        )
        client.send_transaction(tx, sender)

    tx2 = Transaction()
    tx2.add(
        transfer(
            TransferParams(
                program_id=TOKEN_PROGRAM_ID,
                source=SENDER_TOKEN_ACCOUNT,
                dest=user_token_account,
                owner=sender.public_key,
                amount=int(amount * 1_000_000_000)
            )
        )
    )

    result = client.send_transaction(tx2, sender, opts=TxOpts(skip_preflight=True))
    return result
