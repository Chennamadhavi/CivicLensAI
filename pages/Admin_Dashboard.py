import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from modules.database import (
    get_all_complaints,
    update_status
)

st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide"
)

st.title("Admin Dashboard")

complaints = get_all_complaints()

if complaints:

    data = []

    for i, complaint in enumerate(
        complaints,
        start=1
    ):

        complaint_id = complaint[0]
        complaint_text = complaint[1]
        location = complaint[2]
        maps_link = complaint[3]
        status = complaint[4]
        created_at = complaint[5]

        try:

            utc_time = datetime.strptime(
                created_at,
                "%Y-%m-%d %H:%M:%S"
            )

            ist_time = utc_time + timedelta(
                hours=5,
                minutes=30
            )

            created_at = ist_time.strftime(
                "%d-%b-%Y %I:%M %p"
            )

        except:

            pass

        data.append(
            [
                i,
                complaint_id,
                complaint_text,
                location,
                maps_link,
                status,
                created_at
            ]
        )

    df = pd.DataFrame(
        data,
        columns=[
            "S.No",
            "Complaint ID",
            "Complaint",
            "Location",
            "Maps Link",
            "Status",
            "Submitted On"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Complaints",
            len(df)
        )

    with col2:
        st.metric(
            "Open",
            len(
                df[df["Status"] == "Open"]
            )
        )

    with col3:
        st.metric(
            "In Progress",
            len(
                df[df["Status"] == "In Progress"]
            )
        )

    with col4:
        st.metric(
            "Resolved",
            len(
                df[df["Status"] == "Resolved"]
            )
        )

    st.markdown("---")

    st.subheader("Complaints Table")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Update Complaint Status")

    selected_id = st.selectbox(
        "Select Complaint",
        df["Complaint ID"].tolist()
    )

    selected_row = df[
        df["Complaint ID"] == selected_id
    ]

    st.dataframe(
        selected_row,
        use_container_width=True,
        hide_index=True
    )

    new_status = st.selectbox(
        "New Status",
        [
            "Open",
            "In Progress",
            "Resolved"
        ]
    )

    if st.button("Update Status"):

        update_status(
            selected_id,
            new_status
        )

        st.success(
            f"{selected_id} updated successfully."
        )

        st.rerun()

else:

    st.info(
        "No complaints available."
    )