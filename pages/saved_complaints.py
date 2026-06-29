import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from modules.database import (
    get_all_complaints
)

st.set_page_config(
    page_title="Saved Complaints",
    layout="wide"
)

st.title("Saved Complaints")

complaints = get_all_complaints()

if complaints:

    data = []

    for index, complaint in enumerate(
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
                index,
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

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No complaints found."
    )