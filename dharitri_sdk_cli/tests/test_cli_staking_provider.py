import json
from pathlib import Path
from typing import Any

from dharitri_sdk_cli.cli import main

parent = Path(__file__).parent
alice = parent / "testdata" / "alice.pem"

first_bls_key = "f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d"
second_bls_key = "1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
validators_file = parent / "testdata" / "validators_file.pem"


def test_create_new_delegation_contract(capsys: Any):
    main(
        [
            "staking-provider",
            "create-new-delegation-contract",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--value",
            "1250000000000000000000",
            "--total-delegation-cap",
            "10000000000000000000000",
            "--service-fee",
            "100",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "createNewDelegationContract@021e19e0c9bab2400000@64"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqyllls4jxmwv"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60126500
    assert transaction["value"] == "1250000000000000000000"
    assert (
        transaction["signature"]
        == "b577f6556330fca56d69abb15c31aab62aabbf0e651fe2a3a0400c0175a1f7f7d4d4469d46c362db54e782f91fc982d269826ae80227766a2db4012bdcd0ec03"
    )


def test_create_new_delegation_contract_with_provided_gas_limit(capsys: Any):
    main(
        [
            "staking-provider",
            "create-new-delegation-contract",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--value",
            "1250000000000000000000",
            "--total-delegation-cap",
            "10000000000000000000000",
            "--service-fee",
            "100",
            "--chain",
            "T",
            "--gas-limit",
            "60126501",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "createNewDelegationContract@021e19e0c9bab2400000@64"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqyllls4jxmwv"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60126501
    assert transaction["value"] == "1250000000000000000000"
    assert (
        transaction["signature"]
        == "da0bfa5a04308be1a149d516403a0d088ea244f844e4270c1380bc54fc4e9c8afaa6528ace88e2de974afbab1c8564233ad018cac5c3eeb875cdcee793119301"
    )


def test_add_nodes(capsys: Any):
    validators_file = parent / "testdata" / "validators.pem"

    main(
        [
            "staking-provider",
            "add-nodes",
            "--validators-pem",
            str(validators_file),
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "addNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@4dd9ac4250060e1adb1a7f8beb4ad8a53a8e08ae04c00d228a2b6de364b7ea1c07390d84865a0cd5d9145f2ddd6cb809@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@90c52a1a11b058a95998c4761668283659c76e5c56ebf7937f8c14be0126f52ae566c3838570e5bba6bbbcddc60c8699@e5dc552b4b170cdec4405ff8f9af20313bf0e2756d06c35877b6fbcfa6b354a7b3e2d439ea87999befb09a8fa1b3f014e57ec747bf738c4199338fcd4a87b373dd62f5c8329f1f5f245956bbb06685596a2e83dc38befa63e4a2b5c4ce408506@e299c68b056e4ebc7a39ae50e2091e1ccd63ca11a2429e26dac1901396f4a338c34dbd87b20d1ec8f67e4af18a7a790d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 20367000
    assert (
        transaction["signature"]
        == "e118368321df98abfa93349b419b56dd1b155434d9a978edfa5369f3270feab6371bfdd363f75d7fa68fe7c05e546d59605f39ed633d0399d19adb6a38dc770e"
    )


def test_add_nodes_with_gas_limit(capsys: Any):
    validators_file = parent / "testdata" / "validators.pem"

    main(
        [
            "staking-provider",
            "add-nodes",
            "--validators-pem",
            str(validators_file),
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
            "--gas-limit",
            "20367001",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "addNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@4dd9ac4250060e1adb1a7f8beb4ad8a53a8e08ae04c00d228a2b6de364b7ea1c07390d84865a0cd5d9145f2ddd6cb809@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d@90c52a1a11b058a95998c4761668283659c76e5c56ebf7937f8c14be0126f52ae566c3838570e5bba6bbbcddc60c8699@e5dc552b4b170cdec4405ff8f9af20313bf0e2756d06c35877b6fbcfa6b354a7b3e2d439ea87999befb09a8fa1b3f014e57ec747bf738c4199338fcd4a87b373dd62f5c8329f1f5f245956bbb06685596a2e83dc38befa63e4a2b5c4ce408506@e299c68b056e4ebc7a39ae50e2091e1ccd63ca11a2429e26dac1901396f4a338c34dbd87b20d1ec8f67e4af18a7a790d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 20367001
    assert (
        transaction["signature"]
        == "06768601c172b9600861b210f40263d9ccc7e17ad2e1b25603cfe2dbffbe9119ad927459dae08a6167f487a44353202b248147c69909a181c39ee700d301b60e"
    )


def test_remove_nodes_with_bls_keys(capsys: Any):
    main(
        [
            "staking-provider",
            "remove-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "removeNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 13645500


def test_remove_nodes_with_validators_file(capsys: Any):
    main(
        [
            "staking-provider",
            "remove-nodes",
            "--validators-pem",
            str(validators_file),
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "removeNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 13645500


def test_stake_nodes_with_bls_keys(capsys: Any):
    main(
        [
            "staking-provider",
            "stake-nodes",
            "--validators-pem",
            str(validators_file),
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "stakeNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 18644000


def test_stake_nodes_with_validators_file(capsys: Any):
    main(
        [
            "staking-provider",
            "stake-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "stakeNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 18644000


def test_unbond_nodes(capsys: Any):
    main(
        [
            "staking-provider",
            "unbond-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "unBondNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 18645500


def test_unstake_nodes(capsys: Any):
    main(
        [
            "staking-provider",
            "unstake-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "unStakeNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 18647000


def test_unjail_nodes(capsys: Any):
    main(
        [
            "staking-provider",
            "unjail-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--value",
            "5000000000000000000",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert (
        data
        == "unJailNodes@f8910e47cf9464777c912e6390758bb39715fffcb861b184017920e4a807b42553f2f21e7f3914b81bcf58b66a72ab16d97013ae1cff807cefc977ef8cbf116258534b9e46d19528042d16ef8374404a89b184e0a4ee18c77c49e454d04eae8d@1b4e60e6d100cdf234d3427494dac55fbac49856cadc86bcb13a01b9bb05a0d9143e86c186c948e7ae9e52427c9523102efe9019a2a9c06db02993f2e3e6756576ae5a3ec7c235d548bc79de1a6990e1120ae435cb48f7fc436c9f9098b92a0d"
    )
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 13645500
    assert transaction["value"] == "5000000000000000000"


def test_change_service_fee(capsys: Any):
    main(
        [
            "staking-provider",
            "change-service-fee",
            "--service-fee",
            "100",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "changeServiceFee@64"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11078500


def test_modify_delegation_cap(capsys: Any):
    main(
        [
            "staking-provider",
            "modify-delegation-cap",
            "--delegation-cap",
            "10000000000000000000000",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--chain",
            "T",
            "--nonce",
            "7",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "modifyTotalDelegationCap@021e19e0c9bab2400000"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11117500


def test_automatic_activation(capsys: Any):
    main(
        [
            "staking-provider",
            "automatic-activation",
            "--set",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "setAutomaticActivation@74727565"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11096500

    # Clear the captured content
    capsys.readouterr()

    main(
        [
            "staking-provider",
            "automatic-activation",
            "--unset",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "setAutomaticActivation@66616c7365"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11099500


def test_redelegate_cap(capsys: Any):
    main(
        [
            "staking-provider",
            "redelegate-cap",
            "--set",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "setCheckCapOnReDelegateRewards@74727565"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11108500

    # Clear the captured content
    capsys.readouterr()

    main(
        [
            "staking-provider",
            "redelegate-cap",
            "--unset",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "setCheckCapOnReDelegateRewards@66616c7365"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11111500


def test_set_metadata(capsys: Any):
    main(
        [
            "staking-provider",
            "set-metadata",
            "--name",
            "Test",
            "--website",
            "www.test.com",
            "--identifier",
            "TEST",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "setMetaData@54657374@7777772e746573742e636f6d@54455354"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 11131000


def test_create_delegation_contract_from_validator(capsys: Any):
    main(
        [
            "staking-provider",
            "make-delegation-contract-from-validator",
            "--max-cap",
            "0",
            "--fee",
            "3745",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "makeNewContractFromValidatorData@@0ea1"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqqqyllls4jxmwv"
    assert transaction["gasLimit"] == 510000000


def test_delegate(capsys: Any):
    main(
        [
            "staking-provider",
            "delegate",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--value",
            "1000000000000000000",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "delegate"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 12000000


def test_claim_rewards(capsys: Any):
    main(
        [
            "staking-provider",
            "claim-rewards",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "claimRewards"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 6000000


def test_redelegate_rewards(capsys: Any):
    main(
        [
            "staking-provider",
            "redelegate-rewards",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "reDelegateRewards"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 12000000


def test_undelegate(capsys: Any):
    main(
        [
            "staking-provider",
            "undelegate",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--value",
            "1000000000000000000",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "unDelegate@0de0b6b3a7640000"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 12000000


def test_withdraw(capsys: Any):
    main(
        [
            "staking-provider",
            "withdraw",
            "--delegation-contract",
            "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp",
            "--pem",
            str(alice),
            "--nonce",
            "7",
            "--chain",
            "T",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "withdraw"
    assert transaction["sender"] == "drt1c7pyyq2yaq5k7atn9z6qn5qkxwlc6zwc4vg7uuxn9ssy7evfh5jq4nm79l"
    assert transaction["receiver"] == "drt1yvesqqqqqqqqqqqqqqqqqqqqqqqqyvesqqqqqqqqqqqqqthllllswa9mfp"
    assert transaction["gasLimit"] == 12000000


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout


def get_transaction(capsys: Any):
    output = _read_stdout(capsys)
    return json.loads(output)
