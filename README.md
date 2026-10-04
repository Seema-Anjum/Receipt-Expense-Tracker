# 🧾 Receipt & Expense Tracker

An AI-powered receipt and expense splitting application built with **Streamlit** and **Google Gemini Vision**.

Upload a receipt image and the application automatically extracts the purchased items, prices, subtotal, tax, discount, and final total. The bill can then be split equally or item-by-item, with payments rounded to **whole Indian rupees** and reconciled so the final amounts always match the bill.

The application can also send the final bill breakdown directly to **Telegram**.

---

## 🚀 Features

### 📸 Receipt Upload

Upload a receipt in:

* JPG
* JPEG
* PNG

The uploaded receipt is analyzed using Gemini Vision.

### 🤖 AI Receipt Extraction

Google Gemini extracts structured information from the receipt:

* Item name
* Quantity
* Unit price
* Item total
* Subtotal
* Tax
* Discount
* Final total

The AI response is returned as structured JSON.

### 🧮 Receipt Verification

The application independently calculates:

```text
Expected Total = Subtotal + Tax - Discount
```

It then compares the calculated value with the total detected by Gemini.

This helps detect possible extraction errors.

### 👥 Equal Bill Splitting

The bill can be divided equally among multiple people.

The application uses whole rupees instead of paise.

For example:

```text
₹100 ÷ 3

Person 1 → ₹34
Person 2 → ₹33
Person 3 → ₹33

Total → ₹100
```

The amounts always add up exactly to the bill.

### 🍕 Item-Wise Bill Splitting

Users can enter people's names and assign individual receipt items to them.

Example:

```text
Pizza  → Seema
Burger → Rahul
Drinks → Priya
```

The application calculates how much each person needs to pay.

The result is reconciled to whole rupees so the final payment total matches the assigned item total.

### 📱 Telegram Notifications

After calculating the bill, the user can send the payment breakdown to a Telegram chat using a Telegram Bot.

Example:

```text
🧾 BILL SPLIT

💰 Total: ₹100

👥 PAYMENT BREAKDOWN

• Seema: ₹34
• Rahul: ₹33
• Priya: ₹33

✅ Amounts rounded to whole rupees.
```

---

# 🏗️ Architecture

```text
                  ┌─────────────────┐
                  │  Receipt Image  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Gemini Vision  │
                  │  AI Extraction  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Structured JSON │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Python Validate │
                  │ & Calculate     │
                  └────────┬────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        ┌──────────────┐      ┌──────────────┐
        │ Equal Split  │      │ Item Split   │
        └──────┬───────┘      └──────┬───────┘
               │                     │
               └──────────┬──────────┘
                          ▼
                 ┌──────────────────┐
                 │ Whole ₹ Amounts  │
                 │ Exact Reconcile  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Telegram Bot     │
                 └──────────────────┘
```

---

# 📁 Project Structure

```text
receipt-expense-tracker/
│
├── app.py
│
├── gemini_service.py
│
├── bill_splitter.py
│
├── telegram_service.py
│
├── requirements.txt
│
├── README.md
│
└── .streamlit/
    │
    └── secrets.toml
```

---

# 🛠️ Technologies Used

| Technology          | Purpose                    |
| ------------------- | -------------------------- |
| Python              | Application logic          |
| Streamlit           | Web interface              |
| Google Gemini       | AI receipt analysis        |
| Google GenAI SDK    | Gemini API integration     |
| Pillow              | Image processing           |
| python-telegram-bot | Telegram messaging         |
| Telegram Bot API    | Sending bill notifications |

---

# 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/receipt-expense-tracker.git
```

Move into the project:

```bash
cd receipt-expense-tracker
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔑 API Configuration

The application uses Streamlit secrets instead of storing API keys directly in Python files.

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"

TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"

TELEGRAM_CHAT_ID = "your_telegram_chat_id"
```

### ⚠️ Security

Never commit:

```text
.streamlit/secrets.toml
```

to GitHub.

Add this to `.gitignore`:

```gitignore
.streamlit/secrets.toml
__pycache__/
*.pyc
venv/
.env
```

---

# 🤖 Setting Up Gemini

Create a Gemini API key and add it to:

```text
.streamlit/secrets.toml
```

Example:

```toml
GEMINI_API_KEY = "YOUR_KEY"
```

The application uses Gemini to analyze the uploaded receipt image.

The AI is responsible for **extraction**, while Python is responsible for **calculation and validation**.

---

# 📱 Setting Up Telegram

## 1. Create a Telegram Bot

Open Telegram and search for:

```text
@BotFather
```

Send:

```text
/newbot
```

Follow the instructions.

BotFather will provide a bot token.

Example:

```text
123456789:ABCxxxxxxxxxxxxxxxx
```

Add it to:

```toml
TELEGRAM_BOT_TOKEN = "your_bot_token"
```

---

## 2. Start the Bot

Open your newly created Telegram bot.

Press:

```text
Start
```

Send a message such as:

```text
hello
```

---

## 3. Get the Chat ID

Open:

```text
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Find:

