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
        st.title("Zomato Data Insights")
        st.write("This app provides insights into the Zomato dataset.")
        questions = self.db_manager.get_questions()
        question_chosen = st.selectbox("Choose a question to view the insights", questions)
        insights = self.db_manager.get_queries_from_DB(question_chosen)
        if insights:
            st.dataframe(insights, use_container_width=True)
        else:
            st.error("Failed to fetch data from the database.")


app = ZomatoDataInsightsApp()
app.run()