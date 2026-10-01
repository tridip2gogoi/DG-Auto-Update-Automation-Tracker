import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Telecom NOC Portal", layout="wide")

DATA_FILE = 'telecom_records.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return [
        {
            "saipId": "SAIP90211", "jc": "JC-7712", "state": "Assam", "supervisorName": "Bikash Gogoi",
            "trtName": "TRT-Guwahati", "contactNo": "9876543210", "siteType": "Ground", "facility5g": "Yes",
            "dgMake": "Kirloskar", "dgRating": "25 KVA", "oemVendor": "Indus", "ebNonEb": "EB",
            "dependentSite": "None", "fuelSensorStatus": "Working", "docketNo": "DOC-40192",
            "openDate": "2026-05-01", "bucket": "Critical", "presentDocketNo": "PDOC-9981",
            "presentDocketRaiseDate": "2026-05-10", "agingDays": "5", "timeline": "24 Hrs",
            "presentRemarks": "DG battery low voltage issue", "previousRemarks": "Resolved previously",
            "previousDocketNo": "PDOC-8812", "previousDocketRaiseDate": "2026-04-10",
            "lastClosedDate": "2026-04-15", "batteryBackupMin": "120"
        }
    ]

def save_data(records):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=4)

st.title("🗼 Telecom NOC Operations & Docket Portal")

records = load_data()

# Sidebar for adding new record
st.sidebar.header("Add / Manage Records")
with st.sidebar.form("record_form"):
    saipId = st.text_input("SAIP ID")
    jc = st.text_input("JC")
    state = st.text_input("State")
    supervisorName = st.text_input("Supervisor Name")
    docketNo = st.text_input("Docket No.")
    bucket = st.text_input("Bucket (e.g. Critical)")
    
    submitted = st.form_submit_button("Save Record")
    if submitted and saipId:
        new_item = {
            "saipId": saipId, "jc": jc, "state": state, "supervisorName": supervisorName,
            "docketNo": docketNo, "bucket": bucket, "openDate": "2026-05-01", "agingDays": "2"
        }
        records.insert(0, new_item)
        save_data(records)
        st.success("Record Saved Successfully!")
        st.rerun()

# Main Display
st.subheader("Site Records Dashboard")
df = pd.DataFrame(records)
st.dataframe(df, use_container_width=True)
