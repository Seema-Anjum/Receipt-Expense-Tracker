import json
import streamlit as st
from google import genai
from google.genai import types


def analyze_receipt(image_bytes, mime_type):

    # Get API key from Streamlit secrets
    api_key = st.secrets["GEMINI_API_KEY"]

    # Create Gemini client
    client = genai.Client(
        api_key=api_key
    )

    prompt = """
    Analyze this receipt carefully.

    Extract the following information:

    1. Every purchased item
    2. Quantity
    3. Unit price
    4. Item total
    5. Subtotal
    6. Tax
    7. Discount
    8. Final total

    Return ONLY valid JSON using exactly this structure:

    {
        "items": [
            {
                "name": "item name",
                "quantity": 1,
                "unit_price": 0,
                "total": 0
            }
        ],
        "subtotal": 0,
        "tax": 0,
        "discount": 0,
        "total": 0
    }

    Rules:

    - Do not invent values.
    - If a value cannot be identified, use null.
    - Carefully read all numbers.
    - Preserve the actual values from the receipt.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",

        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            ),
            prompt
        ],

        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)