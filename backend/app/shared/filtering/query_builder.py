class QueryBuilder:

    def __init__(self, stmt):
        self.stmt = stmt

    def where(self, condition):
        self.stmt = self.stmt.where(condition)
        return self

    def order_by(self, *columns):
        self.stmt = self.stmt.order_by(*columns)
        return self

    def build(self):
        return self.stmt