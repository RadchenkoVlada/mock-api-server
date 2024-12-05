from collections import namedtuple
from decimal import Decimal
import psycopg2, pytest
from dotenv import dotenv_values

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
""", ('Côte de Blaye', 263.5)),

# TODO:
# ("""SELECT employee_id, SUM(freight)
#  FROM orders
#  GROUP BY employee_id;
# """, (8, 7487.8804)),

("""
SELECT city,
   AVG(EXTRACT(year from AGE(CURRENT_TIMESTAMP, birth_date))),
   MAX(EXTRACT(year from AGE(CURRENT_TIMESTAMP, birth_date))),
   MIN(EXTRACT(year from AGE(CURRENT_TIMESTAMP, birth_date)))
FROM employees
WHERE city = 'London'
GROUP BY city;
""", ('London', Decimal('63'), Decimal('69'), Decimal('58'))),

("""SELECT city, AVG(EXTRACT(year from AGE(CURRENT_TIMESTAMP, birth_date))) AS avg_age
  FROM employees
  GROUP BY city
  HAVING AVG(EXTRACT(year from AGE(CURRENT_TIMESTAMP, birth_date))) > 60;
""", ('Redmond', Decimal('87'))),

("""SELECT first_name, last_name, EXTRACT(year from AGE(CURRENT_TIMESTAMP, birth_date)) AS age
 FROM employees
 ORDER BY age DESC
 LIMIT 3;
""", ('Margaret', 'Peacock', Decimal('87')))
)

@pytest.mark.parametrize("execute_query, expected_result", TEST_DATA, indirect=["execute_query"])
def test_first_row_of_sql_queries(execute_query, expected_result):
    assert execute_query.fetchone() == expected_result
    # TODO: test the whole result, instead of only first line?
