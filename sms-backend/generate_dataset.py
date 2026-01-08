import csv
import random

# --- Configuration ---
NUM_ROWS = 5000  # <--- Change this number to generate more or fewer rows
OUTPUT_FILE = 'dataset.csv' # <--- This will be the name of your final downloadable file

# --- Templates for each category ---

# Personal messages are often casual, referencing plans, or simple check-ins.
personal_templates = [
    "Hey, are we still on for {event} {day}?",
    "Can you pick up some {item} on your way home?",
    "lol that's hilarious 😂",
    "Just reached {place}. Where are you?",
    "Running late, be there in {number} mins.",
    "Did you see that movie last night? Was amazing!",
    "Happy Birthday! Hope you have a great day 🎉",
    "What time should I come over?",
    "Thanks for yesterday, it was a lot of fun!",
    "How's your mom doing?",
    "I'll call you back in a bit, in a meeting right now.",
    "Don't forget to take out the trash.",
    "Let's catch up this weekend. Are you free on Saturday?",
]

# Transactional messages are factual and related to user actions (purchases, OTPs, etc.).
transactional_templates = [
    "Your OTP for {service} is {otp}. It is valid for {number} minutes. Do not share it with anyone.",
    "Thank you for your payment of Rs. {amount} at {merchant}.",
    "Your order #{order_id} from {merchant} has been shipped. Track here: {link}",
    "Rs. {amount} has been debited from your account XX{account_num} for a purchase at {merchant}.",
    "Rs. {amount} has been credited to your account XX{account_num}.",
    "Your {service} subscription has been renewed for Rs. {amount}.",
    "Reminder: Your credit card payment of Rs. {amount} is due on {date}.",
    "Your package from {merchant} is out for delivery today.",
    "Account Alert: A login from a new device was detected at {time}. If this wasn't you, please secure your account.",
]

# Promotional messages are marketing communications from businesses.
promotional_templates = [
    "FLASH SALE! Get {discount}% off on all {product_category} at {brand}. Use code {promo_code}. Shop now: {link}",
    "Exclusive Offer: Get a flat {discount}% discount on your next order from {brand}. T&C apply.",
    "Hey! We miss you. Here's a Rs. {amount} voucher just for you. Use code {promo_code}. Valid till {date}.",
    "New arrivals are here! Explore the latest collection at {brand}. Visit {link}",
    "Book your tickets for the {event} now and get an early bird discount of {discount}%!",
    "Upgrade your plan and get 2x data for the same price. Offer for {brand} users only.",
    "Your cart is waiting! Complete your purchase now and get free shipping. {link}",
]

# Spam messages often create false urgency, offer unrealistic prizes, or are unsolicited.
spam_templates = [
    "Congratulations! You've won a Rs. {amount} cash prize. To claim, click this link: {link}",
    "URGENT: Your bank account has been compromised. Verify your identity immediately at {link} to avoid suspension.",
    "Earn Rs. {amount} per day from home! No experience needed. WhatsApp us now at 98XXXXXX01.",
    "FREE {product}! You have been selected as a lucky winner. Claim your reward now before it expires: {link}",
    "Approved: Your personal loan of Rs. {amount} is ready. No documents required. Click for instant cash: {link}",
    "You have (1) new unread message from a secret admirer. Read it here: {link}",
    "Make money fast with our exclusive crypto trading signals. Guaranteed profits! Join our Telegram channel: {link}",
    "Your phone is infected with 5 viruses! Remove them now with our antivirus app: {link}",
]

# --- Placeholder data ---
placeholders = {
    "event": ["dinner", "the meeting", "the movie", "the party", "lunch"],
    "day": ["tonight", "tomorrow", "on Friday", "this weekend"],
    "item": ["milk", "bread", "vegetables", "eggs", "chicken"],
    "place": ["the cafe", "the office", "home", "Phoenix Mall"],
    "number": [str(random.randint(5, 60)) for _ in range(10)],
    "service": ["Google", "Amazon", "Netflix", "your bank", "Swiggy"],
    "otp": [str(random.randint(100000, 999999)) for _ in range(10)],
    "amount": [str(random.randrange(100, 25000, 50)) for _ in range(10)],
    "merchant": ["Amazon", "Flipkart", "Myntra", "Zomato", "BigBasket"],
    "order_id": [str(random.randint(1000000, 9999999)) for _ in range(10)],
    "link": ["http://bit.ly/xyz123", "http://tiny.cc/abc456", "http://short.url/pqr789"],
    "account_num": [str(random.randint(1000, 9999)) for _ in range(5)],
    "date": ["05-Oct-2025", "15-Nov-2025", "30-Sep-2025"],
    "time": ["09:30 AM", "08:45 PM", "12:15 PM"],
    "discount": [str(random.randint(10, 80)) for _ in range(10)],
    "product_category": ["electronics", "fashion", "groceries", "home decor"],
    "brand": ["MegaStore", "StyleUp", "FreshFoods", "UrbanLadder", "Boat"],
    "promo_code": ["SAVE50", "DEAL100", "BIGSALE", "GET20", "FREEDEL"],
    "product": ["iPhone 15", "PS5", "Holiday Package", "Smartwatch"],
}

# --- Generation Logic ---
def generate_row():
    """Generates a single row with a random message and its label."""
    category = random.choice(['personal', 'transactions', 'promotions', 'spam'])
    
    if category == 'personal':
        template = random.choice(personal_templates)
    elif category == 'transactions':
        template = random.choice(transactional_templates)
    elif category == 'promotions':
        template = random.choice(promotional_templates)
    else:  # spam
        template = random.choice(spam_templates)
        
    # Fill placeholders in the template
    message = template.format(**{k: random.choice(v) for k, v in placeholders.items()})
    
    return message, category

# --- Main script execution ---
if __name__ == "__main__":
    print(f"Generating {NUM_ROWS} rows of data...")
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write the header
        writer.writerow(['text', 'label'])
        
        # Write the data rows
        for i in range(NUM_ROWS):
            text, label = generate_row()
            writer.writerow([text, label])
            
    print(f"Successfully created '{OUTPUT_FILE}' with {NUM_ROWS} entries.")
