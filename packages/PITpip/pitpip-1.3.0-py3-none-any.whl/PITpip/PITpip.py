# package-import-test-pip.py

def greet(name):
    """Greet the user."""
    return f"Hello, {name} everything changed when the version changed!"

if __name__ == "__main__":
    print(greet("World"))