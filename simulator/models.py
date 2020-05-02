import itertools


class User:

    def __init__(self, id):
        self.id = id
        self.transactions = []

    def add_transaction(self, tx):
        self.transactions.append(tx)

    def control_user(self, target):
        target_tx = target.get_transactions()
        checkable_tx = [tx for tx in self.transactions if target.id in tx]

        for tx in checkable_tx:
            if tx not in target_tx:
                raise ValueError("{} not found".format(tx))

    def remove_last_transaction(self):
        if len(self.transactions) > 0:
            self.transactions.pop()

    def get_transactions(self):
        return self.transactions


class TransactionMaker:

    id_iterator = itertools.count()

    def make(sourceId, targetId, name="anonymous"):
        return "{}:{}:{}=>{}".format(next(TransactionMaker.id_iterator), name, sourceId, targetId)
