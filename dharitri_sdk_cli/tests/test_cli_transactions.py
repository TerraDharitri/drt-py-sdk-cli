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
        == "97500cef697c580695ddd2f589458bf1041da3a5a8e9217d497a84ede171d99236c71cdabb4b2abc82322d94a757338ca320a3016c7bb443ac6284cc4af9390f"
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
        == "7f055de622b1f150163f5e015071a4fd510b510112ada12e604ac56f1af6694e0d8c418be6b4dc8c5cfc8f90f81abc40a89ce51f2c33993efb112d19eee09d0c"
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
        == "8e3c0bb52201332c76f75523fc0b8157c823d0fa09f0fcce0355457add9d19334566fb39f50ac8c2201bb82281a9e6d4a2bc9992ae6b46c4fa72d6b7d8b2f30f"
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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
        ]
    )
    assert return_code == 0
    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["relayer"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
            "--relayer-pem",
            str(testdata_path / "testUser.pem"),
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["relayer"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
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

    assert tx_json["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["chainID"] == "test"
    assert tx_json["gasLimit"] == 50000
    assert tx_json["version"] == 2
    assert tx_json["options"] == 0
    assert (
        tx_json["signature"]
        == "ad0d823f4b85f113a2ac43e0949c6b476035cfad9aae67cb6877628ecea159623a52af5b86a8c41cf8f7d50d8c9e95677221489e5f2ebe03564d76c0469ab507"
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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
            "--relayer",
            "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct",
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

    assert tx_json["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx_json["receiver"] == "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c"
    assert tx_json["chainID"] == "test"
    assert tx_json["gasLimit"] == 50000
    assert tx_json["version"] == 2
    assert tx_json["options"] == 2
    assert tx_json["guardian"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
    assert tx_json["relayer"] == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
    assert (
        tx_json["signature"]
        == "bd92c7ce737871d5bc413d9e358a4075921efef545b50aac8cd083ac1970b66bd3b25fe25fadf3535faeeb76bd047600e66b0cdb3b44cb6860197b641ed9ff08"
    )
    assert (
        tx_json["guardianSignature"]
        == "146fdb95b0d11d5f4eaa269c76182b69128cbd8de022a62f7415ec29f08a5a7648ce0e9e8094f35c1a16970916dc6bb6c2d1d379e49b7443564b1360bb0b9e02"
    )
    assert (
        tx_json["relayerSignature"]
        == "e3d1e4ef55e946d656706f9e3619e4f48ebe5dd3904ec9295ae3bed002155401f8466690c6f72de8f1f4f7dfdd197b03a05fc8a5f163c6f8168d9a05f7e05c03"
    )


def test_estimate_gas(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--proxy",
            "https://devnet-gateway.dharitri.org",
            "--value",
            "1000000000000",
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["gasLimit"] == 50000


def test_estimate_gas_for_guarded_tx(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--proxy",
            "https://devnet-gateway.dharitri.org",
            "--value",
            "1000000000000",
            "--guardian",
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["gasLimit"] == 100000


def test_estimate_gas_with_multiplier(capsys: Any):
    return_code = main(
        [
            "tx",
            "new",
            "--pem",
            str(testdata_path / "alice.pem"),
            "--receiver",
            "drt1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqlqde3c",
            "--proxy",
            "https://devnet-gateway.dharitri.org",
            "--gas-limit-multiplier",
            "1.5",
            "--value",
            "1000000000000",
        ]
    )
    assert return_code == 0

    tx = _read_stdout(capsys)
    tx_json = json.loads(tx)["emittedTransaction"]
    assert tx_json["gasLimit"] == 75000


def test_raise_error_when_data_and_transfers_provided(capsys: Any):
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
            "--chain",
            "D",
            "--data",
            "hello",
            "--token-transfers",
            "TEST-123456",
        ]
    )
    assert return_code == 1


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout
