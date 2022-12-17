import requests

# Make the GET request to the API
response = requests.get("http://127.0.0.1:5000/customer/getOfferings")

# Check the status code to ensure the request was successful
if response.status_code == 200:
    # Get the JSON data from the response
    data = response.text

    # Print the JSON data
    print(data)
else:
    print("Request failed with status code:", response.status_code)

