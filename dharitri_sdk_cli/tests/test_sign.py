import json
from pathlib import Path

from dharitri_sdk_cli.cli import main


def test_sign_tx():
    parent = Path(__file__).parent
    unsigned_transaction = parent / "testdata" / "transaction.json"
    signed_transaction = parent / "testdata-out" / "signed_transaction.json"
    expected_signature = "cf3f5a028bdaf62734047a988f6d75fde46621d90d7474594fade4ab41bf45a09607959380f491539766b1eb5e01d4ab290524c358cc95eede8f5b1d0ab9780d"

    main(
        [
            "tx",
            "sign",
            "--pem",
            f"{parent}/testdata/testUser.pem",
            "--infile",
            f"{unsigned_transaction}",
            "--outfile",
            f"{signed_transaction}",
        ]
    )

    with open(signed_transaction) as f:
        signed_tx = json.load(f)

    assert signed_tx["emittedTransaction"]["signature"] == expected_signature
