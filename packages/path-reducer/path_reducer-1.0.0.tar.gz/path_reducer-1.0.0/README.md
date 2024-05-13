# path-reducer

path-reducer is a Python package that simplifies a list of directions by removing opposite directions that cancel each other out.

## Installation

Package is published on [PyPI](https://pypi.org/project/path-reducer/), you can install it using pip:

```
pip install path-reducer
```

## Usage

```python
from path_reducer import PathReducer

# Create a PathReducer instance
path_reducer = PathReducer()

# Example usage
directions = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]
optimized_directions = path_reducer.reduce_path(directions)
print(optimized_directions)  # Output: ["WEST"]
```

## Local development

Project is set up using Poetry, to run it locally follow these steps:

1. Clone this repository to your local machine:

    ```
    git clone https://github.com/augustinasn/path-reducer.git
    ```

2. Navigate to the project directory:

    ```
    cd path-reducer
    ```

3. Install Poetry (if you haven't already):

    ```
    pip install poetry
    ```

4. Use Poetry to install the project's dependencies:

    ```
    poetry install
    ```

5. Activate the Poetry virtual environment:

    ```
    poetry shell
    ```
   
6. Tests are included in the tests directory. You can run the tests using the following command:
    ```
    python test.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.