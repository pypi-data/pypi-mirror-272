import typing

import pastperfect
from turbofan.database import text

from profitpulse.lib.asset_name import AssetName
from profitpulse.lib.transaction import Transaction
from profitpulse.services.import_transactions import (
    TRANSACTION_IMPORTED,
    ImportTransactionsTransactionCollector,
)


class Transactions(ImportTransactionsTransactionCollector):
    def __init__(self, session: typing.Any) -> None:
        self._session = session

    def append(self, t: Transaction, asset_name: AssetName) -> None:
        """
        Append a transaction to the repository.
        """

        # Get the asset id by asset name
        sql_statement = """
            SELECT id
              FROM account
             WHERE name = :name
        """
        prepared_statement = text(sql_statement).bindparams(name=str(asset_name))
        result = self._session.execute(prepared_statement)
        asset_id = result.fetchone()[0]

        # Insert the transaction
        sql_statement = """
            INSERT INTO balance (date_of_movement, description, value, origin, account_id)
                 VALUES (:date_of_movement, :description, :value, :origin, :asset_id)
        """
        prepared_statement = text(sql_statement).bindparams(
            date_of_movement=str(t.date_of_movement),
            description=t.description,
            value=t.value,
            origin=t.origin,
            asset_id=asset_id,
        )
        self._session.execute(prepared_statement)

        events = pastperfect.Events(self._session)
        events.append(
            pastperfect.Event(
                name=TRANSACTION_IMPORTED,
                data={
                    "value": int(str(t.value).replace(".", "")),
                    "date": str(
                        t.date_of_movement.date()
                    ),  # TODO: should not need date()
                    "description": t.description,
                },
            )
        )
