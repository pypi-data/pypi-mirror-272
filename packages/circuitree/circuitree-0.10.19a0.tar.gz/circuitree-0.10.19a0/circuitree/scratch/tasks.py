from app import app
from module import MyClass


@app.task
def run_addn(x, y):
    """Run the addn method of MyClass in a Celery task."""
    obj = MyClass(x)
    return obj.addn(y, 10)
