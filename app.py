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

st.title("Telecom NOC Operations & Docket Portal")

records = load_data()

menu = st.sidebar.radio("Navigation", ["Dashboard & View / Edit", "Add New Site Record"])

if menu == "Add New Site Record":
    st.header("Add New Site & Docket Record")
    with st.form("add_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            saipId = st.text_input("SAIP ID *")
            jc = st.text_input("JC *")
            state = st.text_input("State *")
            supervisorName = st.text_input("Supervisor Name *")
        with col2:
            trtName = st.text_input("TRT Name")
            contactNo = st.text_input("Contact No.")
            siteType = st.text_input("Site Type")
            facility5g = st.selectbox("5G Facility", ["Yes", "No"])
        with col3:
            dgMake = st.text_input("DG Make")
            dgRating = st.text_input("DG Rating")
            oemVendor = st.text_input("OEM Vendor")
            ebNonEb = st.selectbox("EB/Non EB", ["EB", "Non EB"])
        with col4:
            docketNo = st.text_input("Docket No.")
            bucket = st.text_input("Bucket (e.g. Critical / Active)")
            agingDays = st.number_input("Aging (Days)", min_value=0, value=1)
            presentRemarks = st.text_input("Present Remarks")

        submitted = st.form_submit_button("Save New Record")
        if submitted:
            if saipId and jc and state and supervisorName:
                new_item = {
                    "saipId": saipId, "jc": jc, "state": state, "supervisorName": supervisorName,
                    "trtName": trtName, "contactNo": contactNo, "siteType": siteType, "facility5g": facility5g,
                    "dgMake": dgMake, "dgRating": dgRating, "oemVendor": oemVendor, "ebNonEb": ebNonEb,
                    "dependentSite": "", "fuelSensorStatus": "", "docketNo": docketNo,
                    "openDate": "2026-10-02", "bucket": bucket, "presentDocketNo": "",
                    "presentDocketRaiseDate": "", "agingDays": str(agingDays), "timeline": "",
                    "presentRemarks": presentRemarks, "previousRemarks": "", "previousDocketNo": "",
                    "previousDocketRaiseDate": "", "lastClosedDate": "", "batteryBackupMin": ""
                }
                records.insert(0, new_item)
                save_data(records)
                st.success(f"Site {saipId} added successfully!")
            else:
                st.error("Please fill all mandatory fields (SAIP ID, JC, State, Supervisor Name).")

else:
    st.header("Live Records Dashboard (Search, Edit & Delete)")
    
    if len(records) == 0:
        st.info("No records found.")
    else:
        search_query = st.text_input("Search by SAIP ID, State, Supervisor, or Docket:", "")
        
        filtered_records = records
        if search_query:
            filtered_records = [
                r for r in records if any(search_query.lower() in str(val).lower() for val in r.values())
            ]

        st.write(f"Showing **{len(filtered_records)}** of **{len(records)}** total records.")

        if len(filtered_records) > 0:
            selected_index = st.selectbox(
                "Select a Site Record to Edit or Delete:",
                options=range(len(filtered_records)),
                format_func=lambda i: f"SAIP ID: {filtered_records[i].get('saipId', 'N/A')} | State: {filtered_records[i].get('state', 'N/A')} | Supervisor: {filtered_records[i].get('supervisorName', 'N/A')}"
            )

            if selected_index is not None:
                actual_record = filtered_records[selected_index]
                orig_index = records.index(actual_record)

                with st.form("edit_form"):
                    st.subheader(f"Editing Record: {actual_record.get('saipId', '')}")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        e_saipId = st.text_input("SAIP ID", value=actual_record.get("saipId", ""))
                        e_jc = st.text_input("JC", value=actual_record.get("jc", ""))
                        e_state = st.text_input("State", value=actual_record.get("state", ""))
                        e_supervisorName = st.text_input("Supervisor Name", value=actual_record.get("supervisorName", ""))
                    with col2:
                        e_trtName = st.text_input("TRT Name", value=actual_record.get("trtName", ""))
                        e_contactNo = st.text_input("Contact No.", value=actual_record.get("contactNo", ""))
                        e_siteType = st.text_input("Site Type", value=actual_record.get("siteType", ""))
                        e_facility5g = st.selectbox("5G Facility", ["Yes", "No"], index=0 if actual_record.get("facility5g","Yes")=="Yes" else 1)
                    with col3:
                        e_dgMake = st.text_input("DG Make", value=actual_record.get("dgMake", ""))
                        e_dgRating = st.text_input("DG Rating", value=actual_record.get("dgRating", ""))
                        e_oemVendor = st.text_input("OEM Vendor", value=actual_record.get("oemVendor", ""))
                        e_bucket = st.text_input("Bucket", value=actual_record.get("bucket", ""))
                    with col4:
                        e_docketNo = st.text_input("Docket No.", value=actual_record.get("docketNo", ""))
                        e_agingDays = st.text_input("Aging Days", value=actual_record.get("agingDays", "0"))
                        e_presentRemarks = st.text_input("Present Remarks", value=actual_record.get("presentRemarks", ""))
                        e_batteryBackupMin = st.text_input("Battery Backup (Min)", value=actual_record.get("batteryBackupMin", ""))

                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        update_btn = st.form_submit_button("Save Updates")
                    with col_btn2:
                        delete_btn = st.form_submit_button("Delete This Record")

                    if update_btn:
                        records[orig_index] = {
                            **actual_record,
                            "saipId": e_saipId, "jc": e_jc, "state": e_state, "supervisorName": e_supervisorName,
                            "trtName": e_trtName, "contactNo": e_contactNo, "siteType": e_siteType, "facility5g": e_facility5g,
                            "dgMake": e_dgMake, "dgRating": e_dgRating, "oemVendor": e_oemVendor, "bucket": e_bucket,
                            "docketNo": e_docketNo, "agingDays": e_agingDays, "presentRemarks": e_presentRemarks,
                            "batteryBackupMin": e_batteryBackupMin
                        }
                        save_data(records)
                        st.success("Record updated successfully!")
                        st.rerun()

                    if delete_btn:
                        records.pop(orig_index)
                        save_data(records)
                        st.warning("Record deleted successfully!")
                        st.rerun()

        st.divider()
        st.subheader("Complete Master Data Table")
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Master Data as CSV",
        data=csv_data,
        file_name="telecom_noc_master_records.csv",
        mime="text/csv",
    )
