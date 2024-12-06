import psycopg2, pytest
from dotenv import dotenv_values
from tests.file_utilities import read_csv_file

ENV_FILENAME = "database.env"

@pytest.fixture(scope="module")
def db_config():
    """
    Simple fixture for env file reading.
    :return: dict with env variables and their values
    """
    return dotenv_values(ENV_FILENAME)

@pytest.fixture(scope="module")
def connection(db_config):
    """
    Fixture for connection to database.
    Tries to connect on module startup and close the connection after all tests.
    :return: psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(f"dbname={db_config['POSTGRES_DB']} user={db_config['POSTGRES_USER']} password={db_config['POSTGRES_PASSWORD']} host=mock-db-server port=5432")
    except psycopg2.Error as e:
        pytest.fail(f"Failed to establish a connection to database. Please, make sure that mock-db-server is up and configuration in {ENV_FILENAME} is correct. Error:{e}")

    yield conn
    conn.close()

@pytest.fixture()
def execute_query(connection, request):
    try:
        cur = connection.cursor()
        cur.execute(request.param)
    except psycopg2.Error as e:
        pytest.fail(f"Failed to create a cursor with query: \"{request.param}\" a connection to database. Error:{e}")

    yield cur
    cur.close()

TEST_DATA = (
("""SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 10;
""", "tests/test_data/q1.csv"),

("""SELECT employee_id, SUM(freight)
FROM orders
GROUP BY employee_id
ORDER BY employee_id;
""", "tests/test_data/q2.csv"),

("""
SELECT city,
   AVG(EXTRACT(year from AGE(birth_date))),
   MAX(EXTRACT(year from AGE(birth_date))),
   MIN(EXTRACT(year from AGE(birth_date)))
FROM employees
WHERE city = 'London'
GROUP BY city;
""", "tests/test_data/q3.csv"),

("""SELECT city, AVG(EXTRACT(year from AGE(birth_date))) AS avg_age
  FROM employees
  GROUP BY city
  HAVING AVG(EXTRACT(year from AGE(birth_date))) > 60;
""", "tests/test_data/q4.csv"),

("""SELECT first_name, last_name, EXTRACT(year from AGE(birth_date)) AS age
 FROM employees
 ORDER BY age DESC
 LIMIT 3;
""", "tests/test_data/q5.csv")
)

@pytest.mark.parametrize("execute_query, read_csv_file", TEST_DATA, indirect=True)
def test_first_row_of_sql_queries(execute_query, read_csv_file):
    sql_query_result = [e for e in execute_query]
    assert sql_query_result == read_csv_file
