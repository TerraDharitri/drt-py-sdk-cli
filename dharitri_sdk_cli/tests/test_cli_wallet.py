import getpass
import json
from pathlib import Path
from typing import Any

from dharitri_py_sdk import Address, AddressComputer, Mnemonic, UserPEM, UserWallet

from dharitri_sdk_cli.cli import main

testdata_path = Path(__file__).parent / "testdata"
testdata_out_path = Path(__file__).parent / "testdata-out"


def test_wallet_new(capsys: Any):
    main(["wallet", "new"])
    displayed_mnemonic = _read_stdout_mnemonic(capsys)
    assert Mnemonic.is_text_valid(displayed_mnemonic)


def test_generate_wallet_in_specific_shard(capsys: Any):
    address_computer = AddressComputer()

    main(["wallet", "new", "--shard", "0"])
    address = Address.new_from_bech32(_read_stdout_wallet_address(capsys))
    assert address_computer.get_shard_of_address(address) == 0

    main(["wallet", "new", "--shard", "1"])
    address = Address.new_from_bech32(_read_stdout_wallet_address(capsys))
    assert address_computer.get_shard_of_address(address) == 1

    main(["wallet", "new", "--shard", "2"])
    address = Address.new_from_bech32(_read_stdout_wallet_address(capsys))
    assert address_computer.get_shard_of_address(address) == 2


def test_wallet_new_and_save_in_pem_format(capsys: Any):
    outfile = testdata_out_path / "testWallet.pem"
    outfile.unlink(missing_ok=True)
    main(["wallet", "new", "--format", "pem", "--outfile", str(outfile)])

    expected_secret_key = Mnemonic(_read_stdout_mnemonic(capsys)).derive_key(0)
    actual_secret_key = UserPEM.from_file(outfile).secret_key
    assert actual_secret_key.hex() == expected_secret_key.hex()


def test_wallet_new_and_save_in_json_format(capsys: Any, monkeypatch: Any):
    outfile = testdata_out_path / "testWallet.json"
    outfile.unlink(missing_ok=True)
    _mock_getpass(monkeypatch, "password")
    main(["wallet", "new", "--format", "keystore-mnemonic", "--outfile", str(outfile)])

    expected_mnemonic = Mnemonic(_read_stdout_mnemonic(capsys))
    keyfile = json.loads(outfile.read_text())
    actual_mnemonic = UserWallet.decrypt_mnemonic(keyfile, "password")
    assert actual_mnemonic.get_text() == expected_mnemonic.get_text()


def test_wallet_new_as_mnemonic():
    outfile = testdata_out_path / "wallet.txt"
    outfile.unlink(missing_ok=True)

    main(["wallet", "new", "--format", "raw-mnemonic", "--outfile", str(outfile)])

    assert Mnemonic.is_text_valid(outfile.read_text())


def test_wallet_new_as_pem():
    outfile = testdata_out_path / "wallet.pem"
    outfile.unlink(missing_ok=True)

    main(
        [
            "wallet",
            "new",
            "--format",
            "pem",
            "--outfile",
            str(outfile),
            "--address-hrp",
            "drt",
        ]
    )

    assert UserPEM.from_file(outfile).label.startswith("drt1")

    outfile.unlink(missing_ok=True)

    main(
        [
            "wallet",
            "new",
            "--format",
            "pem",
            "--outfile",
            str(outfile),
            "--address-hrp",
            "test",
        ]
    )

    assert UserPEM.from_file(outfile).label.startswith("test1")


def test_wallet_new_as_keystore_with_mnemonic(capsys: Any, monkeypatch: Any):
    outfile = testdata_out_path / "keystore-with-mnemonic.json"
    outfile.unlink(missing_ok=True)
    _mock_getpass(monkeypatch, "password")

    main(["wallet", "new", "--format", "keystore-mnemonic", "--outfile", str(outfile)])

    expected_mnemonic = _read_stdout_mnemonic(capsys)
    keyfile = json.loads(outfile.read_text())
    actual_mnemonic = UserWallet.decrypt_mnemonic(keyfile, "password")
    assert actual_mnemonic.get_text() == expected_mnemonic


