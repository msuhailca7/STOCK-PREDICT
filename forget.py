# Install Courier SDK: pip install trycourier
from trycourier import Courier

client = Courier(auth_token="pk_prod_Q7S8YDR7CMMZB1MEW9T9Z0WMBKVP")

resp = client.send_message(
        message={
          "to": {
            "email": "msuhailca7@gmail.com"
          },
          "content": {
            "title": "Welcome to Courier!",
            "body": "Want to hear a joke? {{joke}}"
          },
          "data":{
            "joke": "Why does Python live on land? Because it is above C level"
          }
        }
  )