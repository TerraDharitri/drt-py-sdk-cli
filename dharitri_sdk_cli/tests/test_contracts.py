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
    contract_address = Address.new_from_bech32("drt1qqqqqqqqqqqqqpgqeyj9g344pqguukajpcfqz9p0rfqgyg4l396qyvkwmg")
    request_payload = b"test"
    signature = _create_request_signature(account, contract_address, request_payload)

    assert (
        signature.hex()
        == "dc7dbc3b1f54539f4c8b09eabb789de3e719ce1090c6f8b4d1ab6aa00265b580934464e2af5539a3a20094f04fa4cbbbfe205c789693419fcd29919321c9600e"
    )


def test_prepare_args_for_factories():
    sc = SmartContract(TransactionsFactoryConfig("mock"))
    args = [
        "0x5",
        "123",
        "false",
        "true",
        "str:test-string",
        "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf",
    ]

    arguments = sc._convert_args_to_typed_values(args)
    assert arguments[0].get_payload() == b"\x05"
    assert arguments[1].get_payload() == 123
    assert arguments[2].get_payload() is False
    assert arguments[3].get_payload() is True
    assert arguments[4].get_payload() == "test-string"
    assert (
        arguments[5].get_payload()
        == Address.new_from_bech32("drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf").get_public_key()
    )
