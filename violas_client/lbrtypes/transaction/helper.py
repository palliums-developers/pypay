import datetime
from violas_client.lbrtypes.transaction import TransactionPayload, RawTransaction, SignedTransaction
from violas_client.libra_client.account import Account
from violas_client.crypto.ed25519 import ED25519_SIGNATURE_LENGTH
from violas_client.lbrtypes.transaction.authenticator import TransactionAuthenticator
from violas_client.crypto.hash import hash_seed

def create_unsigned_txn(
    payload: TransactionPayload,
    sender_address,
    sender_sequence_number,
    max_gas_amount,
    gas_unit_price,
    gas_currency_code,
    txn_expiration,
    chain_id
) -> RawTransaction:
    return RawTransaction(
        sender_address,
        sender_sequence_number,
        payload,
        max_gas_amount,
        gas_unit_price,
        gas_currency_code,
        int(datetime.datetime.now().timestamp()) + txn_expiration,
        chain_id
    )

def create_user_txn(
    payload,
    sender_account: Account,
    sender_sequence_number,
    max_gas_amount,
    gas_unit_price,
    gas_currency_code,
    txn_expiration,
    chain_id
) -> SignedTransaction:
    raw_txn = create_unsigned_txn(
        payload,
        sender_account.address,
        sender_sequence_number,
        max_gas_amount,
        gas_unit_price,
        gas_currency_code,
        txn_expiration,
        chain_id
    )
    signature = sender_account.sign(hash_seed(b"RawTransaction")+raw_txn.serialize())[:ED25519_SIGNATURE_LENGTH]
    authenticator = TransactionAuthenticator.ed25519(sender_account.public_key, signature)
    return SignedTransaction(raw_txn, authenticator)


