from celery import Celery

app = Celery("test", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

@app.task
def add(x, y):
    return x + y