def test_wallet_new_as_keystore_with_secret_key(capsys: Any, monkeypatch: Any):
    outfile = testdata_out_path / "keystore-with-mnemonic.json"
    outfile.unlink(missing_ok=True)
    _mock_getpass(monkeypatch, "password")

    main(["wallet", "new", "--format", "keystore-secret-key", "--outfile", str(outfile)])

    expected_secret_key = Mnemonic(_read_stdout_mnemonic(capsys)).derive_key(0)
    actual_secret_key = UserWallet.load_secret_key(outfile, "password")
    assert actual_secret_key.hex() == expected_secret_key.hex()


def test_wallet_convert_raw_mnemonic_to_pem():
    infile = testdata_path / "mnemonic.txt"
    outfile = testdata_out_path / "alice.pem"
    outfile.unlink(missing_ok=True)

    main(
        [
            "wallet",
            "convert",
            "--in-format",
            "raw-mnemonic",
            "--infile",
            str(infile),
            "--out-format",
            "pem",
            "--outfile",
            str(outfile),
            "--address-index",
            "0",
        ]
    )

    pem = UserPEM.from_file(outfile)
    assert pem.label == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert pem.secret_key.hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"


def test_wallet_convert_raw_mnemonic_to_keystore_with_mnemonic(monkeypatch: Any):
    infile = testdata_path / "mnemonic.txt"
    outfile = testdata_out_path / "keystore_with_mnemonic.json"

    outfile.unlink(missing_ok=True)
    _mock_getpass(monkeypatch, "password")

    main(
        [
            "wallet",
            "convert",
            "--in-format",
            "raw-mnemonic",
            "--infile",
            str(infile),
            "--out-format",
            "keystore-mnemonic",
            "--outfile",
            str(outfile),
        ]
    )

    keyfile_json = outfile.read_text()
    keyfile = json.loads(keyfile_json)
    mnemonic = UserWallet.decrypt_mnemonic(keyfile, "password")
    assert mnemonic.get_text() == infile.read_text()


def test_wallet_convert_raw_mnemonic_to_keystore_with_secret_key(monkeypatch: Any):
    infile = testdata_path / "mnemonic.txt"
    outfile = testdata_out_path / "keystore_with_secret_key.json"

    # Alice
    outfile.unlink(missing_ok=True)
    _mock_getpass(monkeypatch, "password")

    main(
        [
            "wallet",
            "convert",
            "--in-format",
            "raw-mnemonic",
            "--infile",
            str(infile),
            "--out-format",
            "keystore-secret-key",
            "--outfile",
            str(outfile),
            "--address-index",
            "0",
        ]
    )

    keyfile_json = outfile.read_text()
    keyfile = json.loads(keyfile_json)
    secret_key = UserWallet.decrypt_secret_key(keyfile, "password")
    assert secret_key.hex() == "413f42575f7f26fad3317a778771212fdb80245850981e48b58a4f25e344e8f9"

    # Bob
    outfile.unlink(missing_ok=True)
    main(
        [
            "wallet",
            "convert",
            "--in-format",
            "raw-mnemonic",
            "--infile",
            str(infile),
            "--out-format",
            "keystore-secret-key",
            "--outfile",
            str(outfile),
            "--address-index",
            "1",
        ]
    )

    keyfile_json = outfile.read_text()
    keyfile = json.loads(keyfile_json)
    secret_key = UserWallet.decrypt_secret_key(keyfile, "password")
    assert secret_key.hex() == "b8ca6f8203fb4b545a8e83c5384da033c415db155b53fb5b8eba7ff5a039d639"


def test_wallet_convert_keystore_with_secret_key_to_pem(monkeypatch: Any):
    infile = testdata_path / "alice.json"
    outfile = testdata_out_path / "alice.pem"

    outfile.unlink(missing_ok=True)
    _mock_getpass(monkeypatch, "password")

    main(
        [
            "wallet",
            "convert",
            "--in-format",
            "keystore-secret-key",
            "--infile",
            str(infile),
            "--out-format",
            "pem",
            "--outfile",
            str(outfile),
        ]
    )

    pem = UserPEM.from_file(outfile)
    assert pem.label == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert pem.secret_key.hex() == "7b4686f3c925f9f6571de5fa24fb6a7ac0a2e5439a48bad8ed90b6690aad6017"


