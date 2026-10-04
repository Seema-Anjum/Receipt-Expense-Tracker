import streamlit as st

from gemini_service import analyze_receipt
from telegram_service import send_telegram

from bill_splitter import (
    split_equally,
    split_by_items
)


# =================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Receipt Expense Tracker",
    page_icon="🧾",
    layout="centered"
)


# ==================================================
# TITLE
# ==================================================

st.title("🧾 Receipt & Expense Tracker")

st.write(
    "Upload a receipt and let Gemini extract "
    "the bill details automatically."
)


# ==================================================
# SESSION STATE
# ==================================================

if "receipt" not in st.session_state:
    st.session_state.receipt = None

if "equal_split" not in st.session_state:
    st.session_state.equal_split = None

if "item_split" not in st.session_state:
    st.session_state.item_split = None


# ==================================================
# TELEGRAM MESSAGE FORMATTER
# ==================================================

def create_bill_message(total, people_amounts):

    message = "🧾 BILL SPLIT\n\n"

    message += f"💰 Total: ₹{round(total)}\n\n"

    message += "👥 PAYMENT BREAKDOWN\n\n"

    for person, amount in people_amounts.items():

        message += (
            f"• {person}: ₹{round(amount)}\n"
        )

    message += (
        "\n✅ Amounts rounded to whole rupees."
    )

    return message


# ==================================================
# UPLOAD RECEIPT
# ==================================================

uploaded_file = st.file_uploader(
    "Upload your receipt",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# ==================================================
# ANALYZE RECEIPT
# ==================================================

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded Receipt",
        use_container_width=True
    )

    if st.button("🔍 Analyze Receipt"):

        with st.spinner(
            "Reading your receipt..."
        ):

            try:

                image_bytes = uploaded_file.getvalue()

                mime_type = uploaded_file.type

                receipt = analyze_receipt(
                    image_bytes,
                    mime_type
                )

                st.session_state.receipt = receipt

                # Clear old split results
                st.session_state.equal_split = None
                st.session_state.item_split = None

                st.success(
                    "✅ Receipt analyzed successfully!"
                )

            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {e}"
                )


# ==================================================
# DISPLAY RECEIPT
# ==================================================

