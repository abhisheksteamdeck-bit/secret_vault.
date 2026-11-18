import json

file = "secret vault data.json"

master_password = []

# Load the master password from JSON when one is not configured in the code.
try:
    with open(file, "r") as f:
        stored_data = json.load(f)

    if not master_password and isinstance(stored_data, dict):
        json_master_password = stored_data.get("master_password", "")
        if isinstance(json_master_password, str) and json_master_password.strip():
            master_password = [json_master_password.strip()]
except FileNotFoundError:
    stored_data = {}
except json.JSONDecodeError:
    print("The vault data file contains invalid JSON and cannot be loaded.")
    raise SystemExit(1)

if not isinstance(stored_data, dict):
    print("The vault data file must contain a JSON object.")
    raise SystemExit(1)

print("are you new to this software")
new_customer_check = str(input("yes/no : ")).lower().strip()

access_granted = False

if new_customer_check == "no":
    if not master_password:
        print("No master password is saved. Run the program again and answer yes to create one.")
    else:
        print("then type your master password to enter your security vault\nand you only have 3 attempts to type the right master password, or the account will get locked for the day.")

        attempts = 3

        while attempts > 0:
            master_password_check = str(input("master password : ")).strip()

            if master_password_check in master_password:
                print("access granted")
                access_granted = True
                break
            else:
                attempts -= 1
                if attempts == 0:
                    print("the account is locked")
                    break
                print("the password is wrong you have", attempts, "remaining")

elif new_customer_check == "yes":
    if master_password:
        print("A master password is already set. Answer no next time to sign in.")
    else:
        print("make a new master password")
        making_master_password = str(input("create a master password\n>>>")).strip()

        if making_master_password:
            master_password = [making_master_password]
            print("the master password is successfully made.")
            if "password" in stored_data and "username" in stored_data:
                user_data = stored_data
                user_data["master_password"] = making_master_password
            else:
                print("now type to store a password and username before we proceed to any other actions.")
                password = str(input("password to store : "))
                username = str(input("username to store : "))
                user_data = {
                    "master_password": making_master_password,
                    "password": password,
                    "username": username
                }

            with open(file, "w") as f:
                json.dump(user_data, f, indent=4)
                print("you are all done!")
                access_granted = True
        else:
            print("the master password cannot be empty.")
elif new_customer_check not in ("yes", "no"):
    print("Please answer yes or no.")

if access_granted:
    print("\nwhat would you like to do:")
    print("1. check password and username")
    print("2. change password or username")
    print("3. change master password")
    print("4. quit the software")

    while True:
        try:
            user_want_to_do = int(input("\nwhat will you do sir: "))
        except ValueError:
            print("Please enter a menu number.")
            continue
        
        if user_want_to_do == 4 or user_want_to_do == 6:
            print("thanks for using the app")
            break

        elif user_want_to_do == 1:
            print("here you go")

            

            with open(file, "r") as f:
                loaded_data = json.load(f)
                print("the password is", loaded_data["password"])
                print("the username is", loaded_data["username"])

        elif user_want_to_do == 2:
            print("what do you want to change")
            change_check = str(input("password or username: ")).lower().strip()

            if change_check == "password":
                print("here you go change it")
                new_password = str(input("new password : "))

                with open(file, "r") as f:
                    loaded_data = json.load(f)

                loaded_data["password"] = new_password

                with open(file, "w") as f:
                    json.dump(loaded_data, f, indent=4)
                    print("you are all set")

            elif change_check == "username":
                print("here you go change it")
                new_username = str(input("new username : "))

                with open(file, "r") as f:
                    loaded_data = json.load(f)

                loaded_data["username"] = new_username
                with open(file, "w") as f:
                    json.dump(loaded_data, f, indent=4)
                    print("you are all set")
            else:
                print("Please choose password or username.")

        elif user_want_to_do == 3:
            current_master_password = str(input("current master password: ")).strip()

            if current_master_password not in master_password:
                print("the master password is wrong")
                continue

            new_master_password = str(input("new master password: ")).strip()
            if not new_master_password:
                print("the master password cannot be empty")
                continue

            confirm_master_password = str(input("confirm new master password: ")).strip()
            if new_master_password != confirm_master_password:
                print("the master passwords do not match")
                continue

            with open(file, "r") as f:
                loaded_data = json.load(f)

            loaded_data["master_password"] = new_master_password
            with open(file, "w") as f:
                json.dump(loaded_data, f, indent=4)

            master_password = [new_master_password]
            print("the master password has been changed")
        else:
            print("Please choose a valid menu option.")
