import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Health Risk System",
    page_icon="🩺",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS (MAKE UI BEAUTIFUL)
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f6f9fc;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #1f4e79;
    }
    .subtitle {
        font-size: 16px;
        color: gray;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown('<div class="title">🩺 Patient Health Risk Assessment System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered health prediction using Python + SQLite</div>', unsafe_allow_html=True)

st.divider()

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["➕ Add Patient", "📊 View Records", "🗑️ Delete Record", "✏️ Update Record"]
)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_connection():
    return sqlite3.connect("patients.db")

# -----------------------------
# ADD PATIENT
# -----------------------------
if menu == "➕ Add Patient":

    st.subheader("Add New Patient")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        dob = st.date_input("Date of Birth", value=date(2004, 1, 1))

    with col2:
        glucose = st.number_input("Glucose", 0, 500, 0)
        haemoglobin = st.number_input("Haemoglobin", 0, 30, 0)
        cholesterol = st.number_input("Cholesterol", 0, 500, 0)

    if st.button("Submit Patient"):

        if "@" not in email or "." not in email:
            st.error("Invalid Email Address")

        elif dob > date.today():
            st.error("Invalid Date of Birth")

        else:

            if glucose > 140 and cholesterol > 200:
                remarks = "High Diabetes & Heart Risk"
            elif glucose > 140:
                remarks = "Possible Diabetes Risk"
            elif cholesterol > 200:
                remarks = "Possible Heart Risk"
            else:
                remarks = "No Significant Risk"

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO patients
                (name, dob, email, glucose, haemoglobin, cholesterol, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, str(dob), email, glucose, haemoglobin, cholesterol, remarks))

            conn.commit()
            conn.close()

            st.success("Patient Added Successfully ✅")
            st.info(f"Prediction: {remarks}")

# -----------------------------
# VIEW RECORDS
# -----------------------------
elif menu == "📊 View Records":

    st.subheader("All Patient Records")

    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()

    st.dataframe(df, use_container_width=True)

    st.metric("Total Patients", len(df))

# -----------------------------
# DELETE RECORD
# -----------------------------
elif menu == "🗑️ Delete Record":

    st.subheader("Delete Patient")

    delete_id = st.number_input("Enter Patient ID", min_value=1, step=1)

    if st.button("Delete Record"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM patients WHERE id=?", (delete_id,))

        conn.commit()
        conn.close()

        st.success("Record Deleted Successfully 🗑️")

# -----------------------------
# UPDATE RECORD
# -----------------------------
elif menu == "✏️ Update Record":

    st.subheader("Update Patient Data")

    update_id = st.number_input("Patient ID", min_value=1, step=1)

    col1, col2, col3 = st.columns(3)

    with col1:
        new_glucose = st.number_input("Glucose", min_value=0)
    with col2:
        new_haemoglobin = st.number_input("Haemoglobin", min_value=0)
    with col3:
        new_cholesterol = st.number_input("Cholesterol", min_value=0)

    if st.button("Update"):

        if new_glucose > 140 and new_cholesterol > 200:
            remarks = "High Diabetes & Heart Risk"
        elif new_glucose > 140:
            remarks = "Possible Diabetes Risk"
        elif new_cholesterol > 200:
            remarks = "Possible Heart Risk"
        else:
            remarks = "No Significant Risk"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE patients
            SET glucose=?, haemoglobin=?, cholesterol=?, remarks=?
            WHERE id=?
        """, (new_glucose, new_haemoglobin, new_cholesterol, remarks, update_id))

        conn.commit()
        conn.close()

        st.success("Record Updated Successfully ✏️")