if st.session_state.receipt:

    receipt = st.session_state.receipt

    st.divider()

    st.subheader(
        "📋 Extracted Receipt"
    )

    st.json(receipt)


    # ==================================================
    # EXTRACT VALUES
    # ==================================================

    items = receipt.get(
        "items",
        []
    )

    calculated_items_total = sum(
        item.get("total", 0) or 0
        for item in items
    )

    subtotal = (
        receipt.get("subtotal")
        or calculated_items_total
    )

    tax = (
        receipt.get("tax")
        or 0
    )

    discount = (
        receipt.get("discount")
        or 0
    )

    gemini_total = receipt.get(
        "total"
    )


    # ==================================================
    # RECEIPT SUMMARY
    # ==================================================

    st.subheader(
        "💵 Receipt Summary"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Items Total",
            f"₹{round(calculated_items_total)}"
        )

    with col2:

        st.metric(
            "Subtotal",
            f"₹{round(subtotal)}"
        )


    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            "Tax",
            f"₹{round(tax)}"
        )

    with col4:

        st.metric(
            "Discount",
            f"₹{round(discount)}"
        )


    if gemini_total is not None:

        st.metric(
            "Final Total",
            f"₹{round(gemini_total)}"
        )


    # ==================================================
    # VERIFICATION
    # ==================================================

    st.subheader(
        "🧮 Receipt Verification"
    )

    if gemini_total is not None:

        expected_total = (
            subtotal
            + tax
            - discount
        )

        difference = abs(
            expected_total
            - gemini_total
        )

        st.write(
            f"**Expected total:** "
            f"₹{round(expected_total)}"
        )

        st.write(
            f"**Receipt total:** "
            f"₹{round(gemini_total)}"
        )

        if difference < 0.01:

            st.success(
                "✅ Receipt total verified!"
            )

        else:

            st.warning(
                f"⚠️ Total mismatch: "
                f"₹{difference:.2f}"
            )

    else:

        st.warning(
            "⚠️ Receipt total could not "
            "be detected."
        )


    # ==================================================
    # EQUAL SPLIT
    # ==================================================

    st.divider()

    st.subheader(
        "👥 Split the Bill Equally"
    )

    number_of_people = st.number_input(
        "How many people?",
        min_value=1,
        max_value=50,
        value=2,
        step=1
    )


    if st.button(
        "💰 Split Bill Equally"
    ):

        if gemini_total is None:

            st.error(
                "❌ Receipt total is not available."
            )

        else:

            result = split_equally(
                gemini_total,
                number_of_people
            )

            # Create person names
            people_amounts = {}

            for index, amount in enumerate(
                result["amounts"],
                start=1
            ):

                people_amounts[
                    f"Person {index}"
                ] = amount

            # Save result
            st.session_state.equal_split = (
                people_amounts
            )


    # ==================================================
    # DISPLAY EQUAL SPLIT
    # ==================================================

    if st.session_state.equal_split:

        st.subheader(
            "💰 Equal Split Result"
        )

        total = sum(
            st.session_state.equal_split.values()
        )

        for person, amount in (
            st.session_state.equal_split.items()
        ):

            st.write(
                f"**{person}** → ₹{amount}"
            )

        st.write(
            f"**Total:** ₹{total}"
        )

        # Telegram button
        if st.button(
            "📨 Send Equal Split to Telegram"
        ):

            message = create_bill_message(
                total,
                st.session_state.equal_split
            )

            chat_id = st.secrets[
                "TELEGRAM_CHAT_ID"
            ]

            try:

                send_telegram(
                    chat_id,
                    message
                )

                st.success(
                    "✅ Bill sent to Telegram!"
                )

            except Exception as e:

                st.error(
                    f"❌ Telegram failed: {e}"
                )


    # ==================================================
    # ITEM-WISE SPLIT
    # ==================================================

    st.divider()

    st.subheader(
        "🍕 Split by Item"
    )

    people_input = st.text_input(
        "Enter people's names separated by commas",
        placeholder="Seema, Rahul, Priya"
    )


    if people_input:

        people = [
            person.strip()
            for person in people_input.split(",")
            if person.strip()
        ]


        if people:

            st.write(
                "### Assign Items"
            )

            assignments = {}


            for index, item in enumerate(items):

                item_name = item.get(
                    "name",
                    f"Item {index + 1}"
                )

                item_total = (
                    item.get("total")
                    or 0
                )

                selected_person = st.selectbox(
                    f"{item_name} — ₹{round(item_total)}",
                    people,
                    key=f"person_{index}"
                )

                assignments[item_name] = (
                    selected_person
                )


            if st.button(
                "🍽️ Calculate Item Split"
            ):

                item_split = split_by_items(
                    items,
                    assignments
                )

                st.session_state.item_split = (
                    item_split
                )


    # ==================================================
    # DISPLAY ITEM SPLIT
    # ==================================================

    if st.session_state.item_split:

        st.subheader(
            "💰 Item Split Result"
        )

        for person, amount in (
            st.session_state.item_split.items()
        ):

            st.write(
                f"**{person}** → ₹{amount}"
            )

        item_split_total = sum(
            st.session_state.item_split.values()
        )

        st.write(
            f"**Total Assigned:** "
            f"₹{item_split_total}"
        )

        # Telegram button
        if st.button(
            "📨 Send Item Split to Telegram"
        ):

            message = create_bill_message(
                item_split_total,
                st.session_state.item_split
            )

            chat_id = st.secrets[
                "TELEGRAM_CHAT_ID"
            ]

            try:

                send_telegram(
                    chat_id,
                    message
                )

                st.success(
                    "✅ Item split sent to Telegram!"
                )

            except Exception as e:

                st.error(
                    f"❌ Telegram failed: {e}"
                )