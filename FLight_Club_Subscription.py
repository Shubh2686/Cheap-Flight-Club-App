import requests

USERS_EndPoint = "https://api.sheety.co/80a776766d1e7c2c63ae29076d75aaa4/myFlightDeals/users"

print("Welcome to Shubham's Flight Club!\nWe find the best flight deals and email you. ")

first_name = input("What is your first name?\n")
last_name = input("What is your last name?\n")
email = input("What is your Email?\n")
email_again = input("Please enter your Email again?\n")

while True:
    if email == email_again:
        new_data = {
            "user": {'firstName': first_name, 'lastName': last_name, 'email': email}
        }
        response = requests.post(url=USERS_EndPoint, json=new_data)
        print(response.text)
        break
    else:
        print("Email didn't match!!")
        email_again = input("Please enter your Email again?\n")

