from typing import Any

# Define the decorator function
def NTSubscriber(table_name: str, path: str, default: Any):
    # This decorator returns an object that will be assigned to the variable
    def decorator():
        # Return an instance of a descriptor or custom class
        return NTSubscriberField(table_name, path, default)
    return decorator()

# Define the NTSubscriberField class, which can be a descriptor
class NTSubscriberField:
    def __init__(self, table_name: str, path: str, default: Any):
        self.table_name = table_name
        self.path = path
        self.default = default
        self.private_name = None  # Will be set in __set_name__

    def __set_name__(self, owner, name):
        # Set the private name to avoid naming conflicts
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Custom logic for getting the value
        # For example, fetch from a database or network table
        print(f"Getting value from {self.table_name}:{self.path} (default: {self.default})")
        return getattr(instance, self.private_name, self.default)

    def __set__(self, instance, value):
        # Custom logic for setting the value
        # For example, update a database or network table
        print(f"Setting value for {self.table_name}:{self.path} to {value}")
        setattr(instance, self.private_name, value)

# Example class using the NTSubscriber decorator
class MyClass:
    @NTSubscriber("mytable", "mypath", 3)
    myfield: int = 0

    @NTSubscriber("othertable", "otherpath", "default")
    another_field: str

    def __init__(self):
        self.myfield = 10
        self.another_field = "hello"

# Usage
if __name__ == "__main__":
    obj = MyClass()
    print(obj.myfield)           # Triggers NTSubscriberField.__get__
    obj.myfield = 20             # Triggers NTSubscriberField.__set__
    print(obj.another_field)     # Triggers NTSubscriberField.__get__
    obj.another_field = "world"  # Triggers NTSubscriberField.__set__
