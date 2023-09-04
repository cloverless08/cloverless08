import sqlite3
import random

varDataSave = 0
varResetQuery = 0
varOpenTableConfirm = 1
varUQTable = 0

# Preset login credentials
userNameOne = "carrick"
userPassOne = "1234"

userNameTwo = random.randint(
    000000000000000,
    999999999999999)  # Unset login credentials, encrypted for security
userPassTwo = random.randint(000000000000000, 999999999999999)

userNameThree = random.randint(000000000000000, 999999999999999)
userPassThree = random.randint(000000000000000, 999999999999999)

# Ask for username and password
username = input("Enter your username: ")
password = input("Enter your password: ")
print(" ")  #empty

# Check if the entered credentials are correct
if (username == userNameOne and password == userPassOne) or (
    username == userNameTwo
    and password == userPassTwo) or (username == userNameThree
                                     and password == userPassThree):

  # Generates unuique session ID
  varSessionIdent = random.randint(0000, 9999)
  print("LOGIN COMPLETE\nSESSION ID: ")
  print(varSessionIdent)
  print(" ")  #empty

  # Connect to the SQLite database
  conn = sqlite3.connect("userData.db")
  cursor = conn.cursor()

  # Create or check the user data table
  cursor.execute('''CREATE TABLE IF NOT EXISTS entries
                      (name text, age integer, color text)''')

  #Directory for data browsing
  varDirec = input(
      "DIRECTORY\nTo create a new entry, type: ADD\nTo view database, type: VIEW\n"
  ).lower()
  if varDirec == "ADD".lower():

    # Collect user information through input
    varName = input("\nLOG-NAME\n").lower()
    varAge = input("LOG-AGE\n")
    try:
      varAge = int(varAge)  # Attempt to convert age to an integer
    except ValueError:
      print("Age must be a valid integer.")
      conn.close()
      exit(1)
    varColor = input("LOG-COLOR\n")

    varIdent = random.randint(0000000,
                              9999999)  # Create a random UUID for each user
    print("\nName and Age recieved, UUID generated")

    # Insert user data into the database
    cursor.execute("INSERT INTO entries VALUES (?, ?, ?, ?)",
                   (varName, varAge, varIdent, varColor))
    print("Data Inserting")

    # Commit changes and close the database
    conn.commit()
    conn.close()
    print("Table Changes Commited")
    varDataSave = 1

    # Final confirmation message
    if varDataSave == 1:
      print("Data Saved Succesfully")
    else:
      print("Data Not Saved")

  else:

    if varDirec == "VIEW".lower():

      # Get a name to retrieve data or list all entries
      retrieve_name = input("\nEnter a name from the database: ").lower()

      # Connect to the database
      conn = sqlite3.connect("dbUserData.db")
      cursor = conn.cursor()

      if retrieve_name == "userdatalist".lower():
        # Retrieve and list all entries
        cursor.execute("SELECT * FROM entries")
        all_entries = cursor.fetchall()
        if all_entries:
          for entry in all_entries:
            name, age, user_id = entry
            print(f"Name: {name}, Age: {age}, ID: {user_id}")
        else:
          print("No entries found.")

      else:
        #Retrieves and removes all entries
        if retrieve_name == "userdatadelete".lower():

          #Removal confirmation
          varDeleteConfirm = input(
              "\nAre you sure? This will delete all current logs.\nY or N\n\n")
          if varDeleteConfirm == "Y":
            conn.execute("DROP TABLE entries")

            print("Logs deleted succesfully")

          else:
            print("Logs retained")

        else:
          # Retrieve data for the given name (case-insensitive)
          cursor.execute("SELECT * FROM entries WHERE lower(name)=?",
                         (retrieve_name, ))
          data = cursor.fetchone()

          if data:
            name, age, user_id = data
            print(f"Name: {name}, Age: {age}, ID: {user_id}")
          else:
            print("Name not found.")
    else:

      print("INCORRECT PROMPT (error101)")

    # Close the database
    conn.close()

else:
  print("Invalid username or password. Access denied.")

# 101 = Syntax Error when entering information or data
