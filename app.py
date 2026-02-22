import streamlit as st
import requests

st.set_page_config(page_title="MBCET Campus Pass", layout="centered")

# -------- CUSTOM CSS --------
st.markdown("""
<style>
body {
    background-color: #f4f8fb;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.1);
}
.title {
    text-align: center;
    color: #003366;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# -------- SESSION STATE --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "submitted" not in st.session_state:
    st.session_state.submitted = False


# -------- LOGIN PAGE --------
if not st.session_state.logged_in:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="title">🎓 MBCET CAMPUS PASS PORTAL</h2>', unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username == "user123" and password == "mbcet1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Incorrect username/password")

    st.markdown('</div>', unsafe_allow_html=True)


# -------- DETAILS PAGE --------
elif not st.session_state.submitted:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="title">📝 Pass Request Form</h2>', unsafe_allow_html=True)

    with st.form("pass_form"):

        name = st.text_input("👤 Full Name")
        semester = st.selectbox("📚 Semester", ["", "S1","S2","S3","S4","S5","S6","S7","S8"])
        class_name = st.text_input("🏫 Class (e.g. CS-A)")
        branch = st.text_input("🧠 Branch (e.g. CSE)")
        subject = st.text_input("📖 Subject")
        reason = st.text_area("✍ Reason for Pass")

        submit = st.form_submit_button("🚀 Submit Request")

        if submit:

            if name and semester and class_name and branch and subject and reason:

                # 🔴 REPLACE WITH YOUR GOOGLE SCRIPT URL
                script_url = "https://script.google.com/macros/s/AKfycbx_dhtd9ikZQsej2hKW79whNCIpQbXlcNHr2uUfLlW9MwQkIn_ktNQYHM9zi2spUGQkFA/exec"

                data = {
                    "name": name,
                    "semester": semester,
                    "class_name": class_name,
                    "branch": branch,
                    "subject": subject,
                    "reason": reason
                }

                try:
                    response = requests.post(script_url, json=data)

                    if response.status_code == 200:
                        st.session_state.submitted = True
                        st.rerun()
                    else:
                        st.error("Failed to send data to Google Sheets")

                except Exception as e:
                    st.error(f"Error: {e}")

            else:
                st.warning("⚠ Please fill all fields.")

    st.markdown('</div>', unsafe_allow_html=True)


# -------- SUCCESS PAGE --------
else:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="title">✅ Request Submitted Successfully</h2>', unsafe_allow_html=True)

    st.success("Your response has been recorded for approval.")
    st.info("Please check your WhatsApp for further details.")

    if st.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.session_state.submitted = False
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)