import streamlit as st
import os

st.title("🍰 MERA CHEESECAKE BAKERY")

st.header("Order Your Favorite Cheesecake")

# Cheesecake options and prices
cheesecakes = {
    "Nutella Cheesecake": 15.0,
    "Biscoff Cheesecake": 14.0,
    "New York Cheesecake": 13.0
}

order = {}
total_price = 0.0

st.subheader("Select Quantity")
for cake, price in cheesecakes.items():
    qty = st.number_input(f"{cake} (${price} each)", min_value=0, max_value=20, value=0, step=1)
    order[cake] = qty
    total_price += qty * price

st.subheader("Delivery Options")
delivery = st.radio("Choose delivery method:", ("Pickup", "Home Delivery"))

if delivery == "Home Delivery":
    address = st.text_area("Enter your delivery address:")
else:
    address = "Pickup at store"

st.markdown("---")
st.subheader("Order Summary")

if sum(order.values()) == 0:
    st.info("Please select at least one cheesecake to order.")
else:
    st.write("### Your Order:")
    for cake, qty in order.items():
        if qty > 0:
            st.write(f"- {cake}: {qty} x ${cheesecakes[cake]} = ${qty * cheesecakes[cake]:.2f}")
    st.write(f"**Total Price:** ${total_price:.2f}")
    st.write(f"**Delivery Method:** {delivery}")
    if delivery == "Home Delivery":
        st.write(f"**Delivery Address:** {address}")

    if st.button("Place Order"):
        if delivery == "Home Delivery" and not address.strip():
            st.error("Please enter a delivery address.")
        else:
            st.success("Thank you for your order! We will contact you shortly.")

st.markdown("---")
st.header("Customer Feedback")

# File to store feedbacks
FEEDBACK_FILE = "feedbacks.txt"

# Function to load feedbacks
def load_feedbacks():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        feedbacks = f.read().strip().split("\n---\n")
        return [fb for fb in feedbacks if fb.strip()]

# Function to save feedback
def save_feedback(feedback_text):
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        if os.path.getsize(FEEDBACK_FILE) > 0:
            f.write("\n---\n")
        f.write(feedback_text.strip())

# Display all feedbacks
all_feedbacks = load_feedbacks()
if all_feedbacks:
    st.subheader("What Our Customers Say:")
    for i, fb in enumerate(reversed(all_feedbacks), 1):  # Show latest first
        st.markdown(f"**Feedback #{i}:**")
        st.write(fb)
        st.markdown("---")
else:
    st.info("No feedbacks yet. Be the first to leave a review!")

# Feedback form
with st.form("feedback_form"):
    feedback = st.text_area("Write your feedback or review here:")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if not feedback.strip():
            st.error("Please write some feedback before submitting.")
        else:
            save_feedback(feedback)
            st.success("Thank you for your feedback!")
            st.experimental_rerun()  # Refresh to show new feedback immediately
