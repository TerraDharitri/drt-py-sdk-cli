import logging
from pathlib import Path

from Cryptodome.Hash import keccak
from dharitri_py_sdk import Account, Address, TransactionsFactoryConfig

from dharitri_sdk_cli.contract_verification import _create_request_signature
from dharitri_sdk_cli.contracts import SmartContract

logging.basicConfig(level=logging.INFO)

testdata_folder = Path(__file__).parent / "testdata"


def test_playground_keccak():
    hexhash = keccak.new(digest_bits=256).update(b"").hexdigest()
    assert hexhash == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"


def test_contract_verification_create_request_signature():
    account = Account.new_from_pem(file_path=testdata_folder / "walletKey.pem")
    contract_address = Address.from_bech32("drt1qqqqqqqqqqqqqpgqeyj9g344pqguukajpcfqz9p0rfqgyg4l396qyvkwmg")
    request_payload = b"test"
    signature = _create_request_signature(account, contract_address, request_payload)

    assert (
        signature.hex()
        == "7620b2754d03872720f8eb00d81365f37c670216c2a73695f2c3fbd1d2ae3fdb49a3a0a9f7f9f91b4a2cc8fa2effba3c16a44d08443db43da4f59ae1ba6e0400"
    )


def test_prepare_args_for_factories():
    sc = SmartContract(TransactionsFactoryConfig("mock"))
    args = [
        "0x5",
        "123",
        "false",
        "true",
        "str:test-string",
        "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l",
    ]

    arguments = sc._prepare_args_for_factory(args)
    assert arguments[0].get_payload() == b"\x05"
    assert arguments[1].get_payload() == 123
    assert arguments[2].get_payload() is False
    assert arguments[3].get_payload() is True
    assert arguments[4].get_payload() == "test-string"
    assert (
        arguments[5].get_payload()
        == Address.new_from_bech32("drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l").get_public_key()
    )
