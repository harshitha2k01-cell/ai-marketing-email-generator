import pandas as pd
from transformers import pipeline

# Load model
generator = pipeline("text-generation", model="distilgpt2")

# ===== FIX CSV LOADING =====
df = pd.read_csv("data.csv", header=None)

# Split single column into multiple columns
df = df[0].str.split(",", expand=True)

# Assign proper column names
df.columns = ["Name", "Age", "Interest", "Last_Purchase", "Location"]

# Remove header row (first row)
df = df.drop(0)

# Reset index
df = df.reset_index(drop=True)

# ===== EMAIL GENERATION FUNCTION =====
def generate_email(name, interest, purchase):
    prompt = f"""
Write 3 short lines for a marketing message about {interest}.
Keep it simple, clear, and relevant.
"""

    result = generator(
        prompt,
        max_new_tokens=40,
        temperature=0.6,
        repetition_penalty=1.5
    )

    text = result[0]['generated_text'].replace(prompt, "").strip()

    # ✅ Proper structured email (FIXED)
    email = f"""Hi {name},

Based on your interest in {interest}, we thought you would love our latest products similar to your recent purchase ({purchase}).

{text}

Shop now and upgrade your experience!

Best regards,  
Your Brand Team
"""

    return email.strip()


# ===== RUN FOR ALL CUSTOMERS =====
print("Starting email generation...\n")

emails_data = []

for index, row in df.iterrows():
    email = generate_email(row['Name'], row['Interest'], row['Last_Purchase'])

    emails_data.append({
        "Name": row['Name'],
        "Interest": row['Interest'],
        "Last_Purchase": row['Last_Purchase'],
        "Generated_Email": email
    })

    print("\n---------------------------")
    print(f"Email for {row['Name']}:\n")
    print(email)

# ===== SAVE OUTPUT =====
output_df = pd.DataFrame(emails_data)
output_df.to_csv("generated_emails.csv", index=False, encoding="utf-8-sig")

print("\n✅ Emails saved to generated_emails.csv")