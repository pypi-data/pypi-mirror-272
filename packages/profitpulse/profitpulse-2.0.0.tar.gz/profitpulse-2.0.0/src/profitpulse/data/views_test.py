from datetime import datetime

import pastperfect
import pytest
from turbofan.database import text

from profitpulse.data.views import AssetsView, TransactionsView
from profitpulse.lib.money import Money
from profitpulse.services.import_transactions import TRANSACTION_IMPORTED


class TestAssetsView:
    @pytest.mark.integration
    def test_return_no_data_when_no_assets(self, tmp_db_session):
        assert AssetsView(tmp_db_session).data == []  # nosec

    @pytest.mark.integration
    def test_return_one_asset_when_one_asset_exists(self, tmp_db_session):
        DatabaseScenario(tmp_db_session).open_asset(name="TheAssetName")
        assert AssetsView(tmp_db_session).data == [  # nosec
            ["TheAssetName", str(Money(0)), "Closed", ""]
        ]


class DatabaseScenario:
    def __init__(self, session):
        self.session = session
        self.asset_id = None

    def log_transaction(self, description, value, date_of_movement, origin, asset_id):
        sql_statement = """
            INSERT INTO balance (description, value, date_of_movement, origin, account_id)
                 VALUES (:description, :value, :date_of_movement, :origin, :account_id)
        """

        prepared_statement = text(sql_statement).bindparams(
            description=description,
            value=value,
            date_of_movement=date_of_movement,
            origin=origin,
            account_id=asset_id,
        )

        self.session.execute(prepared_statement)

        events = pastperfect.Events(self.session)
        events.append(
            pastperfect.Event(
                name=TRANSACTION_IMPORTED,
                data={
                    "value": value,
                    "date": date_of_movement,
                    "description": description,
                },
            )
        )

        return self

    def open_asset(self, name):
        sql_statement = "INSERT INTO account (name)VALUES (:name)"
        prepared_statement = text(sql_statement).bindparams(name=name)
        result = self.session.execute(prepared_statement)
        self.asset_id = result.lastrowid
        return self


class TestTransactionsView:
    @pytest.mark.integration
    def test_shown_no_transactions_on_empty_database(self, tmp_db_session):
        transactions, total = TransactionsView(tmp_db_session).data

        assert not transactions  # nosec
        assert total == "0.00"  # nosec

    @pytest.mark.integration
    def test_show_one_transaction_when_one_is_available(self, tmp_db_session):
        """
        Given a database with one transaction
        When the view is executed
        Then the transaction is shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_asset("TheAssetName")
        scenario.log_transaction("foo", 1, "2020-01-01", "foo", scenario.asset_id)

        transactions, total = TransactionsView(tmp_db_session).data

        assert transactions == [{"description": "foo", "value": "0.01"}]  # nosec
        assert total == "0.01"  # nosec

    @pytest.mark.integration
    def test_show_multiple_transactions_when_more_than_one_is_available(
        self, tmp_db_session
    ):
        """
        Given a database with multiple transactions
        When the view is executed
        Then the transactions are shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_asset("TheAssetName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.asset_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-01",
            "foo",
            scenario.asset_id,
        )

        transactions, total = TransactionsView(tmp_db_session).data

        assert transactions == [  # nosec
            {"description": "foo", "value": "0.01"},
            {"description": "bar", "value": "0.02"},
        ]
        assert total == "0.03"  # nosec

    @pytest.mark.integration
    def test_show_transactions_since_a_given_date(self, tmp_db_session):
        """
        Given a database with multiple transactions
        When the view is executed with a since date
        Then the transactions since the given date are shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_asset("TheAssetName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.asset_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-02",
            "foo",
            scenario.asset_id,
        )

        transactions, total = TransactionsView(
            tmp_db_session, since=datetime.strptime("2020-01-02", "%Y-%m-%d")
        ).data

        assert transactions == [{"description": "bar", "value": "0.02"}]  # nosec
        assert total == "0.02"  # nosec

    @pytest.mark.integration
    def test_show_transactions_on_a_given_date(self, tmp_db_session):
        """
        Given a database with multiple transactions
        When the view is executed with a on date
        Then the transactions on the given date are shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_asset("TheAssetName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.asset_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-02",
            "foo",
            scenario.asset_id,
        )

        transactions, total = TransactionsView(
            tmp_db_session,
            on=datetime.strptime("2020-01-01", "%Y-%m-%d"),
        ).data

        assert transactions == [{"description": "foo", "value": "0.01"}]  # nosec
        assert total == "0.01"  # nosec

    @pytest.mark.integration
    def test_show_total_for_a_specific_seller(self, tmp_db_session):
        """
        Given a database with multiple transactions
        When the view is executed with a seller
        Then the total for the given seller is shown
        """

        scenario = DatabaseScenario(tmp_db_session)
        scenario.open_asset("TheAssetName")
        scenario = scenario.log_transaction(
            "foo",
            1,
            "2020-01-01",
            "foo",
            scenario.asset_id,
        )
        scenario.log_transaction(
            "bar",
            2,
            "2020-01-02",
            "foo",
            scenario.asset_id,
        )

        transactions, total = TransactionsView(tmp_db_session, seller="foo").data

        assert total == 1.0  # nosec
