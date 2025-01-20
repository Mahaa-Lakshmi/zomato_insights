# Zomato Food Delivery Data Insights

## Overview

The **Zomato Food Delivery Data Insights** project is a comprehensive platform designed for data analysis and database management in the food delivery domain. Built with Python, MySQL, and Streamlit, it empowers users to manage databases, generate insights, and interact with data in a user-friendly way.

---

## Features

- **Database Management**: Perform CRUD (Create, Read, Update, Delete) operations on tables such as `Customers`, `Orders`, `Restaurants`, `Delivery Persons` and `Deliveries`.
- **Insights Generation**: Gain actionable insights into:
  - Peak ordering times and locations.
  - Most popular restaurants and cuisines.
  - Customer preferences and spending patterns.
  - Delivery performance metrics.
- **Dynamic Table Operations**: Add, modify, or drop tables and columns as per business needs.
- **Interactive Visualizations**: View insights and manage data interactively through Streamlit dashboards.

---

## Getting Started

### Prerequisites

- Python (>= 3.8)
- MySQL Server
- Required Python libraries (see `requirements.txt`)

### Installation

1. Clone the repository or download the project files.
2. Install the required Python libraries by running:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your MySQL server and ensure the credentials in `databaseManager.py` match your setup.

---

## Usage

### Initial Setup (First-Time Run)

1. If starting with a fresh database, populate it with mock data:
   - Open and run all cells in the `dataPopulation.ipynb` file. 
   - This will insert sample data into your database using the `Faker` library.

### Starting the Application

1. If the database already exists and contains data, you can directly start the Streamlit application:
   - Run the following command:
     ```bash
     streamlit run app.py
     ```

2. Open the link displayed in your terminal to access the Streamlit app.

### Application Features

- Navigate to the CRUD operations section to manage database entries.
- Explore the insights section to view analytical insights derived from the data.

---

## File Structure

- `CRUD_operations.py`: Handles CRUD operations on database tables.
- `app.py`: Entry point for the Streamlit application.
- `dataPopulation.ipynb`: Populates the database with mock data for initial setup.
- `databaseManager.py`: Manages MySQL database connections and queries.
- `homepage.py`: Contains the project overview and features for the Streamlit app.
- `insights.py`: Provides analytical insights into the Zomato data.
- `requirements.txt`: Lists the required Python libraries.

---

## Example Insights

- **Peak Ordering Times**: Identify the hours when most orders are placed.
- **Customer Preferences**: Analyze preferred cuisines and order patterns.
- **Delivery Metrics**: Evaluate delivery performance and identify delays or cancellations.

---

## Notes

- Ensure your MySQL database is running before starting the app.
- Modify `databaseManager.py` to update the database credentials if necessary.

---
