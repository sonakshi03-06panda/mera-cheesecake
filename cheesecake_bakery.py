st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

    /* Force light mode background */
    html, body, .main, .block-container {
        background: linear-gradient(135deg, #fcefee, #f9f0ff, #e0f7fa, #fff9e6) !important;
        font-family: 'Poppins', sans-serif !important;
        color: #4a4a4a !important;
    }

    /* Override Streamlit dark mode backgrounds */
    .css-1d391kg, .css-1v3fvcr {
        background: transparent !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #f7c6c7 !important;
        color: #4a4a4a !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 8px 20px !important;
        transition: background-color 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: #f9a1a3 !important;
        color: white !important;
    }

    /* Inputs */
    .stTextInput>div>input, .stTextArea>div>textarea, .stNumberInput>div>input {
        border-radius: 10px !important;
        border: 1.5px solid #f7c6c7 !important;
        padding: 8px !important;
        font-family: 'Poppins', sans-serif !important;
        background-color: #fff !important;
        color: #4a4a4a !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #7b4f72 !important;
    }

    /* Feedback boxes */
    .feedback-box {
        background-color: #fff0f5 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
        box-shadow: 2px 2px 8px rgba(123, 79, 114, 0.15) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("MERA CHEESEEEECAKE BAKERY")

st.header("Order Your Favorite Cheesecake")

# Cheesecake options, prices, and placeholder images
cheesecakes = {
    "Nutella Cheesecake": {
        "price": 250.0,
        "img": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=80&q=80"
    },
    "Biscoff Cheesecake": {
        "price": 250.0,
        "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=80&q=80"
    },
    "New York Cheesecake": {
        "price": 200.0,
        "img": "https://images.unsplash.com/photo-1562440499-64a7a3f7a3a7?auto=format&fit=crop&w=80&q=80"
    }
}

order = {}
total_price = 0.0

st.subheader("Select Quantity")

for cake, data in cheesecakes.items():
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(data["img"], width=80, caption=None)
    with col2:
        qty = st.number_input(f"{cake} (₹{data['price']} each)", min_value=0, max_value=20, value=0, step=1, key=cake)
        order[cake] = qty
        total_price += qty * data['price']

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
            st.write(f"- {cake}: {qty} x ${cheesecakes[cake]['price']} = ${qty * cheesecakes[cake]['price']:.2f}")
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

def load_feedbacks():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        feedbacks = f.read().strip().split("\n---\n")
        return [fb for fb in feedbacks if fb.strip()]

def save_feedback(feedback_text):
    with open(FEEDBACK_FILE, "a", encoding="utf-8") as f:
        if os.path.getsize(FEEDBACK_FILE) > 0:
            f.write("\n---\n")
        f.write(feedback_text.strip())

all_feedbacks = load_feedbacks()
if all_feedbacks:
    st.subheader("What Our Customers Say:")
    for i, fb in enumerate(reversed(all_feedbacks), 1):
        st.markdown(f'<div class="feedback-box"><b>Feedback #{i}:</b><br>{fb}</div>', unsafe_allow_html=True)
else:
    st.info("No feedbacks yet. Be the first to leave a review!")

with st.form("feedback_form"):
    feedback = st.text_area("Write your feedback or review here:")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        if not feedback.strip():
            st.error("Please write some feedback before submitting.")
        else:
            save_feedback(feedback)
            st.success("Thank you for your feedback!")
            st.experimental_rerun()
