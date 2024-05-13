import typing
from typing import Any

import pastperfect

from profitpulse.data.data import View
from profitpulse.services.import_transactions import EXPENSE_MADE


class ExpensesView(View):
    def __init__(self, session: typing.Any, seller: typing.Optional[str] = None):
        self._session = session
        self._seller = seller

    @property
    def data(self) -> Any:
        events = pastperfect.Events(self._session)
        if not len(events):
            return []

        results = []
        for event in events:
            if event.name != EXPENSE_MADE:
                continue

            description = event.data.get("description")

            if self._seller and self._seller not in description:
                continue

            results.append(
                [
                    event.data.get("value"),
                    description,
                    event.data.get("date_of"),
                ]
            )

        return results
