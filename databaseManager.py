import mysql.connector as db
import pandas as pd
import re

class DatabaseManager:
    def __init__(self, host, port, user, password, database):
        self.cnx = db.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=True
        )
        self.db_curr = self.cnx.cursor(dictionary=True)
        self.db_name = database
        self.queries = {
            "Identify peak ordering hours": "SELECT HOUR(order_date) AS order_hour, COUNT(*) AS total_orders FROM Orders GROUP BY order_hour ORDER BY total_orders DESC;",
            "Track delayed and canceled deliveries": "SELECT order_id, delivery_status, estimated_time, delivery_time FROM Deliveries WHERE delivery_status IN ('Delayed', 'Cancelled');",
            "Analyze customer preferences and order patterns": "SELECT preferred_cuisine, COUNT(*) AS total_orders FROM Customers JOIN Orders ON Customers.customer_id = Orders.customer_id GROUP BY preferred_cuisine ORDER BY total_orders DESC;",
            "Evaluate most popular restaurants and cuisines": "SELECT name, cuisine_type, total_orders FROM Restaurants ORDER BY total_orders DESC LIMIT 10;",
            "customers with highest order frequency": "SELECT name, total_orders FROM Customers ORDER BY total_orders DESC LIMIT 10;",
            "the average rating given by customers to restaurants": "SELECT AVG(rating) AS average_rating FROM Restaurants;",
            "payment modes are most commonly used": "SELECT payment_mode, COUNT(*) AS usage_count FROM Orders GROUP BY payment_mode ORDER BY usage_count DESC;",
            "customers who spent the most on orders": "SELECT name, SUM(total_amount) AS total_spent FROM Orders JOIN Customers ON Orders.customer_id = Customers.customer_id GROUP BY name ORDER BY total_spent DESC LIMIT 10;",
            "The average actual and estimated delivery times for all orders": "SELECT AVG(delivery_time) AS average_actual_time, AVG(estimated_time) AS average_estimated_time FROM Deliveries;",
            "Which restaurants have received the highest number of orders": "SELECT name, total_orders FROM Restaurants ORDER BY total_orders DESC LIMIT 10;",
            "Which cuisines generate the highest revenue": "SELECT cuisine_type, SUM(total_amount) AS total_revenue FROM Orders JOIN Restaurants ON Orders.restaurant_id = Restaurants.restaurant_id GROUP BY cuisine_type ORDER BY total_revenue DESC;",
            "delivery personnel who have the highest average customer ratings": "SELECT name, AVG(average_rating) AS average_rating FROM Delivery_persons GROUP BY name ORDER BY average_rating DESC LIMIT 10;",
            "delivery personnel cover the longest average delivery distances": "SELECT name, AVG(distance) AS average_distance FROM Deliveries JOIN Delivery_persons ON Deliveries.delivery_person_id = Delivery_persons.delivery_person_id GROUP BY name ORDER BY average_distance DESC LIMIT 10;",
        }

    def execute_query(self, query):
        try:
            self.db_curr.execute(query)
            return self.db_curr.fetchall()
        except db.Error as err:
            print(f"Error: {err}")
            return None

    def show_table_definition(self, table_name):
        query = f"SHOW CREATE TABLE {table_name};"
        result = self.execute_query(query)
        return re.search(r"\((.*)\)", result[0]['Create Table'], re.DOTALL).group(1)

    def show_tables(self):
        query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{self.db_name}';"
        return [table['TABLE_NAME'] for table in self.execute_query(query)]

    def show_columns(self, table_name):
        query = f"""SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{self.db_name}';"""
        return [col['COLUMN_NAME'] for col in self.execute_query(query)]

    def show_columns_dict(self, table_name):
        query = f"""SELECT COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = '{self.db_name}';"""
        return {item['COLUMN_NAME']: item['DATA_TYPE'] for item in self.execute_query(query)}

    def create_table(self, table_name, values):
        query = f"""CREATE TABLE {table_name} ({values});"""
        try:
            self.db_curr.execute(query)
            self.cnx.commit()
            return pd.DataFrame(self.execute_query(f"DESC {table_name};"), columns=['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'])
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def insert_into_db(self, table_name, values):
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        try:
            self.db_curr.execute(query, values)
            self.cnx.commit()
            return "Data inserted successfully!"
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def read_from_db(self, table_name):
        query = f"SELECT * FROM {table_name};"
        return self.execute_query(query)

    def update_table(self, query):
        try:
            self.db_curr.execute(query)
            self.cnx.commit()
            return "Data updated successfully!"
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def drop_table(self, table_name):
        query = f"DROP TABLE {table_name};"
        try:
            self.db_curr.execute(query)
            return "Table deleted successfully!"
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def delete_table(self, query):
        try:
            self.db_curr.execute(query)
            return "Data deleted successfully!"
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def get_questions(self):
        return list(self.queries.keys())

    def get_queries_from_DB(self, question):
        try:
            self.db_curr.execute(self.queries[question])
            return self.db_curr.fetchall()
        except db.Error as err:
            return f"Error: {err}"
        
    def alter_table_add_column(self, table_name, column_definition):
        """
        Add a new column to an existing table.
        """
        query = f"ALTER TABLE {table_name} ADD COLUMN {column_definition};"
        try:
            self.db_curr.execute(query)
            self.cnx.commit()
            return f"Column '{column_definition}' added successfully to '{table_name}'."
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def alter_table_modify_column(self, table_name, column_definition):
        """
        Modify an existing column in a table.
        """
        query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_definition};"
        try:
            self.db_curr.execute(query)
            self.cnx.commit()
            return f"Column '{column_definition}' modified successfully in '{table_name}'."
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"
    
    def alter_table_drop_column(self, table_name, column_name):
        """
        Drop a column from an existing table.
        """
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        try:
            self.db_curr.execute(query)
            self.cnx.commit()
            return f"Column '{column_name}' dropped successfully from '{table_name}'."
        except db.Error as err:
            self.cnx.rollback()
            return f"Error: {err}"

    def close_connection(self):
        self.db_curr.close()
        self.cnx.close()
        print("Database connection closed.")