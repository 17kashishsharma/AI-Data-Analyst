import streamlit as st
import sqlite3
import pandas as pd

from main import extract_schema, text_to_sql


DB_URL = "sqlite:///amazon.db"
DB_PATH = "amazon.db"


def run_query(sql_query):
    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(sql_query, conn)
        return df

    finally:
        conn.close()


# ----------------------------
# UI
# ----------------------------

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL Assistant")

st.write(
    "Ask questions in natural language and get results from your database."
)

user_question = st.text_input(
    "Enter your question",
    placeholder="Show all customer names"
)

if st.button("Generate SQL & Execute"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    try:

        with st.spinner("Extracting schema..."):
            schema = extract_schema(DB_URL)

        with st.spinner("Generating SQL..."):
            sql_query = text_to_sql(schema, user_question)

        st.subheader("Generated SQL")

        st.code(sql_query, language="sql")

        with st.spinner("Executing query..."):
            result_df = run_query(sql_query)

        st.subheader("Results")

        st.dataframe(
            result_df,
            use_container_width=True
        )

        st.success(
            f"{len(result_df)} rows returned"
        )

    except Exception as e:
        st.error(f"Error: {e}")