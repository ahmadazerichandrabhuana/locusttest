import logging, base64, time
from locust import HttpUser, task, between
from random import randrange

class demoblaze(HttpUser):
    host = "https://api.demoblaze.com"
    default_headers = {
        "accept": "application/json"
    }
    token = ""

    def on_start(self):
        password = "Password123!"
        password_bytes = password.encode("ascii")
        base64_bytes = base64.b64encode(password_bytes)
        base64_password = base64_bytes.decode("ascii")
        responseLogin = self.client.post("/login", json={"username":"random@email.com", "password":base64_password})
        self.token = responseLogin.text[13:(len(responseLogin.text)-2)]
        responseCheckToken = self.client.post("/check", json={"token":self.token})
        # logging.info("Current Token : " + token)
        # logging.info("Encoded Password : " + base64_password)
        logging.info("User is logged in")
        logging.info("Response token check : " + str(responseCheckToken.json()))

    def on_stop(self):
        # this action will not be shown on Locust Statistics tab, but it can be seen from terminal / Logs tab
        responseBody = self.client.post("/deletecart", json={"cookie":self.token})
        logging.info("Cart is deleted")
        logging.info("Body response : " + responseBody.text)

    @task(3)
    def open_main_entries(self):
        with self.client.get(
            "/entries"
        ) as resp:
            pass
        logging.info("User is viewing Main Entries")
        logging.info("Body response : " + str(resp.json()))

    @task(2)
    def view_products(self):
        randomProductId = str(randrange(1, 9))
        with self.client.post(
            "/view",
            json={"id":randomProductId},
        ) as resp:
            pass
        logging.info("User is viewing Product with id : " + randomProductId)
        logging.info("Body response : " + str(resp.json()))

    @task
    def add_to_cart_and_view_cart(self):
        timestamp = str(int(time.time()))
        # logging.info("Sample Timestamp : " + timestamp)
        randomProductId = str(randrange(1, 9))
        with self.client.post(
            "/addtocart",
            json={
                "id":"58d45c9d-ab6d-6e07-f2a7-993a6c7686e6-" + timestamp,
                "cookie":self.token,
                "prod_id":randomProductId,
                "flag":"false"
                },
        ) as response_1:
            pass
        # to run multiple apis sequentially, directly continue them like below line
        with self.client.post(
            "/viewcart",
            json={
                "cookie":self.token,
                "flag":"false"
                },
        ) as response_2:
            pass
        logging.info("User is adding Product with id : " + randomProductId + " into Cart")
        # logging.info("Body response Add to Cart : " + response_1.text) # this api response is empty, so I comment the logging
        logging.info("User is viewing selected Product inside Cart")
        logging.info("Body response View Cart : " + str(response_2.json()))