import unittest
from unittest.mock import MagicMock

from simulator.models import TransactionMaker, User


class TestUser(unittest.TestCase):

    def test_add_transaction_should_add_transaction_to_user_transaction_list(self):
        user = User("me")
        t1, t2, t3 = [TransactionMaker.make("A", "B") for _ in range(3)]

        user.add_transaction(t1)
        user.add_transaction(t2)
        user.add_transaction(t3)

        self.assertEqual(len(user.get_transactions()), 3)

    def test_control_should_check_target(self):
        user = User("A")
        other = User("B")
        other.get_transactions = MagicMock()

        user.control_user(other)

        other.get_transactions.assert_called()

    def test_control_should_detect_missing_common_transaction(self):
        user = User("A")
        other = User("B")
        t0, t1, t2 = [TransactionMaker.make("A", "B", "t{}".format(i)) for i in range(3)]

        user.add_transaction(t0)
        user.add_transaction(t1)
        user.add_transaction(t2)
        other.add_transaction(t0)
        other.add_transaction(t2)

        with self.assertRaises(ValueError) as error:
            user.control_user(other)
        self.assertTrue("t1" in str(error.exception), "\"{}\" does not contain \"t1\"".format(error.exception))

    def test_remove_last_transaction_should_remove_it(self):
        user = User("A")
        t1 = TransactionMaker.make("A", "B")

        user.add_transaction(t1)
        user.remove_last_transaction()

        self.assertEqual(len(user.get_transactions()), 0)


class TestTransactionMaker(unittest.TestCase):
    def test_init_create_unique_id(self):
        t1 = TransactionMaker.make("A", "B")
        t2 = TransactionMaker.make("A", "B")

        self.assertNotEqual(t1, t2)
