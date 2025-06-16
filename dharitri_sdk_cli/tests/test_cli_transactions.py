import json
from pathlib import Path
from typing import Any

from dharitri_sdk_cli.cli import main

testdata_path = Path(__file__).parent / "testdata"
testdata_out = Path(__file__).parent / "testdata-out"


def test_create_tx_and_sign_by_hash(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "89",
            "--gas-limit",
            "50000",
            "--version",
            "2",
            "--options",
            "1",
            "--chain",
            "integration tests chain ID",
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)
    signature = tx_json["emittedTransaction"]["signature"]
    assert (
        signature
        == "45307099ecebc140bdc5f71f088dfe59dd324839061a36d1c22093a2144f77ba2914f6470da6e92a97e43d7a0a9ebeb7f0f5371ad62428718c5163a513567c0e"
    )


def test_create_move_balance_transaction(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "215",
            "--gas-limit",
            "500000",
            "--value",
            "1000000000000",
            "--data",
            "hello",
            "--version",
            "2",
            "--options",
            "0",
            "--chain",
            "T",
        ]
    )
    assert return_code == 0
    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)
    signature = tx_json["emittedTransaction"]["signature"]
    assert (
        signature
        == "5c90025e3361cbe0a28eddbe89d52c3c63d66b1ea22e3bc628d60b352539723b22a8fa3b6f5df6f4f79012f8a7497cb255af3b1e1fa86c1f09d262fc8810b608"
    )


def test_create_multi_transfer_transaction(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "212",
            "--gas-limit",
            "5000000",
            "--token-transfers",
            "SSSSS-941b91-01",
            "1",
            "TEST-738c3d",
            "1200000000",
            "--version",
            "2",
            "--options",
            "0",
            "--chain",
            "T",
        ]
    )
    assert return_code == 0
    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)
    signature = tx_json["emittedTransaction"]["signature"]
    assert (
        signature
        == "1619eba8bcabfdb08ef9170464d5424819e79b4821057d11120ab6577c7327c88263853bdf55cec3acf2d75a1c91cd9d3d694162503a8586e52e6b6da4011207"
    )


def test_create_multi_transfer_transaction_with_single_rewa_transfer(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "7",
            "--gas-limit",
            "1300000",
            "--token-transfers",
            "REWA-000000",
            "1000000000000000000",
            "--chain",
            "T",
        ]
    )
    assert return_code == 0
    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)
    data = tx_json["emittedTransactionData"]
    assert (
        data
        == "MultiDCDTNFTTransfer@8049d639e5a6980d1cd2392abcce41029cda74a1563523a202f09641cc2618f8@01@524557412d303030303030@@0de0b6b3a7640000"
    )


def test_relayed_v3_without_relayer_wallet(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "7",
            "--gas-limit",
            "1300000",
            "--value",
            "1000000000000000000",
            "--chain",
            "T",
            "--relayer",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
        ]
    )
    assert return_code == 0
    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["relayer"] == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    assert tx_json["signature"]
    assert not tx_json["relayerSignature"]


def test_relayed_v3_incorrect_relayer():
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "7",
            "--gas-limit",
            "1300000",
            "--value",
            "1000000000000000000",
            "--chain",
            "T",
            "--relayer",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--relayer-pem",
            str(testdata_path / "alice.pem"),
        ]
    )
    assert return_code


def test_create_relayed_v3_transaction(capsys: Any):
    # create relayed v3 tx and save signature and relayer signature
    # create the same tx, save to file
    # sign from file with relayer wallet and make sure signatures match
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "7",
            "--gas-limit",
            "1300000",
            "--value",
            "1000000000000000000",
            "--chain",
            "T",
            "--relayer",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--relayer-pem",
            str(testdata_path / "testUser.pem"),
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["relayer"] == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    assert tx_json["signature"]
    assert tx_json["relayerSignature"]

    initial_sender_signature = tx_json["signature"]
    initial_relayer_signature = tx_json["relayerSignature"]

    # Clear the captured content
    capsys.readouterr()

    # save tx to file then load and sign tx by relayer
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "7",
            "--gas-limit",
            "1300000",
            "--value",
            "1000000000000000000",
            "--chain",
            "T",
            "--relayer",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--outfile",
            str(testdata_out / "relayed.json"),
        ]
    )
    assert return_code == 0

    # Clear the captured content
    capsys.readouterr()

    return_code = main(
        [
            "tx",
            "relay",
            "--relayer-pem",
            str(testdata_path / "testUser.pem"),
            "--infile",
            str(testdata_out / "relayed.json"),
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["signature"] == initial_sender_signature
    assert tx_json["relayerSignature"] == initial_relayer_signature

    # Clear the captured content
    capsys.readouterr()


def test_check_relayer_wallet_is_provided():
    return_code = main(["tx", "relay", "--infile", str(testdata_out / "relayed.json")])
    assert return_code


def test_create_plain_transaction(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "89",
            "--gas-limit",
            "50000",
            "--chain",
            "test",
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]

    assert tx_json["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["chainID"] == "test"
    assert tx_json["gasLimit"] == 50000
    assert tx_json["version"] == 2
    assert tx_json["options"] == 0
    assert (
        tx_json["signature"]
        == "7064ec73db20fbe13b237815c73387f8beeee2ebb2068a47bce8da2ce2d00c86782af9c54ad0fe2440eefe32b3e424c691b8915779b075af7cd6f48af3dde80c"
    )


def test_sign_transaction(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--nonce",
            "89",
            "--gas-limit",
            "50000",
            "--chain",
            "test",
            "--outfile",
            str(testdata_out / "transaction.json"),
            "--guardian",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--relayer",
            "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k",
        ]
    )
    assert return_code == 0
    assert (testdata_out / "transaction.json").is_file()

    return_code = main(
        [
            "tx",
            "sign",
            "--infile",
            str(testdata_out / "transaction.json"),
            "--guardian-pem",
            str(testdata_path / "testUser.pem"),
            "--relayer-pem",
            str(testdata_path / "testUser2.pem"),
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]

    assert tx_json["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["chainID"] == "test"
    assert tx_json["gasLimit"] == 50000
    assert tx_json["version"] == 2
    assert tx_json["options"] == 2
    assert tx_json["guardian"] == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    assert tx_json["relayer"] == "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"
    assert (
        tx_json["signature"]
        == "ca295e624caa593d00ba17ede487bdb7241112ea6ad4126519125979af373b66aab1d6f0ff68cc5d4a65059dc0c7f7fd37118ea904356b601fed02b22927530c"
    )
    assert (
        tx_json["guardianSignature"]
        == "8133286c1e56205f99209665fbca9c34d6541c43c86831ac4e9afe385e8286814ce2ef79bcc9503d52ac68ac0c8dbcfcba06e3d6d8f226c7780b554fb457010c"
    )
    assert (
        tx_json["relayerSignature"]
        == "8bdf45edd1409c455ec0ba7d566581eadac4ad3b4f63134d5f118acb9c37e16a4f92f1694b1255cc07762c1ed8f3a9cbfb00f1679f601ab58c96ee8e49b61909"
    )


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout
