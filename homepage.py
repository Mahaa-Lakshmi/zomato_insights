import streamlit as st
from databaseManager import DatabaseManager

class ZomatoDataInsightsApp:
    def __init__(self):
        self.db_manager = DatabaseManager(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="zomato"
        )

    def run(self):
       
        st.markdown("""
# Zomato Food Delivery Data Insights
=====================================

## Overview
The Zomato Food Delivery Data Insights project is an interactive data analysis and database management system designed for food delivery analytics. Built using Python, MySQL, and Streamlit, this project empowers users to manage and analyze food delivery data for operational efficiency and improved customer satisfaction.

## Features
*   **Database Management**: Dynamically manage customers, restaurants, orders, delivery personnel, and deliveries data. Perform CRUD (Create, Read, Update, Delete) operations on all database tables.
*   **Interactive Insights**: Retrieve insights from the database using predefined SQL queries. Analyze trends such as:
    *   Peak ordering times and locations.
    *   Most popular restaurants and cuisines.
    *   Customer preferences and spending patterns.
    *   Delivery performance and optimization metrics.
*   **Dynamic Table Creation**: Define new tables dynamically as per business requirements. Add, modify, or drop columns and tables seamlessly.
*   **Visualization**: Use Streamlit for interactive dashboards to display insights and manage the database.
""")


app = ZomatoDataInsightsApp()
app.run()