def test_wallet_bech32_encode(capsys: Any):
    main(
        [
            "wallet",
            "bech32",
            "--encode",
            "c782420144e8296f757328b409d01633bf8d09d8ab11ee70d32c204f6589bd24",
        ]
    )

    out = _read_stdout(capsys)
    assert out == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"


def test_wallet_bech32_decode(capsys: Any):
    main(
        [
            "wallet",
            "bech32",
            "--decode",
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l",
        ]
    )

    out = _read_stdout(capsys)
    assert out == "c782420144e8296f757328b409d01633bf8d09d8ab11ee70d32c204f6589bd24"


def test_wallet_convert_pem_to_bech32_address(capsys: Any):
    infile = testdata_path / "alice.pem"

    main(
        [
            "wallet",
            "convert",
            "--infile",
            str(infile),
            "--in-format",
            "pem",
            "--out-format",
            "address-bech32",
        ]
    )

    out = _read_stdout(capsys).strip("Output:\n\n")
    assert out == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"


def test_wallet_convert_pem_to_pubkey(capsys: Any):
    infile = testdata_path / "alice.pem"

    main(
        [
            "wallet",
            "convert",
            "--infile",
            str(infile),
            "--in-format",
            "pem",
            "--out-format",
            "address-hex",
        ]
    )

    out = _read_stdout(capsys).strip("Output:\n\n")
    assert out == "c782420144e8296f757328b409d01633bf8d09d8ab11ee70d32c204f6589bd24"


def test_wallet_convert_pem_to_secret_key(capsys: Any):
    infile = testdata_path / "alice.pem"

    main(["wallet", "convert", "--infile", str(infile), "--in-format", "pem", "--out-format", "secret-key"])

    out = _read_stdout(capsys).strip("Output:\n\n")
    assert out == "7b4686f3c925f9f6571de5fa24fb6a7ac0a2e5439a48bad8ed90b6690aad6017"


def test_wallet_sign_message(capsys: Any):
    message = "test"
    pem = testdata_path / "alice.pem"

    return_code = main(["wallet", "sign-message", "--message", message, "--pem", str(pem)])
    out = json.loads(_read_stdout(capsys))

    assert False if return_code else True
    assert out == {
        "address": "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l",
        "message": "test",
        "signature": "0x4b9b9293d7aa63b012641485865027adef8b4d4351d27f59ae62979acd49b328876c2fce97a2bed20f2ac12180155494ce1a1dc6103ec78a1ed32c6132734004",
    }


def test_verify_previously_signed_message(capsys: Any):
    message = "test"
    address = "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    signature = "0x4b9b9293d7aa63b012641485865027adef8b4d4351d27f59ae62979acd49b328876c2fce97a2bed20f2ac12180155494ce1a1dc6103ec78a1ed32c6132734004"

    return_code = main(
        [
            "wallet",
            "verify-message",
            "--address",
            address,
            "--message",
            message,
            "--signature",
            signature,
        ]
    )
    assert False if return_code else True

    out = _read_stdout(capsys)
    text = """SUCCESS: The message "test" was signed by drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l""".split()
    assert all(word in out for word in text)


def test_verify_not_signed_message(capsys: Any):
    message = "this message is not signed"
    address = "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    signature = "0x4b9b9293d7aa63b012641485865027adef8b4d4351d27f59ae62979acd49b328876c2fce97a2bed20f2ac12180155494ce1a1dc6103ec78a1ed32c6132734004"

    return_code = main(
        [
            "wallet",
            "verify-message",
            "--address",
            address,
            "--message",
            message,
            "--signature",
            signature,
        ]
    )
    assert False if return_code else True

    out = _read_stdout(capsys)
    text = """FAILED: The message "this message is not signed" was NOT signed by drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l""".split()
    assert all(word in out for word in text)


