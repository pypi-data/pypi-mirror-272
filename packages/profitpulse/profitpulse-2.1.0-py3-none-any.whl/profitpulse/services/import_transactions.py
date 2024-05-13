import abc
import typing

from profitpulse.lib.asset import Asset
from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.transaction import Transaction
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


EXPENSE_MADE = "expense_made"


class ImportTransactionsService(EventEmitterMixin):
    """
    Imports transactions from a source.
    """

    def __init__(
        self,
        transactions_gateway: ImportTransactionsTransactionGater,
        assets: ImportTransactionsAssetCollector,
        event_log: EventLogger,
        *_: typing.Any,
        **__: typing.Dict[typing.Any, typing.Any],
    ) -> None:
        self.transactions = transactions_gateway
        self._assets = assets

        super().__init__(EXPENSE_MADE, event_log)

    def execute(self) -> None:
        for transaction in self.transactions:  # type: ignore
            if transaction.value > 0:
                continue  # Ignore income

            self.emit(
                value=transaction.value,  # type: ignore
                date_of=str(transaction.date_of_movement),  # type: ignore
                description=transaction.description,  # type: ignore
            )
