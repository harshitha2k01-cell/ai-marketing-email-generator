import pandas as pd
import streamlit as st
from transformers import pipeline

# Load model
generator = pipeline("text-generation", model="distilgpt2")

st.title("📧 AI Marketing Email Generator")
st.markdown("### Generate personalized marketing emails using AI 🚀")

st.write("Upload customer data and generate personalized emails!")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])


def generate_email(name, interest, purchase):
    prompt = f"""
    Write 3 short lines for a marketing message about {interest}.
    Keep it simple and engaging.
    """

    result = generator(
        prompt,
        max_new_tokens=40,
        temperature=0.6,
        repetition_penalty=1.5
    )

    text = result[0]['generated_text'].replace(prompt, "").strip()

    email = f"""Hi {name},

Based on your interest in {interest}, we thought you would love our latest products similar to your recent purchase ({purchase}).

{text}

Shop now and upgrade your experience!

Best regards,  
Your Brand Team
"""

    return email.strip()


# MAIN LOGIC
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    st.success("File uploaded successfully!")

    # 👇 ADD HERE
    st.info("Click below to generate emails for all customers")

    if st.button("Generate Emails"):

        emails_data = []

        for _, row in df.iterrows():

            email = generate_email(
                row['Name'],
                row['Interest'],
                row['Last_Purchase']
            )

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