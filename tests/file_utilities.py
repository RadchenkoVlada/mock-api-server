from typing import List, Tuple, Any, Callable
import pytest, csv
from decimal import Decimal


def _get_type_from_str(data: str) -> Callable:
    """
    Helper function transforming string representation of the type (can be read from file) to Python class
    :param data: string representation of the type from file
    :return: Python class representing this type
    """
    if data == "str":
        return str
    elif data == "int":
        return int
    elif data == "Decimal":
        return Decimal
    elif data == "float":
        return float

@pytest.fixture
def read_csv_file(request) -> List[Tuple[Any]]:
    """
    The fixture for CSV file reading and processing. Takes one indirect parameter - file path.
    :return list of tuples with the content of CSV file
    """
    filepath = request.param
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header_with_types = reader.__next__()
        types = [_get_type_from_str(t) for t in header_with_types]
        data = []
        for row in reader:
            data.append(tuple(t(el) for t,el in zip(types, row)))
    return data
