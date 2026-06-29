import streamlit as st
import pandas as pd
import sqlite3
with st.sidebar:

    if st.button("Home"):

        st.switch_page("app.py")
# ==================================
# DATABASE
# ==================================

DB_NAME = "complaints.db"

st.set_page_config(
    page_title="Track Complaint",
    page_icon="",
    layout="wide"
)

st.title("Track Complaint")

st.write(
    "Enter your Complaint ID to check its current status."
)

complaint_id = st.text_input(
    "Complaint ID",
    placeholder="CMP-XXXXXXXX"
)

if st.button("Track Complaint"):

    if complaint_id:

        conn = sqlite3.connect(DB_NAME)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                complaint_id,
                complaint_text,
                status
            FROM complaints
            WHERE complaint_id=?
            """,
            (complaint_id,)
        )

        complaint = cursor.fetchone()

        conn.close()

        if complaint:

            st.success(
                "Complaint Found"
            )

            df = pd.DataFrame(
                [complaint],
                columns=[
                    "Complaint ID",
                    "Complaint",
                    "Status"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.error(
                "Complaint ID not found."
            )

    else:

        st.warning(
            "Please enter a Complaint ID."
        )