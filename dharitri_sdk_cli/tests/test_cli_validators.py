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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 11029500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "7629051f3e8ad2746eec1b4a95cc8ce5de69ee253125e209204b64e4cdb757e90e8034fc7fa3afd4b569c7f1f06db85076c9a63a8545e4d96d4e3c1aabd0df07"
    )
    assert (
        data
        == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
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
            "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf",
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 5057500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "39064a3e23fbee980202024c98dfdaba272693cc1030f6cb3568c8ebe7a526d857b4099cf7784324b51c4ad8f0b92621cdb2c32e631040500e43a878bf989a0d"
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
            "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2",
            "--guardian",
            "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct",
            "--guardian-pem",
            str(guardian),
        ]
    )
    assert return_code == 0

    output = get_output(capsys)
    tx = output["emittedTransaction"]
    data = output["emittedTransactionData"]

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 0
    assert tx["gasLimit"] == 11129500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 2
    assert tx["guardian"] == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
    assert tx["relayer"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
    assert (
        tx["signature"]
        == "3650a0391395674a8edd5743027e4d74449c23e5da23a1b7cc23a4a24b08717f1cb8e28693e8ab086a04929cdf815226e55a02ab63d100bcf229f0202b9adc0e"
    )
    assert (
        tx["guardianSignature"]
        == "761f50cbf106bf705e8167d069c68c5fab3acbe4529f7421fd1e30f74d914723e13aafbae49b61a90cf96e853b659648f13b67e0d39df045500fe63781be3709"
    )
    assert (
        data
        == "stake@02@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1865870f7f69162a2dfefd33fe232a9ca984c6f22d1ee3f6a5b34a8eb8c9f7319001f29d5a2eed85c1500aca19fa4189@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@12b309791213aac8ad9f34f0d912261e30f9ab060859e4d515e020a98b91d82a7cd334e4b504bb93d6b75347cccd6318@b2a11555ce521e4944e09ab17549d85b487dcd26c84b5017a39e31a3670889ba"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "2711000000000000000000"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5057500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "7f4a40781e7e040f657b82152bded1894c9cac2b868f0bd41b6639242410cf2a013c2104fba99aaa73063ace8a01739ffc7509dfdb9c1ea20832a089418af606"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5350000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "38a6291f43d92554394ed926e7500524f7b2a29dede552dfd91b0ff0a3313168854e6aa0f7d767cb53c62c92f51f4f5ea727ceb308fd74340a900ea84f868d07"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5348500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "431d6a532e5d2b2a91de662aad151db0f96fac5425a225f0393d3f409bd1e624ef5cf5e79fce844d9a93a3d836a66088a66d032e16380f18864b4fc19ef05503"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "2500000000000000000000"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5348500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "15458f5db3360251a966286fba7160ec17d88d7fc4f6fe0f9deda658e969f9ba49fef969526157e8750846aa2876b07d3b507ad6e9a0c9ab7655aa22fd413a0d"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5176000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "5d82d90873806855a965bd9b61e11854ef2e8323b17539f3f42a071a44ebdb7b2e34c57d261a02c9fa78feb5ba21bf90dd7bede91a72e0f7a7c8fd38e08f1603"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5057500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "7dbc547aab6fbdc4c0f7620c06cf44d2a00d6012e2a1db2e4edec1fa0f523679571d78eb957b4a9b68853af06c5121df26588a9046e11c00a846d0f1e93a2c07"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5357500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "a27e60730ce7d1199fe7236a3db3c75d238f43d364ad4cd5de9fa1607004c7aa470637f85be1fd09bf43edd78d869ba4f2f121740509b8e93f329f7c0cb2cf07"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5095000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "d0aac76e130a235cfc78028c11ba81c71840d54028cdd6bfa44272e2bc3f8fe65e4404489a50cdf37bc4b04a150cc8586d096224a829ef15a97df04b67b33f09"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5356000
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "d0bef0ca2e18ef2eb5333733be459f65c4b1726372c11f0ccfab18767d68fcf5af4a440d03641729c58ed4a69e17a8921ed38567fe81464f0c1f98f8587b1e00"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5096500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "52b910c987349bda999573067563f43ac323de241e20a228a8dcc129d17f5604d87bbb30fb2ef4233dd64e2c54d76e22d1c209cad4af92e40b73c29d0b51f002"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5078500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "f2791ca4edb918807cacc08c05e7103fd936b2402b3d0c2cf7f219946b8067ebce5a685908a2cac466f1bccb73b4ec8470b421119826584d41684a4971b2eb01"
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

    assert tx["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert tx["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqplllskzf8kp"
    assert tx["value"] == "0"
    assert tx["nonce"] == 7
    assert tx["gasLimit"] == 5369500
    assert tx["chainID"] == "localnet"
    assert tx["version"] == 2
    assert tx["options"] == 0
    assert (
        tx["signature"]
        == "e4420a51bf3ac6762943d15da9a6e14961d53ca96c61b1b1ab333d1298ea0f5eb0c7f50f832d3d34076f91030155d73f856bfd95c5ff3f35bd6962f31a4cc60b"
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
