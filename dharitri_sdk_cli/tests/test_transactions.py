from pathlib import Path

from dharitri_py_sdk import Account, Address

from dharitri_sdk_cli.guardian_relayer_data import GuardianRelayerData
from dharitri_sdk_cli.transactions import TransactionsController

testdata = Path(__file__).parent / "testdata"


class TestTransactionsController:
    controller = TransactionsController("D")
    alice = Account.new_from_pem(testdata / "alice.pem")

    def test_create_transaction_without_data_and_value(self):
        guardian_relayer_data = GuardianRelayerData()
        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            native_amount=0,
            gas_limit=50000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        assert transaction.value == 0
        assert transaction.chain_id == "D"
        assert transaction.gas_limit == 50000
        assert transaction.gas_price == 1000000000
        assert transaction.nonce == 7
        assert transaction.version == 2
        assert transaction.options == 0
        assert not transaction.data
        assert not transaction.guardian
        assert not transaction.relayer
        assert not transaction.guardian_signature
        assert not transaction.relayer_signature
        assert (
            transaction.signature.hex()
            == "b64f85307353db2856df846d2c00983a0ed355a37ab41f4c1f17e8eda35d450f73bab3ca61b4c9130b9fd39ce35f06e2c3a3d59097b8cb9485f4e3ef8e8f1b0c"
        )

    def test_create_transfer_transaction(self):
        guardian_relayer_data = GuardianRelayerData()
        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            native_amount=123456789,
            gas_limit=50000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        assert transaction.value == 123456789
        assert transaction.chain_id == "D"
        assert transaction.gas_limit == 50000
        assert transaction.gas_price == 1000000000
        assert transaction.nonce == 7
        assert transaction.version == 2
        assert transaction.options == 0
        assert not transaction.data
        assert not transaction.guardian
        assert not transaction.relayer
        assert not transaction.guardian_signature
        assert not transaction.relayer_signature
        assert (
            transaction.signature.hex()
            == "0daab8c817331cd743d6c235b163d1ad69daa13b31fcd763b1b29bbcf9b20618a909bc04aed0957721a918ebd4990fb548007df15942475726ff3f6461209907"
        )

    def test_create_transaction_with_data(self):
        guardian_relayer_data = GuardianRelayerData()
        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            native_amount=0,
            gas_limit=50000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            data="testdata",
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        assert transaction.value == 0
        assert transaction.chain_id == "D"
        assert transaction.gas_limit == 50000
        assert transaction.gas_price == 1000000000
        assert transaction.nonce == 7
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data == b"testdata"
        assert not transaction.guardian
        assert not transaction.relayer
        assert not transaction.guardian_signature
        assert not transaction.relayer_signature
        assert (
            transaction.signature.hex()
            == "6545c44f7f20d49aa7eb7637e334dd8b44251ad94aa657e6fefae477c3c2094367e74bfa188d17ddf59a806d2d1b5364b556f47f71497bef16e0768ca9196c0b"
        )

    def test_create_guarded_transaction(self):
        guardian_relayer_data = GuardianRelayerData(
            guardian=Account.new_from_pem(testdata / "testUser2.pem"),
            guardian_address=Address.new_from_bech32("drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"),
        )

        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            native_amount=0,
            gas_limit=200000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            data="testdata",
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        assert transaction.value == 0
        assert transaction.chain_id == "D"
        assert transaction.gas_limit == 200000
        assert transaction.gas_price == 1000000000
        assert transaction.nonce == 7
        assert transaction.version == 2
        assert transaction.options == 2
        assert transaction.data == b"testdata"
        assert not transaction.relayer
        assert not transaction.relayer_signature
        assert (
            transaction.guardian
            and transaction.guardian.to_bech32() == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
        )
        assert (
            transaction.guardian_signature.hex()
            == "0df4196b1c8f32ec2f1e6113e385e9ca09826ebb41ad5680362b8db3f4636bae83c406f760866faa5f06c6ef606b82464b02d652978519fbc19a30725ae66102"
        )
        assert (
            transaction.signature.hex()
            == "a2f2a164362c894988aff95e3000924ed02e7a9ab02a4ae13235142c91090c572999ae761ff0eb646b78c4c3b90645e5f83775d6783a9e6de74d11713ad6b405"
        )

    def test_create_relayed_transaction(self):
        guardian_relayer_data = GuardianRelayerData(
            relayer=Account.new_from_pem(testdata / "testUser2.pem"),
            relayer_address=Address.new_from_bech32("drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"),
        )

        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            native_amount=0,
            gas_limit=200000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            data="testdata",
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        assert transaction.value == 0
        assert transaction.chain_id == "D"
        assert transaction.gas_limit == 200000
        assert transaction.gas_price == 1000000000
        assert transaction.nonce == 7
        assert transaction.version == 2
        assert transaction.options == 0
        assert transaction.data == b"testdata"
        assert not transaction.guardian
        assert not transaction.guardian_signature
        assert (
            transaction.relayer
            and transaction.relayer.to_bech32() == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
        )
        assert (
            transaction.relayer_signature.hex()
            == "43dd3c6bdfcb7b6f9ab8b93c192add80362dfe6ef47f568878794e2b0efa46eb97d5b54e410a32c781e239e0734c3b51a60a80acaf8d810563ab26aa88a33609"
        )
        assert (
            transaction.signature.hex()
            == "ea896758e32de6e828d44cafbf158845c5a0fb04a82ada354a05caf49ebc3b9a6edf278bc0d6256510618e7e87510f1d206ab37e386af81e894351b4b4665f0a"
        )

    def test_create_guarded_relayed_transaction(self):
        guardian_relayer_data = GuardianRelayerData(
            guardian=Account.new_from_pem(testdata / "testUser.pem"),
            guardian_address=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            relayer=Account.new_from_pem(testdata / "testUser2.pem"),
            relayer_address=Address.new_from_bech32("drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"),
        )

        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"),
            native_amount=0,
            gas_limit=200000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            data="testdata",
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        assert transaction.value == 0
        assert transaction.chain_id == "D"
        assert transaction.gas_limit == 200000
        assert transaction.gas_price == 1000000000
        assert transaction.nonce == 7
        assert transaction.version == 2
        assert transaction.options == 2
        assert transaction.data == b"testdata"

        assert (
            transaction.guardian
            and transaction.guardian.to_bech32() == "drt1cqqxak4wun7508e0yj9ng843r6hv4mzd0hhpjpsejkpn9wa9yq8s0ztfl2"
        )
        assert (
            transaction.guardian_signature.hex()
            == "eebe78dd79f78fdb16219c0ff4826a2d8a9c0dba9a164b0b6ace478fe24220bd17738a38b2868e44aa6305a4d030fe4bf48bb35b2d0997323cd630eaed4b810f"
        )

        assert (
            transaction.relayer
            and transaction.relayer.to_bech32() == "drt1ssmsc9022udc8pdw7wk3hxw74jr900xg28vwpz3z60gep66fasaszky4ct"
        )
        assert (
            transaction.relayer_signature.hex()
            == "be9f203a0598008ccd38fdfbca2e3a2f4292bacd545f89f5fbd99813eed1e5d2da643cf73585a7cc44a19d934937e7349d9427b1c3a8392339514a4eefc9b40c"
        )

        assert (
            transaction.signature.hex()
            == "e45eeff5f56bc75b9528538a87156fd51d9bb05234483e9ad2aa17afc5e985ad42aac49e905281d76e224171dcf628e4f4381351418e245a1723a764795b6401"
        )