def test_sign_and_verify_message_with_multi_address_pem(capsys: Any):
    multi_address_pem_path = testdata_path / "multiple_addresses.pem"
    message = "test"

    return_code = main(
        [
            "wallet",
            "sign-message",
            "--message",
            message,
            "--pem",
            str(multi_address_pem_path),
            "--sender-wallet-index",
            "0",
        ]
    )
    out = json.loads(_read_stdout(capsys))

    assert False if return_code else True
    assert out == {
        "address": "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l",
        "message": "test",
        "signature": "0x4b9b9293d7aa63b012641485865027adef8b4d4351d27f59ae62979acd49b328876c2fce97a2bed20f2ac12180155494ce1a1dc6103ec78a1ed32c6132734004",
    }

    return_code = main(
        [
            "wallet",
            "verify-message",
            "--address",
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l",
            "--message",
            message,
            "--signature",
            "0x4b9b9293d7aa63b012641485865027adef8b4d4351d27f59ae62979acd49b328876c2fce97a2bed20f2ac12180155494ce1a1dc6103ec78a1ed32c6132734004",
        ]
    )
    assert False if return_code else True

    out = _read_stdout(capsys)
    text = """SUCCESS: The message "test" was signed by drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l""".split()
    assert all(word in out for word in text)

    return_code = main(
        [
            "wallet",
            "sign-message",
            "--message",
            message,
            "--pem",
            str(multi_address_pem_path),
            "--sender-wallet-index",
            "1",
        ]
    )
    out = json.loads(_read_stdout(capsys))

    assert False if return_code else True
    assert out == {
        "address": "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2",
        "message": "test",
        "signature": "0x77f27d595fb87b24df689948f6aaf2d80a832107b2979098d3e5ac5a30da45e379c0d1edfe0d257fbe338ac4a488417a88933b1e73278bf1321c15ab297c9e0e",
    }

    return_code = main(
        [
            "wallet",
            "verify-message",
            "--address",
            "drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2",
            "--message",
            message,
            "--signature",
            "0x77f27d595fb87b24df689948f6aaf2d80a832107b2979098d3e5ac5a30da45e379c0d1edfe0d257fbe338ac4a488417a88933b1e73278bf1321c15ab297c9e0e",
        ]
    )
    assert False if return_code else True

    out = _read_stdout(capsys)
    text = """SUCCESS: The message "test" was signed by drt18h03w0y7qtqwtra3u4f0gu7e3kn2fslj83lqxny39m5c4rwaectswerhd2""".split()
    assert all(word in out for word in text)

    return_code = main(
        [
            "wallet",
            "sign-message",
            "--message",
            message,
            "--pem",
            str(multi_address_pem_path),
            "--sender-wallet-index",
            "2",
        ]
    )
    out = json.loads(_read_stdout(capsys))

    assert False if return_code else True
    assert out == {
        "address": "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
        "message": "test",
        "signature": "0x0b9bd2bc1251afd81bcab81a6c3aa72e368ca057c21b6dc4d5aafa3eb8dde713e65cd4db7cb1f803abe89e81ee9db1e4d0f449a9bf0ec9b2a8ac0f8e640b8304",
    }

    return_code = main(
        [
            "wallet",
            "verify-message",
            "--address",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--message",
            message,
            "--signature",
            "0x0b9bd2bc1251afd81bcab81a6c3aa72e368ca057c21b6dc4d5aafa3eb8dde713e65cd4db7cb1f803abe89e81ee9db1e4d0f449a9bf0ec9b2a8ac0f8e640b8304",
        ]
    )
    assert False if return_code else True

    out = _read_stdout(capsys)
    text = """SUCCESS: The message "test" was signed by drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q""".split()
    assert all(word in out for word in text)


def _read_stdout_mnemonic(capsys: Any) -> str:
    lines = _read_stdout(capsys).split("\n")
    return lines[0].replace("Mnemonic:", "").strip()


def _read_stdout_wallet_address(capsys: Any) -> str:
    lines = _read_stdout(capsys).split("\n")
    return lines[1].replace("Wallet address:", "").strip()


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout


def _mock_getpass(monkeypatch: Any, password: str):
    monkeypatch.setattr(getpass, "getpass", lambda _: password)  # type: ignore
