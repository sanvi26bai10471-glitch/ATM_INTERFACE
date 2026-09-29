import sys
import datetime

# Centralized User Accounts Database (Simulated In-Memory Storage)
ACCOUNTS = {
    "1001": {
        "name": "Sanvi Shrivastava",
        "reg_no": "26BAI10471",
        "pin": "1234",
        "balance": 150000.0,
        "history": []
    },
    "1002": {
        "name": "Rahul Sharma",
        "reg_no": "26BAS10088",
        "pin": "4321",
        "balance": 85000.0,
        "history": []
    }
}

CURRENT_USER = None

def log_transaction(user_id, trans_type, amount, updated_balance):
    """Logs transaction with timestamp to the specific user's history."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {trans_type}: Rs.{amount:.2f} | Balance: Rs.{updated_balance:.2f}"
    ACCOUNTS[user_id]["history"].append(entry)

def authenticate_user():
    """Universal login supporting any account ID and PIN."""
    global CURRENT_USER
    print("\n" + "=" * 45)
    print("           USER AUTHENTICATION               ")
    print("=" * 45)
    
    attempts = 3
    while attempts > 0:
        acc_id = input("Enter Account Number / User ID (e.g., 1001): ").strip()
        pin = input("Enter 4-Digit Security PIN: ").strip()
        
        if acc_id in ACCOUNTS and ACCOUNTS[acc_id]["pin"] == pin:
            CURRENT_USER = acc_id
            user_info = ACCOUNTS[acc_id]
            print(f"\nLogin Successful! Welcome, {user_info['name']}.")
            return True
        else:
            attempts -= 1
            print(f"Invalid Account ID or PIN. Attempts remaining: {attempts}\n")
            
    print("Security Lockout: Maximum authentication attempts exceeded.")
    return False

def chk_balance():
    """Displays current account balance for active user."""
    user = ACCOUNTS[CURRENT_USER]
    print("\n" + "=" * 45)
    print("              ACCOUNT BALANCE                ")
    print("=" * 45)
    print(f" Account Holder : {user['name']}")
    print(f" Reg / User ID  : {user['reg_no']}")
    print(f" Available Funds: Rs. {user['balance']:.2f}")
    print("=" * 45)

def withdraw():
    """Handles cash withdrawal with validation for active user."""
    user = ACCOUNTS[CURRENT_USER]
    print("\n---------------- CASH WITHDRAWAL ----------------")
    try:
        amt = float(input("Enter amount to withdraw: Rs. "))
        if amt <= 0:
            print("Error: Amount must be greater than 0.")
        elif amt > user["balance"]:
            print(f"Transaction Declined: Insufficient funds! Available: Rs.{user['balance']:.2f}")
        else:
            user["balance"] -= amt
            log_transaction(CURRENT_USER, "WITHDRAWAL", amt, user["balance"])
            print(f"Success: Rs. {amt:.2f} withdrawn.")
            print(f"Updated Balance: Rs. {user['balance']:.2f}")
    except ValueError:
        print("Invalid Input! Please enter a valid numerical value.")

def deposit():
    """Handles cash deposit for active user."""
    user = ACCOUNTS[CURRENT_USER]
    print("\n------------------ CASH DEPOSIT ------------------")
    try:
        amt = float(input("Enter amount to deposit: Rs. "))
        if amt <= 0:
            print("Error: Amount must be greater than 0.")
        else:
            user["balance"] += amt
            log_transaction(CURRENT_USER, "DEPOSIT", amt, user["balance"])
            print(f"Success: Rs. {amt:.2f} deposited.")
            print(f"Updated Balance: Rs. {user['balance']:.2f}")
    except ValueError:
        print("Invalid Input! Please enter a valid numerical value.")

def view_statement():
    """Displays user-specific transaction history."""
    user = ACCOUNTS[CURRENT_USER]
    print("\n================ MINI-STATEMENT ================")
    print(f" Account Holder: {user['name']}")
    if not user["history"]:
        print("No transactions performed during this session.")
    else:
        for idx, item in enumerate(user["history"], 1):
            print(f"{idx}. {item}")
    print("================================================")

def register_new_account():
    """Allows new users to register an account dynamically."""
    print("\n" + "=" * 45)
    print("         NEW USER REGISTRATION              ")
    print("=" * 45)
    new_id = str(len(ACCOUNTS) + 1001)
    name = input("Enter Full Name: ").strip()
    reg_no = input("Enter Registration No / ID: ").strip()
    pin = input("Set a 4-digit PIN: ").strip()
    try:
        init_balance = float(input("Enter Initial Deposit: Rs. "))
    except ValueError:
        init_balance = 5000.0
        print("Invalid deposit amount entered. Defaulting to Rs. 5000.00")

    ACCOUNTS[new_id] = {
        "name": name,
        "reg_no": reg_no,
        "pin": pin,
        "balance": init_balance,
        "history": []
    }
    print(f"\nAccount Created Successfully! Your Account Number is: {new_id}")

def display_front_page():
    print("=" * 50)
    print("       UNIVERSAL ATM INTERFACE SYSTEM           ")
    print("=" * 50)

def main():
    display_front_page()
    
    while True:
        print("\n1. Login to Existing Account")
        print("2. Register New Account")
        print("3. Exit Application")
        init_choice = input("Select an option (1-3): ").strip()
        
        if init_choice == '1':
            if authenticate_user():
                break
        elif init_choice == '2':
            register_new_account()
        elif init_choice == '3':
            print("\nThank you for using Universal ATM. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

    while True:
        user_name = ACCOUNTS[CURRENT_USER]["name"]
        print(f"\n+------------ MAIN MENU ({user_name}) ------------+")
        print("| 1. Check Balance                               |")
        print("| 2. Withdraw Money                              |")
        print("| 3. Deposit Money                               |")
        print("| 4. View Mini-Statement                         |")
        print("| 5. Logout & Exit                               |")
        print("+------------------------------------------------+")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            chk_balance()
        elif choice == '2':
            withdraw()
        elif choice == '3':
            deposit()
        elif choice == '4':
            view_statement()
        elif choice == '5':
            print(f"\nGoodbye {user_name}! Session ended securely.")
            break
        else:
            print("Invalid Choice! Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
