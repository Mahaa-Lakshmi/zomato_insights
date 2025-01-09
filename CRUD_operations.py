import streamlit as st
import databaseManager as dm
import datetime

class CRUDApp:
    def __init__(self):
        self.db_manager = dm.DatabaseManager(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="zomato"
        )
        self.op_choice = None
        self.selected_table = None

    def run(self):
        st.markdown("""
        - You can do CRUD operations here!<br>
        - Select 1 CRUD option from the left sidebar.:point_left: 
        """, True)

        self.op_choice = st.sidebar.selectbox(
            "Choose any 1 CRUD options you like to perform",
            ["CREATE","INSERT", "READ", "UPDATE", "DELETE","ALTER"],
            index=None,
            placeholder="Select one operation..."
        )

        if self.op_choice:
            st.session_state.op_choice = self.op_choice

        if 'op_choice' in st.session_state and self.op_choice:
            getattr(self, f"{self.op_choice.lower()}_operation")()

    def create_operation(self):
        self.table_name = st.text_input("Enter name of the table")
        st.write("Enter the values as shown below. Ex. Column_name datatype")
        st.code("""customer_id INT NOT NULL,\nOrderNumber INT NOT NULL,\nPersonID INT NOT NULL,\nPRIMARY KEY (PersonID),\nFOREIGN KEY (customer_id) REFERENCES customers(customer_id)""", language="sql")
        self.table_values = st.text_area("")
        if self.table_name and self.table_values:
            if st.button("CREATE TABLE"):
                result = self.db_manager.create_table(self.table_name, self.table_values)
                if isinstance(result, str):
                    st.write(result)
                else:
                    st.dataframe(result, hide_index=True)
        else:
            st.warning("Please fill in all fields")

    def insert_operation(self):
        self.selected_table = st.selectbox(
            "Choose a table to insert record",
            self.db_manager.show_tables(),
            index=None,
            placeholder="Select a table..."
        )
        if self.selected_table:
            column_names, column_types = list(zip(*self.db_manager.show_columns_dict(self.selected_table).items()))
            values = []
            for column_name, column_type in zip(column_names, column_types):
                column_type = column_type.upper()
                value = self.get_input_value(column_name, column_type)
                values.append(value)
            if st.button("INSERT"):
                st.write(self.db_manager.insert_into_db(self.selected_table, values))

    def read_operation(self):
        self.selected_table = st.selectbox(
            "Choose a table to read record",
            self.db_manager.show_tables(),
            index=None,
            placeholder="Select a table..."
        )
        if self.selected_table:
            data = self.db_manager.read_from_db(self.selected_table)
            if data:
                st.dataframe(data)
            else:
                st.error("Failed to fetch data from the database.")

    def update_operation(self):
        self.selected_table = st.selectbox(
            "Choose a table to update record",
            self.db_manager.show_tables(),
            index=None,
            placeholder="Select a table..."
        )
        if self.selected_table:
            column_names, column_types = list(zip(*self.db_manager.show_columns_dict(self.selected_table).items()))
            column_name = st.selectbox("Select the column of the condition", column_names, index=None)
            if column_name in column_names:
                column_type = column_types[column_names.index(column_name)]
                column_type = column_type.upper()
                value = self.get_input_value(column_name, column_type)
                condn_col_value = value
                update_column_name = st.selectbox("Select the column to be updated", column_names, index=None)
                if update_column_name in column_names:
                    column_type = column_types[column_names.index(update_column_name)]
                    column_type = column_type.upper()
                    value = self.get_input_value(update_column_name, column_type)
                    update_col_value = value
                    sql_query = f"""update {self.selected_table} set {update_column_name}={update_col_value} where {column_name}={condn_col_value};"""
                    st.write(sql_query)
                    if st.button("UPDATE"):
                        st.write(self.db_manager.update_table(sql_query))

    def delete_operation(self):
        drop_delete_option = st.selectbox(
            "Choose a option to perform",
            ["Delete row records","Drop table"],
            index=None,
            placeholder="Select a option..."
        )
        if drop_delete_option == "Drop table":
            self.selected_table = st.selectbox(
                "Choose a table to drop",
                self.db_manager.show_tables(),
                index=None,
                placeholder="Select a table..."
            )
            if st.checkbox("Are you sure to delete the table permanently?"):
                st.write(self.selected_table)
                st.write(self.db_manager.drop_table(self.selected_table))
        else:
            self.selected_table = st.selectbox(
                "Choose a table to delete record",
                self.db_manager.show_tables(),
                index=None,
                placeholder="Select a table..."
            )
            if self.selected_table:
                column_names, column_types = list(zip(*self.db_manager.show_columns_dict(self.selected_table).items()))
                column_name = st.selectbox("Select the column of the condition", column_names, index=None)
                if column_name in column_names:
                    column_type = column_types[column_names.index(column_name)]
                    column_type = column_type.upper()
                    value = self.get_input_value(column_name, column_type)
                    delete_value = value
                    sql_query = f"""delete from {self.selected_table} where {column_name}={delete_value};"""
                    st.write(sql_query)
                    if st.button("DELETE"):
                        st.write(self.db_manager.delete_table(sql_query))

    def get_input_value(self, column_name, column_type):
        if column_type.startswith(("SMALLINT", "MEDIUMINT", "INT", "INTEGER", "BIGINT", "BIT", "TINYINT")):
            return st.number_input(f"Enter {column_name} value", min_value=0, step=1)
        elif column_type.startswith(("CHAR", "VARCHAR", "BINARY", "VARBINARY", "TINYBLOB", "TINYTEXT", "TEXT", "BLOB", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT", "LONGBLOB", "ENUM", "SET")):
            return st.text_input(f"Enter {column_name} value")
        elif column_type == "DATE":
            return st.date_input(f"Enter {column_name} value")
        elif column_type == "DATETIME":
            return datetime.datetime.combine(st.date_input(f"Enter {column_name} value"), st.time_input(f"Enter {column_name} timestamp value"))
        elif column_type in ["BOOLEAN", "BOOL"]:
            return st.selectbox(f"Enter {column_name} value", [True, False])
        elif column_type.startswith(("FLOAT", "DOUBLE", "DECIMAL", "DEC")):
            return st.number_input(f"Enter {column_name} value")
        else:
            return st.text_input(f"Enter {column_name} value")
        
    def alter_operation(self):
        """
        Handles ALTER operations (Add, Modify, Drop columns) via Streamlit.
        """
        self.selected_table = st.selectbox(
            "Choose a table to alter",
            self.db_manager.show_tables(),
            index=None,
            placeholder="Select a table..."
        )
        alter_type = st.radio(
            "Choose ALTER operation",
            ["Add Column", "Modify Column", "Drop Column"],
            horizontal=True
        )
        if self.selected_table:
            if alter_type == "Add Column":
                column_definition = st.text_input("Enter new column definition (e.g., column_name DATA_TYPE):")
                if st.button("Add Column"):
                    result = self.db_manager.alter_table_add_column(self.selected_table, column_definition)
                    st.write(result)
            elif alter_type == "Modify Column":
                column_definition = st.text_input("Enter modified column definition (e.g., column_name NEW_DATA_TYPE):")
                if st.button("Modify Column"):
                    result = self.db_manager.alter_table_modify_column(self.selected_table, column_definition)
                    st.write(result)
            elif alter_type == "Drop Column":
                column_name = st.selectbox(
                    "Choose a column to drop",
                    self.db_manager.show_columns(self.selected_table),
                    index=None,
                    placeholder="Select a column..."
                )
                if st.button("Drop Column"):
                    result = self.db_manager.alter_table_drop_column(self.selected_table, column_name)
                    st.write(result)

app = CRUDApp()
app.run()