```json
"chat": {
    "id": 123456789
}
```

Use that number as:

```toml
TELEGRAM_CHAT_ID = "123456789"
```

Never share your bot token publicly.

---

# ▶️ Running the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The application will open in your browser.

---

# 🔄 Application Workflow

### Step 1 — Upload Receipt

Upload a receipt image.

### Step 2 — Analyze Receipt

Click:

```text
🔍 Analyze Receipt
```

Gemini analyzes the image.

### Step 3 — Review Extracted Data

The application displays:

* Items
* Prices
* Subtotal
* Tax
* Discount
* Final total

### Step 4 — Verify Receipt

Python calculates:

```text
Subtotal + Tax - Discount
```

and compares it with the extracted final total.

### Step 5 — Choose Split Method

You can either:

```text
👥 Equal Split
```

or:

```text
🍕 Item-Wise Split
```

### Step 6 — Round Amounts

The application works with whole rupees.

Example:

```text
₹100 / 3

₹34
₹33
₹33
```

### Step 7 — Send to Telegram

Click:

```text
📨 Send to Telegram
```

The final breakdown is sent to your Telegram chat.

---

# 🧠 Design Philosophy

A key design decision in this project is:

> **Gemini extracts. Python decides.**

Gemini is used for understanding the receipt image.

Python handles:

* Mathematical calculations
* Receipt verification
* Bill splitting
* Rounding
* Reconciliation

This prevents the AI from being responsible for financial calculations.

---

# 💰 Whole-Rupee Reconciliation

Normal rounding can create incorrect totals.

For example:

```text
₹100 / 3 = ₹33.33
```

Simply rounding every person's share gives:

```text
₹33 + ₹33 + ₹33 = ₹99 ❌
```

Instead, the application distributes the remaining rupee:

```text
₹34 + ₹33 + ₹33 = ₹100 ✅
```

For item-wise splitting, the application also reconciles rounded values so that the final amounts match the calculated total.

---

# 🧩 Main Components

## `app.py`

Responsible for:

* Streamlit UI
* Receipt upload
* Displaying extracted information
* Receipt verification
* Equal splitting
* Item-wise splitting
* Telegram interaction
* Session state

---

## `gemini_service.py`

Responsible for:

* Connecting to Gemini
* Sending receipt images
* Providing extraction instructions
* Receiving structured JSON
* Parsing the Gemini response

---

## `bill_splitter.py`

Responsible for:

* Equal bill splitting
* Item-wise splitting
* Whole-rupee rounding
* Exact total reconciliation

---

## `telegram_service.py`

Responsible for:

* Connecting to Telegram
* Sending bill messages
* Keeping Telegram-specific logic separate from the UI

---

# 📋 Example Receipt JSON

Gemini produces data similar to:

```json
{
    "items": [
        {
            "name": "Pizza",
            "quantity": 1,
            "unit_price": 250,
            "total": 250
        },
        {
            "name": "Burger",
            "quantity": 2,
            "unit_price": 120,
            "total": 240
        }
    ],
    "subtotal": 490,
    "tax": 49,
    "discount": 0,
    "total": 539
}
```

---

# 🧪 Example

Suppose the receipt total is:

```text
₹539
```

Three people split it equally.

The application calculates:

```text
Person 1 → ₹180
Person 2 → ₹180
Person 3 → ₹179

Total → ₹539
```

The Telegram message becomes:

```text
🧾 BILL SPLIT

💰 Total: ₹539

👥 PAYMENT BREAKDOWN

• Person 1: ₹180
• Person 2: ₹180
• Person 3: ₹179

✅ Amounts rounded to whole rupees.
```

---

# 🔐 Security Considerations

Never expose:

* Gemini API key
* Telegram bot token
* Telegram chat ID

Do not hard-code credentials in Python.

Use:

```text
.streamlit/secrets.toml
```

and keep the file out of Git.

---

# 🚧 Future Improvements

Possible future features:

* 👤 Add custom names for equal split
* 💸 Tip calculation
* 🧾 Multiple receipt support
* 📊 Expense history
* 📅 Monthly expense analytics
* 💾 Database storage
* 👥 Group expense tracking
* 🔗 Shareable bill links
* 📱 WhatsApp integration
* 📧 Email receipts
* 📈 Spending dashboards
* 🔐 User authentication
* ☁️ Cloud deployment
* 🧠 Better receipt confidence scoring
* ✏️ Manual correction of extracted items

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Generative AI
* Vision AI
* Gemini API
* Structured JSON generation
* Prompt engineering
* Python
* Streamlit
* API integration
* Telegram Bot API
* Session state
* Financial calculation logic
* Error handling
* Modular application architecture

---

# 👩‍💻 Author

**Shaik Seema Anjum**

Built as an AI-powered expense management project combining:

```text
AI + Python + Streamlit + Telegram
```

