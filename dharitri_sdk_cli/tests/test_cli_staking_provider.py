import json
from pathlib import Path
from typing import Any

from dharitri_sdk_cli.cli import main

parent = Path(__file__).parent
alice = parent / "testdata" / "alice.pem"
guardian = parent / "testdata" / "testUser.pem"
relayer = parent / "testdata" / "testUser2.pem"

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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60126500
    assert transaction["value"] == "1250000000000000000000"
    assert transaction["options"] == 0
    assert transaction["version"] == 2
    assert (
        transaction["signature"]
        == "2724ef55b19cd8af895fbb3702d86eedc63c175c4765c1b826480dca6e65f97380d9c89a2ab7dfec52a66a24f43acb2b79460fbfeef0e4fd45351335b8412403"
    )


def test_create_new_delegation_contract_sign_by_hash(capsys: Any):
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
            "--options",
            "1",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "createNewDelegationContract@021e19e0c9bab2400000@64"
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60126500
    assert transaction["value"] == "1250000000000000000000"
    assert transaction["options"] == 1
    assert transaction["version"] == 2
    assert (
        transaction["signature"]
        == "d3a4d636bbe6d2e4d97af06af0b4b3093f8f22326cc5dada81996b0e51aca5c17da17f7489bbd0708e6187c7aa17d74421e755fdf6d3fd5c5691050531297006"
    )


