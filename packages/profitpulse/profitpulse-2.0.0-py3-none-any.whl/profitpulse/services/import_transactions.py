import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.transaction import Transaction
from profitpulse.services.deposit_into_asset import AssetNotFoundError
from profitpulse.services.services import EventEmitterMixin, EventLogger


class ImportTransactionsTransactionGater(abc.ABC):
    def __iter__(self) -> None:
        pass  # pragma: no cover


class ImportTransactionsTransactionCollector(abc.ABC):
    @abc.abstractmethod
    def append(self, transaction: Transaction, asset_name: AssetName) -> None:
        pass  # pragma: no cover


class ImportTransactionsRequester(abc.ABC):
    @property
    @abc.abstractmethod
    def asset_name(self) -> AssetName: ...  # pragma: no cover


class ImportTransactionsAssetCollector(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, asset_name: AssetName) -> Asset: ...  # pragma: no cover


TRANSACTION_IMPORTED = "transaction_imported"


class ImportTransactionsService(EventEmitterMixin):
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: ImportTransactionsTransactionGater,
        transactions: ImportTransactionsTransactionCollector,
        assets: ImportTransactionsAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ) -> None:
        self.transactions = transactions_gateway
        self._transactions = transactions
        self._assets = assets

        super().__init__(TRANSACTION_IMPORTED, event_log)

    def execute(self, request: ImportTransactionsRequester) -> None:
        try:
            _ = self._assets[request.asset_name]
        except KeyError:
            raise AssetNotFoundError(request.asset_name)

        for transaction in self.transactions:  # type: ignore
            self._transactions.append(transaction, request.asset_name)

        # self.emit(
        #     name=str(asset.name),  # type: ignore
        #     balance=int(request.amount),  # type: ignore
        # )
