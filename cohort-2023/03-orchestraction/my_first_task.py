from prefect import task, flow

@task
def print_plus_one(obj): 
    print(f"Received a {type(obj)} with value {obj}")

    #shows the type of parameter aafter coercion
    print(obj + 1) #adds one

@flow
def validation_flow(x: int, y:int): 
    print_plus_one(x)
    print_plus_one(y)

if __name__ == "__main__":
    validation_flow(1, 2)
    