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
            receiver=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
            native_amount=0,
            gas_limit=50000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
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
            == "bed4103a8ce01d98891b9b98b601a2eeef9af0ce410147334e18a2ab84701ded6e9aec05b6e7918c898a34bca2f8445ae4a83811d0488ddab04b095cf9cefb05"
        )

    def test_create_transfer_transaction(self):
        guardian_relayer_data = GuardianRelayerData()
        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
            native_amount=123456789,
            gas_limit=50000,
            gas_price=1000000000,
            nonce=7,
            version=2,
            options=0,
            guardian_and_relayer_data=guardian_relayer_data,
        )

        assert transaction.sender == self.alice.address
        assert transaction.receiver.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
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
            == "e0fab6a3e8ed97def2876e5d5b09823945a3aba8b3f27819fac60a46a97004bc210e83dd9bc961c0588a617af40c65db968fec6deaf87cfe70a3707a47f4f300"
        )

    def test_create_transaction_with_data(self):
        guardian_relayer_data = GuardianRelayerData()
        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
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
        assert transaction.receiver.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
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
            == "9a684ad73780d1a73a693e9a0c46f395c952a8228e4c5415e4a40a625eba8b24a117413fcde8c14c14237779c023e110c61ec90b538844160f2fa26e87f29001"
        )

    def test_create_guarded_transaction(self):
        guardian_relayer_data = GuardianRelayerData(
            guardian=Account.new_from_pem(testdata / "testUser2.pem"),
            guardian_address=Address.new_from_bech32("drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"),
        )

        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
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
        assert transaction.receiver.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
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
            and transaction.guardian.to_bech32() == "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"
        )
        assert (
            transaction.guardian_signature.hex()
            == "10c34f854b9d76a765e821bfa13d13b97c31271ffc0c7e00e5c5b13c59209a65d1c9ae0b8c4b994e7465a4ee374cf39fce065a3a734c3da79238686417cef503"
        )
        assert (
            transaction.signature.hex()
            == "8b6b338b657fe5aca42b60533258b069641c828dfbe02859d543329afb06e6189e92545f20ab022158b2d19e97ad0e41e4cd8e96dd57bb9d9398657f796df009"
        )

    def test_create_relayed_transaction(self):
        guardian_relayer_data = GuardianRelayerData(
            relayer=Account.new_from_pem(testdata / "testUser2.pem"),
            relayer_address=Address.new_from_bech32("drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"),
        )

        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
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
        assert transaction.receiver.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
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
            and transaction.relayer.to_bech32() == "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"
        )
        assert (
            transaction.relayer_signature.hex()
            == "81856dc88c361cf807d9bb125e17f9130ace351de969a3553a20c9f486fb30ca89b4c9aeb58ceecd18f49c6d9629ea1045cf2da9f1cc8095dffa6d6a2b5c7f0b"
        )
        assert (
            transaction.signature.hex()
            == "fea0b4a89697951e6f6c80045e6d18671aeb30ef4fd884223e7a37095afad9de5f9d84c679b3b78a8078b5a7f9dabf876e30c9b2bb1d9949b702f403518c8a0a"
        )

    def test_create_guarded_relayed_transaction(self):
        guardian_relayer_data = GuardianRelayerData(
            guardian=Account.new_from_pem(testdata / "testUser.pem"),
            guardian_address=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
            relayer=Account.new_from_pem(testdata / "testUser2.pem"),
            relayer_address=Address.new_from_bech32("drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"),
        )

        transaction = self.controller.create_transaction(
            sender=self.alice,
            receiver=Address.new_from_bech32("drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"),
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
        assert transaction.receiver.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
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
            and transaction.guardian.to_bech32() == "drt1kp072dwz0arfz8m5lzmlypgu2nme9l9q33aty0znualvanfvmy5qd3yy8q"
        )
        assert (
            transaction.guardian_signature.hex()
            == "e9a0750a8955f56faab12144925fc796796610f8aac600dd9ab8f2eae4b8212d8fb5f75b204079c0b8867df4506f91c099043a1cbd91126c6a95a1134e7c140b"
        )

        assert (
            transaction.relayer
            and transaction.relayer.to_bech32() == "drt1nrdn6f9e43a57dj0f2ra33r4e8wt5ueemdlu8hzpnkg7zqq4shlsq0cq3k"
        )
        assert (
            transaction.relayer_signature.hex()
            == "0e7112ce6ff067369d57db666d5eae2684549426f9b45208a72c8ae022e811264932fbf018e6823b2ab5e1b0cd832744de6f990d9c1a0f7b3c851f265b550c0e"
        )

        assert (
            transaction.signature.hex()
            == "257611d878a27f378c3f2b4bf723fe1f87ce670b623daa06afd2c888d2c3551504e07764172fad3b0c32495571ac7b7484c0a591ae2fd42428ca43ae4d68fc0c"
        )
