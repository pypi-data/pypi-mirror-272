# type: ignore
import pytest

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.services.deposit_into_asset import AssetNotFoundError
from profitpulse.services.import_transactions import ImportTransactionsService


class AssetsStub:
    def __getitem__(self, asset_name: AssetName) -> Asset:
        return Asset(asset_name)


class RequestStub:
    @property
    def asset_name(self) -> AssetName:
        return AssetName("TheAssetName")


def test_append_zero_transactions_when_no_transactions_to_append() -> None:
    request = RequestStub()
    assets = AssetsStub()
    source_transactions = []
    transactions = []
    service = ImportTransactionsService(source_transactions, transactions, assets, [])

    service.execute(request)

    assert len(transactions) == 0  # nosec


class TransactionsStub:
    def __init__(self) -> None:
        self._transactions = []  # type: ignore

    def append(self, transaction, asset_name: AssetName):
        self._transactions.append(transaction)

    def __len__(self):
        return len(self._transactions)


def test_append_one_transaction_when_one_transaction_available_in_source():
    request = RequestStub()
    assets = AssetsStub()
    source_transactions = [{}]
    transactions = TransactionsStub()
    service = ImportTransactionsService(source_transactions, transactions, assets, [])

    service.execute(request)

    assert len(transactions) == 1  # nosec


class AssetNotFounStub:
    def __getitem__(self, _):
        raise KeyError


def test_raise_error_if_asset_not_found() -> None:
    request = RequestStub()
    assets = AssetNotFounStub()
    transactions = []
    source_transactions = [{}]
    service = ImportTransactionsService(source_transactions, transactions, assets, [])
    with pytest.raises(
        AssetNotFoundError,
        match="Could not find an asset with name 'TheAssetName'",
    ):
        service.execute(request)
