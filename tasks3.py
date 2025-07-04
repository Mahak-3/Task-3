
import nltk
from nltk.chat.util import Chat, reflections
import datetime
import random
import re
from collections import Counter

nltk.download('punkt')

# --- Café Elements ---
coffee_quotes = [
    "🍩 Start your day with coffee and kindness.",
    "☕ Behind every great day is a great coffee."
]

specials = [
    "🎉 Today's Special: Buy 1 Latte, Get 1 Donut Free!",
    "🍯 Honey Muffin at just ₹50 today only!",
    "🥤 Free Iced Tea with every Muffin!"
]

menu_prices = {
    "coffee": 100,
    "cappuccino": 150,
    "tea": 80,
    "latte": 140,
    "donut": 60,
    "muffin": 70
}

order = []
seating_preference = ""
awaiting_more_order = False

# --- Helper Functions ---
def get_time():
    return datetime.datetime.now().strftime('%I:%M %p')

def get_date():
    return datetime.datetime.now().strftime('%B %d, %Y')

def print_welcome_banner():
    print("="*50)
    print("☕  WELCOME TO CHAT CAFÉ  ☕".center(50))
    print("="*50)

def ask_user_name():
    name = input("Before we start, may I know your name? 😊\nYou: ")
    print(f"\nNice to meet you, {name.title()}! 🧋 What would you like to order today?\n")
    return name

def get_menu():
    menu = "📋 Here's our menu with prices (in ₹):\n"
    for item, price in menu_prices.items():
        menu += f"🍴 {item.title()} : ₹{price}\n"
    menu += "\nWould you like to order something, Sir/Mam? 😊"
    return menu

def handle_order(user_input):
    global awaiting_more_order
    added = []
    for item in menu_prices:
        if item in user_input:
            order.append(item)
            added.append(f"{item.title()} (₹{menu_prices[item]})")
    if added:
        awaiting_more_order = True
        return "✅ Added to your order: " + ", ".join(added) + "\n📝 Would you like to add anything else to your order? (yes/no)"
    return "❌ Sorry, I didn't catch the item. Please try again from the menu."

def show_total():
    if not order:
        return "🧾 You haven't ordered anything yet."
    counted = Counter(order)
    total = sum(menu_prices[item] * qty for item, qty in counted.items())
    items = '\n'.join([f"{item.title()} x{qty} = ₹{menu_prices[item]*qty}" for item, qty in counted.items()])
    return f"🧾 Here's your order summary:\n{items}\n\n💰 Total bill: ₹{total}"

def save_receipt(name):
    if not order:
        return
    filename = f"{name}_receipt.txt"
    with open(filename, "w", encoding="utf-8") as f:  # ✅ Fixed encoding
        f.write(f"Chat Café Receipt for {name.title()}\n")
        f.write(f"Date: {get_date()}, Time: {get_time()}\n\n")
        f.write(show_total())
    print(f"\n📄 Your receipt has been saved as {filename}")

# --- Smart Response Handler ---
def smart_response(user_input, name):
    global seating_preference, awaiting_more_order

    user_input = user_input.lower().strip()

    # Handle yes/no for more orders
    if awaiting_more_order:
        awaiting_more_order = False
        if user_input in ["yes", "y", "sure", "ok", "ya"]:
            return "Great! 😊 Please type your next item."
        elif user_input in ["no", "n", "nope", "nah"]:
            return "Alright! ✅ You can type 'total' to see your bill or ask for a seat. 🪑"
        else:
            awaiting_more_order = True
            return "Please reply with 'yes' or 'no'. 😊"

    if re.search(r'\b(hi|hello|hey)\b', user_input):
        return f"Hey {name.title()}! 👋 What can I get for you today?"

    elif re.search(r'\b(menu|show menu|see menu)\b', user_input):
        return get_menu()

    elif re.search(r'\b(total|bill|amount)\b', user_input):
        return show_total()

    elif re.search(r'\b(coffee|tea|latte|donut|cappuccino|muffin)\b', user_input):
        return handle_order(user_input)

    elif re.search(r'\b(time)\b', user_input):
        return f"🕒 The current café time is {get_time()}."

    elif re.search(r'\b(date)\b', user_input):
        return f"📅 Today's date is {get_date()}."

    elif re.search(r'\b(seating|table)\b', user_input):
        return "🪑 Would you prefer *indoor* or *outdoor* seating?"

    elif re.search(r'\b(indoor)\b', user_input):
        seating_preference = "indoor"
        return "🪑 Indoor table reserved for you! Enjoy the cozy vibes."

    elif re.search(r'\b(outdoor)\b', user_input):
        seating_preference = "outdoor"
        return "🌿 Outdoor seating arranged! Enjoy the fresh air and sunshine."

    elif re.search(r'\b(wifi|internet)\b', user_input):
        return "📶 Yes, we offer free Wi-Fi! Just ask the barista for the password."

    elif re.search(r'\b(thank you|thanks)\b', user_input):
        return "You're most welcome! 😊 Anything else you'd like?"

    elif re.search(r'\b(bye|exit|quit)\b', user_input):
        save_receipt(name)
        if seating_preference:
            return f"Goodbye {name.title()}! 🪑 Your {seating_preference} table will miss you. Come back soon! 🌟"
        else:
            return f"Goodbye {name.title()}! ☕ Hope to see you again at Chat Café soon. 🌟"

    else:
        return "Hmm... 🤔 I didn't get that. Want to order something or check the menu?"

# --- Main Chat Loop ---
def start_chat():
    print_welcome_banner()
    print(random.choice(coffee_quotes))
    print(random.choice(specials))
    print()

    name = ask_user_name()

    print("💬 You can say things like 'I want a cappuccino', 'Show me the menu', 'Indoor seating', or 'Total'.")
    print("Type 'bye' anytime to exit.\n")

    while True:
        user_input = input("You: ")
        response = smart_response(user_input, name)
        print("CafeBot:", response)
        if response.startswith("Goodbye"):
            break

# --- Run the ChatBot ---
if __name__ == "__main__":
    start_chat()
