import typing
from typing import Any

import pastperfect

from profitpulse.data.data import View
from profitpulse.services.import_transactions import EXPENSE_MADE


class ExpensesView(View):
    def __init__(
        self,
        session: typing.Any,
        seller: typing.Optional[str] = None,
        group_seller: typing.Optional[bool] = False,
    ):
        self._session = session
        self._seller = seller
        self._group_seller = group_seller

    @property
    def data(self) -> Any:  # noqa
        events = pastperfect.Events(self._session)
        if not len(events):
            return []

        seller_value = {}
        results = []

        def get_expenses_by_seller(evt: pastperfect.Event):
            nonlocal seller_value

            if evt.name != EXPENSE_MADE:
                return

            d = evt.data.get("description")
            if self._seller and self._seller not in d:
                return

            try:
                seller_value[d] = seller_value[d] + evt.data.get("value")
            except KeyError:
                seller_value[d] = evt.data.get("value")

        def get_expenses(evt: pastperfect.Event):
            nonlocal results
            if evt.name != EXPENSE_MADE:
                return

            d = evt.data.get("description")

            if self._seller and self._seller not in d:
                return

            results.append(
                [
                    evt.data.get("value"),
                    d,
                    evt.data.get("date_of"),
                ]
            )

        handler = get_expenses
        if self._group_seller:
            handler = get_expenses_by_seller

        events.replay([handler])

        if self._group_seller:
            results = [[value, key] for key, value in seller_value.items()]

        return results
