import typing
from datetime import datetime
from typing import Any

import pastperfect
from turbofan.database import text

from profitpulse.data import assets as assets_repository
from profitpulse.data.data import View
from profitpulse.lib.money import Money
from profitpulse.services.deposit_into_asset import ASSET_DEPOSITED
from profitpulse.services.import_transactions import TRANSACTION_IMPORTED
from profitpulse.services.revalue_asset import ASSET_REVALUED


class AssetsView(View):
    def __init__(self, session: typing.Any) -> None:
        self._session = session

    @property
    def data(self) -> Any:
        sql_stmt = """
          SELECT account.name as name,
                 account.status,
                 balance.description
            FROM account
       LEFT JOIN balance
              ON account.id = balance.account_id
        """
        rows = self._session.execute(text(sql_stmt))
        assets = list(rows)
        events = pastperfect.Events(self._session)

        results = []
        for asset in assets:
            asset_name = asset[0]
            asset_details = [
                asset_name,
                "0.00",
                "Open" if asset[1] == assets_repository.ACTIVE else "Closed",
                asset[2] if asset[2] else "",
            ]
            total_balance = Money(0)
            for event in events:
                if (
                    event.name == ASSET_DEPOSITED or event.name == ASSET_REVALUED
                ) and event.data.get("name") == asset_name:
                    total_balance = total_balance + Money(event.data.get("balance"))

            asset_details[1] = str(total_balance)

            results.append(asset_details)

        return results


class TransactionsView(View):
    def __init__(
        self,
        session: typing.Any,
        seller: typing.Optional[str] = None,
        since: typing.Optional[datetime] = None,
        on: typing.Optional[datetime] = None,
    ) -> None:
        self._seller = seller.lower() if seller else None
        self._session = session
        self._since = since
        self._on = on

    @property
    def data(self) -> typing.Any:  # noqa
        """
        The data resulting from the view execution.
        """

        if not self._seller:
            events = pastperfect.Events(self._session)
            total_money = Money(0)
            transactions = []
            for event in events:
                if event.name != TRANSACTION_IMPORTED:
                    continue

                date_of_transaction = datetime.strptime(event.data["date"], "%Y-%m-%d")
                if self._since:
                    if date_of_transaction < self._since:
                        continue

                if self._on:
                    if date_of_transaction != self._on:
                        continue

                total_money = total_money + Money(event.data["value"])
                transactions.append(
                    {
                        "description": event.data["description"],
                        "value": str(Money(event.data["value"])),
                    }
                )

                # on="2020-01-01"

            return transactions, str(total_money)

        #  # Need something that reads a date in a string and loads it into a date
        #         # object and then allows to compare if it is > < or = than a date string
        #         d = datetime.strptime(str(t.date_of_movement), '%Y-%m-%d %H:%M:%S%z')
        #         _ = d

        # Construct the query
        sql_stmt = "SELECT description, value FROM balance"
        if self._since:
            sql_stmt += " WHERE date_of_movement >= :since"
        if self._on:
            sql_stmt += " WHERE date_of_movement = :on"

        # Bind parameters
        prepared_statement = text(sql_stmt)
        if self._since:
            prepared_statement = prepared_statement.bindparams(since=self._since)
        if self._on:
            prepared_statement = prepared_statement.bindparams(on=self._on)

        # Extract data
        rows = self._session.execute(prepared_statement)

        # Transform the data for output
        transactions = []
        for row in rows:
            transactions.append({"description": row[0], "value": row[1]})

        seller = self._seller
        total: float = 0.0

        for transaction in transactions:
            description = str(transaction["description"]).lower()
            value = float(transaction["value"])

            if not seller:
                total += value
                continue

            if seller and seller in description:
                total += value

        return transactions, total
