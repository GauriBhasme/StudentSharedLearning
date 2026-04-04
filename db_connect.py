import pymysql
import dotenv
import os

dotenv.load_dotenv()

def connect_to_database():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),  
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("Successfully connected to MySQL database")
        return connection
    except pymysql.MySQLError as error:
        print("Failed to connect to MySQL database: {}".format(error))
        return None
    finally:
        if connection:
            connection.close()

