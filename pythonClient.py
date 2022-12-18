import requests

userCustomerID = 1
while True:
    print()
    print("-----------------------------------")
    print("1) Show Offerings")
    print("2) Show Shopping Basket")
    print("3) Add Offering to Shopping Basket")
    print("4) Revome Item from Shopping Basket")
    print("0) Exit)")
    print("-----------------------------------")
    userchoice = input()
    print()

    if userchoice == "1":
        response = requests.get("http://127.0.0.1:5000/customer/getAllOfferings")

    if userchoice == "2":
        #getAllShoppingBasketItemsForCustomerWithID(customerID)
        print("lol")
    
    if userchoice =="3":
        userOfferingID = input()
        response = requests.get("http://127.0.0.1:5000/customer/addToCart/" + str(userCustomerID) +"/" + str(userOfferingID))

    if userchoice =="4":
        userItemID = input()
        #removeFromCart(userCustomerID,userItemID)

    if userchoice == "0":
        exit()
        

# Make the GET request to the API

# Check the status code to ensure the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.text

        # Print the JSON data
        print(data)
    else:
        print("Request failed with status code:", response.status_code)


