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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
            "--relayer-pem",
            str(user),
        ]
    )
    assert not return_code

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqpgq2leexk6fwaxlxggzrnkxzruwsjzfcq2mqzgq7hwwcs"
    assert tx["value"] == "0"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 15000000
    assert tx["chainID"] == "T"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert tx["relayer"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
    assert (
        tx["signature"]
        == "42ca28c45a0d09fbc6f1c804a16d3b6df13f97598d2f0390e6b6cf159a01085d0aa885c511b48df8b088212bdbd2d4f1ceed26bfff532cec840f79637a626508"
    )
    assert (
        tx["relayerSignature"]
        == "8dad8988da5cbdf7cc3def9e2990bcd57d793e87a5254ecd6951c52de0c8978bd00e8e71606606f9a77c99700ea97139cd5c969e33cd4c8d360108173ac7a60a"
    )
    assert data == "register@616c6963652e6e756d626174"


def get_output(capsys: Any):
    tx = _read_stdout(capsys)
    return json.loads(tx)


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout
