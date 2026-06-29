import streamlit as st
import uuid
import json
import pandas as pd

from modules.classify import classify_issue
from modules.image_analyzer import analyze_images
import modules.database as db

st.set_page_config(
    page_title="CivicLens AI",
    layout="wide"
)

db.init_db()

st.title("CivicLens AI")

st.info(
    "Upload images or enter a complaint description, then click Send to analyze the issue."
)

uploaded_files = st.file_uploader(
    "Upload Images",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "bmp",
        "gif",
        "tiff",
        "tif"
    ],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 5:

    st.error(
        "Maximum 5 images allowed."
    )

    st.stop()

if uploaded_files:

    st.write(
        f"{len(uploaded_files)} image(s) selected"
    )

    cols = st.columns(
        min(len(uploaded_files), 5)
    )

    for i, image in enumerate(uploaded_files):

        with cols[i % 5]:

            st.image(
                image,
                width=120
            )

st.markdown("---")

with st.form("complaint_form"):

    complaint = st.text_input(
        "Complaint Description",
        placeholder="Describe a civic issue..."
    )

    location = st.text_input(
        "Location",
        placeholder="e.g. Near Bus Stand, Nandyal"
    )

    maps_link = st.text_input(
        "Google Maps Link (Optional)",
        placeholder="https://maps.google.com/..."
    )

    submitted = st.form_submit_button(
        "Send"
    )

location = location.title() if location else ""

if submitted:

    if not complaint and not uploaded_files:

        st.warning(
            "Please enter a complaint or upload at least one image."
        )

    elif not location:

        st.warning(
            "Please provide the complaint location."
        )

    else:

        complaint_id = (
            "CMP-" +
            str(uuid.uuid4())[:8].upper()
        )

        try:

            with st.spinner(
                "Analyzing complaint..."
            ):

                if uploaded_files:

                    result = analyze_images(
                        uploaded_files
                    )

                else:

                    result = classify_issue(
                        complaint
                    )

            result = result.replace(
                "```json",
                ""
            )

            result = result.replace(
                "```",
                ""
            )

            result = result.strip()

            data = json.loads(
                result
            )

            db.save_complaint(
                complaint_id,
                complaint if complaint else "Image Complaint",
                json.dumps(data),
                location,
                maps_link
            )

            st.success(
                "Complaint Submitted Successfully"
            )

            st.markdown(
                f"""
### Complaint Registered

**Complaint ID:** `{complaint_id}`

**Location:** {location}

**Expected Response Time:** Within 24 Hours
"""
            )

            result_df = pd.DataFrame(
                {
                    "Field": [
                        "Category",
                        "Severity",
                        "Department",
                        "Summary"
                    ],
                    "Value": [
                        data.get("category", "N/A"),
                        data.get("severity", "N/A"),
                        data.get("department", "N/A"),
                        data.get("summary", "N/A")
                    ]
                }
            )

            st.subheader(
                "Analysis Result"
            )

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )

            if data.get("title"):

                st.subheader(
                    "Complaint Title"
                )

                st.write(
                    data["title"]
                )

            if data.get("description"):

                st.subheader(
                    "Complaint Description"
                )

                st.write(
                    data["description"]
                )

        except Exception as e:

            import traceback

            st.error(
                f"Error: {str(e)}"
            )

            st.code(
                traceback.format_exc()
            )