import json
from pathlib import Path

from dharitri_sdk_cli.cli import main


def test_sign_tx():
    parent = Path(__file__).parent
    unsigned_transaction = parent / "testdata" / "transaction.json"
    signed_transaction = parent / "testdata-out" / "signed_transaction.json"
    expected_signature = "f973e03e98b0638e8f54acb5e694859e9ee964758eea79d5447e6fea35b043be79ef66d695065f8159ab133b5699b2df488cc52911c07b5a7c869f4ab7814a04"

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
