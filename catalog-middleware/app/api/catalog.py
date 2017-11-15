from flask_restful import Resource
from flask import request
# import MySQLdb
import os
import mysql.connector

# import settings
# from app import app
# Get database settings from environment variables
MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST")
MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER")
MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD")
MYSQL_DATABASE_DB = os.getenv("MYSQL_DATABASE_DB")

class Catalog(Resource):

    def get(self):

        # Handle catalog search
        keyword = request.args.get('keyword')
        if keyword:
            return {'keyword': keyword}

        else:
            cnx = mysql.connector.connect(user=MYSQL_DATABASE_USER, 
                                    password=MYSQL_DATABASE_PASSWORD,
                                    host=MYSQL_DATABASE_HOST)

            cursor = cnx.cursor()

            sql = "SELECT title, author, publisher FROM catalog.books LIMIT 20"
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = cursor.fetchall()
                books = []

                for row in results:
                    books_dict = {}
                    books_dict["title"] = row[0]
                    books_dict["author"] = row[1]
                    books_dict["publisher"] = row[2]
                    books.append(books_dict)

                return books
 
            except:
                print("Error: unable to fetch data")

            finally:
                cursor.close()
    