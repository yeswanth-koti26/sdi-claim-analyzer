import openai
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("ORG_ID")

# 🔄 Retry-safe GPT wrapper
def ask_gpt(system_prompt, user_prompt, model="gpt-4", temperature=0.2, max_tokens=1500):
    retries = 3
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️ GPT call failed (attempt {attempt + 1}): {e}")
            time.sleep(2)
    return ""

# 🧠 Document classification
def classify_document_fulltext(text):
    prompt = f"""
You are an AI document classifier. Based on the full document content below, identify the document type. Respond with ONLY one of the following categories:

- tenant_ledger
- lease_addendum
- lease_agreement
- notification_to_tenant
- invoice
- claim_evaluation_report
- move_out_statement
- other

Document content:
{text[:1500]}
"""
    response = ask_gpt(
        system_prompt="You classify housing claim documents based on content.",
        user_prompt=prompt,
        max_tokens=100
    )
    return response.lower().strip().replace('"', '').replace(".", "")

# 💰 GPT-based charge extraction with policy tagging
def extract_charges_fulltext(text):
    prompt = f"""
You are a claims analyst assistant. Extract ALL financial charges listed in the following move-out or ledger document. Each line item should include:

- "description": Short description of the charge.
- "amount": Number only, no $ or commas.
- "category": One of [rent, cleaning, utilities, rekey, lease break fee, landscaping, legal, admin, sdi premium, animal fee, coordination fee, late fee, other].
- "policy_covered": true if the charge is covered under the SDI policy rules below, false otherwise.

SDI Policy Guidelines:
- ✅ Covered: excessive cleaning, unpaid rent (max 1 month), rekey, landscaping (up to $500), unpaid utilities, lease break (max 1 month)
- ❌ Not Covered: animal fees, SDI premium, admin fees, late fees, legal fees, normal wear, tenant services, filter program, coordination fees

Respond ONLY with a valid JSON list like this:
[
  {{ "description": "Move-out cleaning", "amount": 150.00, "category": "cleaning", "policy_covered": true }},
  {{ "description": "Animal Fee", "amount": 70.00, "category": "animal fee", "policy_covered": false }}
]

Here is the extracted document text:
{text[:3500]}
"""
    response = ask_gpt(
        system_prompt="You extract charges and classify them under SDI rules.",
        user_prompt=prompt,
        max_tokens=1800
    )

    try:
        charges = json.loads(response)
        if isinstance(charges, list):
            return charges
        else:
            print("⚠️ GPT did not return a list.")
            return []
    except Exception as e:
        print("⚠️ Failed to parse GPT charge response:", e)
        print("🔍 Raw response was:\n", response)
        return []
