from gevent import monkey 

monkey.patch_all()

from app import add


class MyClass:
    def __init__(self, x):
        self.x = x

    def add(self, y):
        return add.delay(self.x, y).get()

    def addn(self, y, n):
        """Result of n * (x + y)."""
        return sum(self.add(y) for _ in range(n))
