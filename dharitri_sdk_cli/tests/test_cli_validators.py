import json
from pathlib import Path
from typing import Any

from dharitri_sdk_cli.cli import main

testdata_path = Path(__file__).parent / "testdata"
testdata_out = Path(__file__).parent / "testdata-out"

alice_pem = testdata_path / "alice.pem"
reward_address = "drt1k2s324ww2g0yj38qn2ch2jwctdy8mnfxep94q9arncc6xecg3xaq889n6e"
bls_key = "e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"

relayer = testdata_path / "testUser.pem"
guardian = testdata_path / "testUser2.pem"


def test_stake(capsys: Any):
    validators_pem = testdata_path / "validators_file.pem"

    return_code = main(
        [
            "validator",
            "stake",
            "--pem",
            str(alice_pem),
            "--value",
            "2500000000000000000000",
            "--validators-pem",
            str(validators_pem),
            "--reward-address",
            reward_address,
            "--chain",
            "localnet",
            "--nonce=0",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 11029500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "5469fb058ed27027768196f811dac4b02825c67ced3bfe27543528de710bc8a0acacc32785e72423e7487a8246080b2fac5f935950320c17f33d3594472b220d"
    )
    assert (
        data
        == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1dbc595db6361a15ac59e12745c33dd0b6b9f0e2ac1634fb69e5f77f4865150a5c79055c11e84980a9228a9998fb628e@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@7b902a5c75d527437dfd821702472adf20c88f67d4df24a3b9048d520a6d18e628a08314d963bd12b837593bbcb4020a@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
    )


def test_top_up(capsys: Any):
    return_code = main(
        [
            "validator",
            "stake",
            "--pem",
            str(alice_pem),
            "--value",
            "2500000000000000000000",
            "--top-up",
            "--chain",
            "localnet",
            "--nonce=0",
            "--reward-address",
            "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 5057500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "6e6ba71060ae3ff9e05f9da8e74b27e956ad024861cf595fc27b6ebff2b0d02d4b7689935e4343f04c8476cd7933ed8e50f2233a8cb091093c2c36044fbe0404"
    )
    assert data == "stake"


def test_stake_with_relayer_and_guardian(capsys: Any):
    validators_pem = testdata_path / "validators_file.pem"

    return_code = main(
        [
            "validator",
            "stake",
            "--pem",
            str(alice_pem),
            "--value",
            "2500000000000000000000",
            "--validators-pem",
            str(validators_pem),
            "--reward-address",
            reward_address,
            "--chain",
            "localnet",
            "--nonce=0",
            "--options=2",
            "--relayer",
            "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q",
            "--guardian",
            "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k",
            "--guardian-pem",
            str(guardian),
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 11129500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 2
    assert tx["guardian"] == "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"
    assert tx["relayer"] == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
    assert (
        tx["signature"]
        == "2ebca07b6bb0be4d05bd3905262bf1e9316d9a22ab849e77a852154a5dd339bf696cdae2cb21508ae7704822a9bfb5b2b79b487b66baeece409d6446af8f3604"
    )
    assert (
        tx["guardianSignature"]
        == "38fe3ae725d18f94377b08b58a5e544479aefe7e92e3deb5cf5cb31b01df09db4f4cfb47b4ece1294d3e4d1b2f37cd19a23464b9fbdfeb37f1b5ed22c66c0400"
    )
    assert (
        data
        == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1dbc595db6361a15ac59e12745c33dd0b6b9f0e2ac1634fb69e5f77f4865150a5c79055c11e84980a9228a9998fb628e@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@7b902a5c75d527437dfd821702472adf20c88f67d4df24a3b9048d520a6d18e628a08314d963bd12b837593bbcb4020a@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
    )


def test_stake_top_up(capsys: Any):
    return_code = main(
        [
            "validator",
            "stake",
            "--top-up",
            "--pem",
            str(alice_pem),
            "--value",
            "2711000000000000000000",
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "2711000000000000000000"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5057500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "88498e415b7de01969b951d8cf91af6e18c1c2e15fce00813df57a42c668870c8c08a9a8b9d8b34b1f951e9b794d23547e0405f8252a501831fe5585a7463600"
    )
    assert data == "stake"


def test_unstake(capsys: Any):
    return_code = main(
        [
            "validator",
            "unstake",
            "--pem",
            str(alice_pem),
            "--nodes-public-key",
            bls_key,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5350000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "d0090943d330dd98f802c5289e2215d6b4eef4e378eef45d8e252f01f9a1829057b6dc499126a6e5348bf188bb04282815b1118a515ed317619135da87102d07"
    )
    assert (
        data
        == "unStake@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )


def test_unbond(capsys: Any):
    return_code = main(
        [
            "validator",
            "unbond",
            "--pem",
            str(alice_pem),
            "--nodes-public-key",
            bls_key,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5348500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "4d6c66fd8afa31dead5fa9fe02371307ea5a0375a54977547c09318740d4b75d9b992668b7721b82ed93fb680932d5b1110cd44d0501a4e9f4d3552a0710c000"
    )
    assert (
        data
        == "unBond@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )


def test_unjail(capsys: Any):
    return_code = main(
        [
            "validator",
            "unjail",
            "--pem",
            str(alice_pem),
            "--value",
            "2500000000000000000000",
            "--nodes-public-key",
            bls_key,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5348500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "863104a589b6a167631e330521eca3024d792be3eb87846bd99b265efa010763ef175ca3faba387bb01453223e948a7012baf3820648fa55ea65a9f13f0d980f"
    )
    assert (
        data
        == "unJail@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )


def test_change_reward_address(capsys: Any):
    return_code = main(
        [
            "validator",
            "change-reward-address",
            "--pem",
            str(alice_pem),
            "--reward-address",
            reward_address,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5176000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "3b1b956b4733f5c331a1eb7b549d4cd7106311550246c8b3cde8f445cb79976e0c5a7fb44256dd7df7b8c5c55da023434504215620898eca23cee0bb4fa9500d"
    )
    assert data == "changeRewardAddress@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"


def test_claim(capsys: Any):
    return_code = main(
        [
            "validator",
            "claim",
            "--pem",
            str(alice_pem),
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5057500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "f9a6c55147a2eac64aa81fd7c592a7199be124cbc92c157235dcf42f9a3f9bda9a0271359b029b07ad0f30167d459b615b18d619b226b2cc67ef30e4a4d28b06"
    )
    assert data == "claim"


def test_unstake_nodes(capsys: Any):
    return_code = main(
        [
            "validator",
            "unstake-nodes",
            "--pem",
            str(alice_pem),
            "--nodes-public-key",
            bls_key,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5357500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "0edb5048838791e00aaee2960310e74b17071d5d36446b8c0a803f35d3657cab0a36aba5f4695322904f618cc9580c3448afcf3bc15d9509eb1c86dd1f216f04"
    )
    assert (
        data
        == "unStakeNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )


def test_unstake_tokens(capsys: Any):
    return_code = main(
        [
            "validator",
            "unstake-tokens",
            "--pem",
            str(alice_pem),
            "--unstake-value",
            "11000000000000000000",
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5095000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "dc402cecf430480bbf373a7dcdaea24caa6cb91d1c20609b4ff7445b884a6bfdd6447d6ae4e8cd6f07e64d3cef11bcd72e74cb1c62ada87cb4f652519702eb0a"
    )
    assert data == "unStakeTokens@98a7d9b8314c0000"


def test_unbond_nodes(capsys: Any):
    return_code = main(
        [
            "validator",
            "unbond-nodes",
            "--pem",
            str(alice_pem),
            "--nodes-public-keys",
            bls_key,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5356000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "461599e42ab804133de625896b3494d5754a5f89ec3e02e421e6872ec12437d92f90997719e462adf5d25a19a7d10dc0dde66280fb4b9625ef6a24f6658c7f09"
    )
    assert (
        data
        == "unBondNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )


def test_unbond_tokens(capsys: Any):
    return_code = main(
        [
            "validator",
            "unbond-tokens",
            "--pem",
            str(alice_pem),
            "--unbond-value",
            "20000000000000000000",
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5096500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "158d6d230cf64ff8c996dd1c8ca5e191fab5b4233f1271622e3a66ab557ff72ecd03fbd6a3d63f5f644881af23766d470f8f1bc16d341ca91b0a56499e720a0c"
    )
    assert data == "unBondTokens@01158e460913d00000"


def test_clean_registration_data(capsys: Any):
    return_code = main(
        [
            "validator",
            "clean-registered-data",
            "--pem",
            str(alice_pem),
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5078500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "0f12db6fe5e02c06f7fd28e8d4fd91ca9b728e49da71053bb02581c946aecc9fea5c6b1a54b386a249c927ec89c61bc5210095dd6a60853b53de3246c3fa7504"
    )
    assert data == "cleanRegisteredData"


def test_re_stake_unstaked_nodes(capsys: Any):
    return_code = main(
        [
            "validator",
            "restake-unstaked-nodes",
            "--pem",
            str(alice_pem),
            "--nodes-public-keys",
            bls_key,
            "--chain",
            "localnet",
            "--nonce=7",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert tx["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqplllsphc9lf"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5369500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "c40832505eae036a148543d398c4a92bda692172d7f0e6e84c505b84968506394e8d30b63ac0c84dbb2610be50c3b03a3619884d7e55c3ced9438bc0e1034407"
    )
    assert (
        data
        == "reStakeUnStakedNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208"
    )


def get_output(capsys: Any):
    tx = _read_stdout(capsys)
    return json.loads(tx)


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout
