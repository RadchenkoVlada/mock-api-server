import pytest
import csv
from decimal import Decimal


def get_type_from_str(data):
    if data == "str":
        return str
    elif data == "int":
        return int
    elif data == "Decimal":
        return Decimal
    elif data == "float":
        return float

@pytest.fixture
def read_csv_file(request):
    """
    The fixture for CSV file reading and processing. Takes one indirect parameter - file path.
    :return list of tuples with the content of CSV file
    """
    filepath = request.param
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header_with_types = reader.__next__()
        types = [get_type_from_str(t) for t in header_with_types]
        data = []
        for row in reader:
            data.append(tuple(t(el) for t,el in zip(types, row)))
    return data