def test_create_new_delegation_contract_with_guardian_and_relayer(capsys: Any):
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
            "--guardian-pem",
            str(guardian),
            "--relayer-pem",
            str(relayer),
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "createNewDelegationContract@021e19e0c9bab2400000@64"
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60226500
    assert transaction["value"] == "1250000000000000000000"
    assert transaction["options"] == 2
    assert transaction["version"] == 2
    assert transaction["guardian"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
    assert transaction["relayer"] == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
    assert (
        transaction["signature"]
        == "923790cfb4e01a4c7620e3bb73410a476e41f612eb55cdab74e1c4384ee6e6568d5ebedc99d42d43c13d551efd74f1ffd504260926ca6d684218be1f66359e0a"
    )


def test_create_new_delegation_contract_with_guardian_and_relayer_and_provided_version_and_options(capsys: Any):
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
            "--guardian-pem",
            str(guardian),
            "--relayer-pem",
            str(relayer),
            "--version",
            "7",
            "--options",
            "77",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "createNewDelegationContract@021e19e0c9bab2400000@64"
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60226500
    assert transaction["value"] == "1250000000000000000000"
    assert transaction["options"] == 77
    assert transaction["version"] == 7
    assert transaction["guardian"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
    assert transaction["relayer"] == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"


def test_create_new_delegation_contract_with_guardian_and_relayer_and_sign_by_hash(capsys: Any):
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
            "--guardian-pem",
            str(guardian),
            "--relayer-pem",
            str(relayer),
            "--options",
            "1",
        ]
    )
    tx = get_transaction(capsys)
    data = tx["emittedTransactionData"]
    transaction = tx["emittedTransaction"]

    assert data == "createNewDelegationContract@021e19e0c9bab2400000@64"
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60226500
    assert transaction["value"] == "1250000000000000000000"
    assert transaction["options"] == 1
    assert transaction["version"] == 2
    assert transaction["guardian"] == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
    assert transaction["relayer"] == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
    assert (
        transaction["signature"]
        == "ce0c0a6a70e8dc8e2dfe46b4aac81a466c71be28be4d067f3cd8140b9866ecfc340766cd981450eab4615df66fe6b93008a1b96670fdbc2253843645018ecb01"
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["chainID"] == "T"
    assert transaction["gasLimit"] == 60126501
    assert transaction["value"] == "1250000000000000000000"
    assert (
        transaction["signature"]
        == "ac8b6de84d320853ba64c8abd60ea244b56e5ef4337d464cc35d1da7a1c585ba2fc4ce7a6f3778841d709e0d730a27ed554ba39fb9f85bada2312fca70c8e80f"
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
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
        == "addNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208@307ef00b648eed52ce4e95f8155f2e65491addd49266254f7c32ff06622e335752a6a6ad2efeb2534ec0db6a431b4989@78689fd4b1e2e434d567fe01e61598a42717d83124308266bd09ccc15d2339dd318c019914b86ac29adbae5dd8a02d0307425e9bd85a296e94943708c72f8c670f0b7c50a890a5719088dbd9f1d062cad9acffa06df834106eebe1a4257ef00d@4c90003d4b535fe709b6583708ae276e29558c58d160ad6241c3063e590611a2e327f2b8299b4955179a85eab50b4587@7188b234a8bf834f2e6258012aa09a2ab93178ffab9c789480275f61fe02cd1b9a58ddc63b79a73abea9e2b7ac5cac0b0d4324eff50aca2f0ec946b9ae6797511fa3ce461b57e77129cba8ab3b51147695d4ce889cbe67905f6586b4e4f22491@1d6cf6b0a38fa5c10df6493eae0b14c5d119d9f7d3d3e790a047e4e7c09919f64f910971ceef380b49f70fc982d07d19"
    )
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 20367000
    assert (
        transaction["signature"]
        == "e8638b2389bd5f786aee41e5a635b6fbb66afbbb5de27e6c9196c0b7dc0138c9ae443ef330d6b07893c7bb32523570224c6a079f848c32cf3565567f588f6a09"
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
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
        == "addNodes@e7beaa95b3877f47348df4dd1cb578a4f7cabf7a20bfeefe5cdd263878ff132b765e04fef6f40c93512b666c47ed7719b8902f6c922c04247989b7137e837cc81a62e54712471c97a2ddab75aa9c2f58f813ed4c0fa722bde0ab718bff382208@307ef00b648eed52ce4e95f8155f2e65491addd49266254f7c32ff06622e335752a6a6ad2efeb2534ec0db6a431b4989@78689fd4b1e2e434d567fe01e61598a42717d83124308266bd09ccc15d2339dd318c019914b86ac29adbae5dd8a02d0307425e9bd85a296e94943708c72f8c670f0b7c50a890a5719088dbd9f1d062cad9acffa06df834106eebe1a4257ef00d@4c90003d4b535fe709b6583708ae276e29558c58d160ad6241c3063e590611a2e327f2b8299b4955179a85eab50b4587@7188b234a8bf834f2e6258012aa09a2ab93178ffab9c789480275f61fe02cd1b9a58ddc63b79a73abea9e2b7ac5cac0b0d4324eff50aca2f0ec946b9ae6797511fa3ce461b57e77129cba8ab3b51147695d4ce889cbe67905f6586b4e4f22491@1d6cf6b0a38fa5c10df6493eae0b14c5d119d9f7d3d3e790a047e4e7c09919f64f910971ceef380b49f70fc982d07d19"
    )
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 20367001
    assert (
        transaction["signature"]
        == "6770df37437a2dad18ce60fc33c753743345d96f56b0bd6095bdcb3b3ae66ecccc639e7bf4d4091636c2a93ac69bd8fd6a3f8b565a7d1db385362bd4d1d6aa05"
    )


def test_remove_nodes_with_bls_keys(capsys: Any):
    main(
        [
            "staking-provider",
            "remove-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 13645500


def test_remove_nodes_with_validators_file(capsys: Any):
    main(
        [
            "staking-provider",
            "remove-nodes",
            "--validators-pem",
            str(validators_file),
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 13645500


def test_stake_nodes_with_bls_keys(capsys: Any):
    main(
        [
            "staking-provider",
            "stake-nodes",
            "--validators-pem",
            str(validators_file),
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 18644000


def test_stake_nodes_with_validators_file(capsys: Any):
    main(
        [
            "staking-provider",
            "stake-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 18644000


def test_unbond_nodes(capsys: Any):
    main(
        [
            "staking-provider",
            "unbond-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 18645500


def test_unstake_nodes(capsys: Any):
    main(
        [
            "staking-provider",
            "unstake-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 18647000


def test_unjail_nodes(capsys: Any):
    main(
        [
            "staking-provider",
            "unjail-nodes",
            "--bls-keys",
            f"{first_bls_key},{second_bls_key}",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
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
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11078500


def test_modify_delegation_cap(capsys: Any):
    main(
        [
            "staking-provider",
            "modify-delegation-cap",
            "--delegation-cap",
            "10000000000000000000000",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11117500


def test_automatic_activation(capsys: Any):
    main(
        [
            "staking-provider",
            "automatic-activation",
            "--set",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11096500

    # Clear the captured content
    capsys.readouterr()

    main(
        [
            "staking-provider",
            "automatic-activation",
            "--unset",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11099500


def test_redelegate_cap(capsys: Any):
    main(
        [
            "staking-provider",
            "redelegate-cap",
            "--set",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11108500

    # Clear the captured content
    capsys.readouterr()

    main(
        [
            "staking-provider",
            "redelegate-cap",
            "--unset",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
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
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsz8he8y"
    assert transaction["gasLimit"] == 51107000


def test_delegate(capsys: Any):
    main(
        [
            "staking-provider",
            "delegate",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11062000


def test_claim_rewards(capsys: Any):
    main(
        [
            "staking-provider",
            "claim-rewards",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11068000


def test_redelegate_rewards(capsys: Any):
    main(
        [
            "staking-provider",
            "redelegate-rewards",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11075500


def test_undelegate(capsys: Any):
    main(
        [
            "staking-provider",
            "undelegate",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11090500


def test_withdraw(capsys: Any):
    main(
        [
            "staking-provider",
            "withdraw",
            "--delegation-contract",
            "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf",
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
    assert transaction["sender"] == "drt1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssey5egf"
    assert transaction["receiver"] == "drt1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqthllllseg5eqf"
    assert transaction["gasLimit"] == 11062000


def _read_stdout(capsys: Any) -> str:
    stdout: str = capsys.readouterr().out.strip()
    return stdout


def get_transaction(capsys: Any):
    output = _read_stdout(capsys)
    return json.loads(output)
