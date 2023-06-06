from prefect import flow, task

@task(name="print hello")
def print_hello(name):
    msg = f"Hello {name}"
    print(msg)
    return msg

@flow(name = "subflow")
def my_subflow(msg):
    print(f"Subflow says: {msg}")


@flow(name = "hello flow")
def hello_world(name = "world"):
    message = print_hello(name)
    my_subflow(message)

hello_world("maria camila")
