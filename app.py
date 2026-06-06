import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

st.title("Patient Health Risk Assessment System")
st.caption("Health Prediction Application using Python and SQLite")

# -----------------------------
# Patient Entry Form
# -----------------------------

name = st.text_input("Full Name")
from datetime import date

dob = st.date_input(
    "Date of Birth",
    value=date(2004, 1, 1),
    min_value=date(1950, 1, 1),
    max_value=date.today()
)
email = st.text_input("Email Address")
glucose = st.number_input(
    "Glucose",
    min_value=0,
    max_value=500,
    step=1
)

haemoglobin = st.number_input(
    "Haemoglobin",
    min_value=0,
    max_value=30,
    step=1
)

cholesterol = st.number_input(
    "Cholesterol",
    min_value=0,
    max_value=500,
    step=1
)
if st.button("Submit"):

    # Validation
    if "@" not in email or "." not in email:
        st.error("Please enter a valid email address")

    elif dob > date.today():
        st.error("Date of Birth cannot be in the future")

    else:

        # Prediction Logic
        if glucose > 140 and cholesterol > 200:
            remarks = "High Diabetes and Cardiovascular Risk"

        elif glucose > 140:
            remarks = "Potential Diabetes Risk"

        elif cholesterol > 200:
            remarks = "Potential Heart Disease Risk"

        else:
            remarks = "No Significant Risk Detected"

        conn = sqlite3.connect("patients.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients
        (name,dob,email,glucose,haemoglobin,cholesterol,remarks)
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            name,
            str(dob),
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()
        conn.close()

        st.success("Patient Record Saved Successfully")
        st.write("Prediction Result:", remarks)

# -----------------------------
# Display Records
# -----------------------------

st.header("Patient Records")

conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM patients")

records = cursor.fetchall()

conn.close()

df = pd.DataFrame(
    records,
    columns=[
        "Patient ID",
        "Full Name",
        "Date of Birth",
        "Email",
        "Glucose",
        "Haemoglobin",
        "Cholesterol",
        "Health Remarks"
    ]
)

st.dataframe(df, use_container_width=True)

# -----------------------------
# Delete Record
# -----------------------------

st.header("Delete Patient Record")

delete_id = st.number_input(
    "Enter Patient ID",
    min_value=1,
    step=1
)

if st.button("Delete"):

    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (delete_id,)
    )

    conn.commit()
    conn.close()

    st.success("Patient Record Deleted Successfully")


    st.header("Update Patient Record")

update_id = st.number_input(
    "Enter Patient ID to Update",
    min_value=1,
    step=1,
    key="update_id"
)

new_glucose = st.number_input(
    "New Glucose Value",
    min_value=0.0,
    key="new_glucose"
)

new_haemoglobin = st.number_input(
    "New Haemoglobin Value",
    min_value=0.0,
    key="new_haemoglobin"
)

new_cholesterol = st.number_input(
    "New Cholesterol Value",
    min_value=0.0,
    key="new_cholesterol"
)

if st.button("Update Record"):

    if new_glucose > 140 and new_cholesterol > 200:
        remarks = "High Diabetes and Cardiovascular Risk"

    elif new_glucose > 140:
        remarks = "Potential Diabetes Risk"

    elif new_cholesterol > 200:
        remarks = "Potential Heart Disease Risk"

    else:
        remarks = "No Significant Risk Detected"

    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE patients
    SET glucose=?,
        haemoglobin=?,
        cholesterol=?,
        remarks=?
    WHERE id=?
    """,
    (
        new_glucose,
        new_haemoglobin,
        new_cholesterol,
        remarks,
        update_id
    ))

    conn.commit()
    conn.close()

    st.success("Patient Record Updated Successfully")