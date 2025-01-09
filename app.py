import streamlit as st

pg = st.navigation([st.Page("homepage.py"), st.Page("CRUD_operations.py"), st.Page("insights.py")])

pg.run()
