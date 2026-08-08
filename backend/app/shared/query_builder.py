class QueryBuilder:

    def __init__(self, stmt):
        self.stmt = stmt

    def where(self, condition):
        self.stmt = self.stmt.where(condition)
        return self

    def order_by(self, *columns):
        self.stmt = self.stmt.order_by(*columns)
        return self

    def limit(self, limit: int):
        self.stmt = self.stmt.limit(limit)
        return self

    def offset(self, offset: int):
        self.stmt = self.stmt.offset(offset)
        return self

    def where_if(self, condition, predicate):
        if condition:
            self.stmt = self.stmt.where(predicate)
        return self

    def order_by_if(
        self,
        condition,
        asc_column,
        desc_column,
    ):
        if condition:
            self.stmt = self.stmt.order_by(asc_column)
        else:
            self.stmt = self.stmt.order_by(desc_column)
        return self

    def build(self):
        return self.stmt