import json
from pathlib import Path
from typing import Any

from dharitri_sdk_cli.cli import main

testdata_path = Path(__file__).parent / "testdata"


def test_prepare_relayed_dns_register_transaction(capsys: Any):
    alice = testdata_path / "alice.pem"
    user = testdata_path / "testUser.pem"

    return_code = main(
        [
            "dns",
            "register",
            "--pem",
            str(alice),
            "--name",
            "alice.numbat",
            "--nonce",
            "0",
            "--gas-limit",
            "15000000",
            "--chain",
            "T",
            "--relayer",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--relayer-pem",
            str(user),
        ]
    )
    assert not return_code

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqpgq2leexk6fwaxlxggzrnkxzruwsjzfcq2mqzgq7hwwcs"
    assert tx["value"] == "0"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 15000000
    assert tx["chainID"] == "T"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert tx["relayer"] == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    assert (
        tx["signature"]
        == "cd7bf57dafbfd96bc95c7c4d0edd041c51491bdd9e598e7a1ce90a859ef7e8de07365042273fdb3fa6754743b0c36c67f6fc07ba42621847dac66d43b6132c08"
    )
    assert (
        tx["relayerSignature"]
        == "e9ddd59b313c81951ff7f6e4c40e35ce79738da09b8e29aa90d93893566a8b18709bc86b96deaa151cbdb4a7f1e496e601f9d93d64dea269ede19f8e2fcb3f00"
    )
    assert data == "register@616c6963652e6e756d626174"


def get_output(capsys: Any):
    tx = _read_stdout(capsys)
    return json.loads(tx)


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout
