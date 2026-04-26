import pandas as pd
import streamlit as st

st.title("📧 AI Marketing Email Generator")
st.markdown("### Generate personalized marketing emails using AI 🚀")

st.write("Upload customer data and generate personalized emails!")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


def generate_email(name, interest, purchase):
    email = f"""Hi {name},

Based on your interest in {interest}, we thought you would love products similar to your recent purchase ({purchase}).

Discover curated {interest.lower()} products designed to enhance your experience and match your lifestyle.

Shop now and unlock exclusive offers just for you!

Best regards,  
Your Brand Team
"""
    return email.strip()


# MAIN LOGIC
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ✅ HANDLE BOTH GOOD & BROKEN CSV
    if len(df.columns) == 1:
        df = df[df.columns[0]].str.split(",", expand=True)
        df.columns = ["Name", "Age", "Interest", "Last_Purchase", "Location"]
    else:
        df.columns = df.columns.str.strip()

    st.success("File uploaded successfully!")

    st.info("Click below to generate emails for all customers")

    if st.button("Generate Emails"):

        emails_data = []

        for _, row in df.iterrows():

            email = generate_email(
                row['Name'],
                row['Interest'],
                row['Last_Purchase']
            )

            # ✅ FIXED INDENTATION
            emails_data.append({
                "Name": row['Name'],
                "Subject": f"Exclusive offers for {row['Interest']} lovers!",
                "Generated_Email": email
            })

        output_df = pd.DataFrame(emails_data)

        st.dataframe(output_df)

        # Download button
        csv = output_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            "Download Emails CSV",
            csv,
            "generated_emails.csv",
            "text/csv"
        )
