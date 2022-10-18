

import psycopg2
from sshtunnel import SSHTunnelForwarder

username = "your username"
password = "your password"
dbName = "p32001_17"


def execute_query(connection, query):
    cursr = connection.cursor()
    try:
        cursr.execute(query)
        connection.commit()
        print("Query Successful")
    except:
        print("Query failed")


def read_query(connection, query):
    cursr = connection.cursor()
    result = None
    try:
        cursr.execute(query)
        result = cursr.fetchall()
        return result
    except:
        print("reading failed")


if __name__ == '__main__':
    try:
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('localhost', 5432)) as server:
            server.start()
            print("SSH tunnel established")
            params = {
                'database': dbName,
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': server.local_bind_port
            }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            print("Database connection established")

            """
            # this is the test code
            test_table = "create table test(test int PRIMARY KEY)"
            test_read = "select * from users"
            execute_query(conn, test_table)

            results = read_query(conn, test_read)
            for result in results:
                print(result)
            """

            conn.close()
    except:
        print("Connection failed")
