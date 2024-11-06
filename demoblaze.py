import logging, base64, time
from locust import HttpUser, task, between
from random import randrange

def assertResponceCode(response,code):
    if response.status_code != code:
        response.failure("Expected "+ response.status_code + " to be "+ code)

def assertContains(response,text):
    with response as r:
        if text not in r.text:
            r.failure("Expected "+ response.text + " to contain "+ text)

def assertResponse(response,code,text):
    assertResponceCode(response,code)
    assertContains(response,text)

class demoblaze(HttpUser):
    host = "https://api.demoblaze.com"
    default_headers = {
        "accept": "application/json"
    }
    # activate this line below to simulate waiting time between user action
    # wait_time = between(1, 5)
    token = ""

    def on_start(self):
        password = "Password123!"
        password_bytes = password.encode("ascii")
        base64_bytes = base64.b64encode(password_bytes)
        base64_password = base64_bytes.decode("ascii")
        responseLogin = self.client.post("/login", json={"username":"random@email.com", "password":base64_password}, catch_response=True)
        assertResponse(responseLogin, 200, "Auth_token:")
        self.token = responseLogin.text[13:(len(responseLogin.text)-2)]
        responseCheckToken = self.client.post("/check", json={"token":self.token})
        assertResponse(responseCheckToken, 200, self.token)
        # logging.info("Current Token : " + token)
        # logging.info("Encoded Password : " + base64_password)
        logging.info("User is logged in")
        logging.info("Response token check : " + responseCheckToken.text)

    def on_stop(self):
        # this action will not be shown on Locust Statistics tab, but it can be seen from terminal / Logs tab
        responseBody = self.client.post("/deletecart", json={"cookie":self.token})
        assertResponse(responseBody, 200, "Item deleted.")
        logging.info("Cart is deleted")
        logging.info("Body response : " + responseBody.text)

    @task(3)
    def open_main_entries(self):
        with self.client.get(
            "/entries",
            catch_response=True
        ) as resp:
            pass
        assertResponse(resp, 200, "Samsung galaxy s6")
        logging.info("User is viewing Main Entries")
        logging.info("Body response : " + resp.text)

    @task(2)
    def view_products(self):
        randomProductId = str(randrange(1, 9))
        with self.client.post(
            "/view",
            json={"id":randomProductId},
            catch_response=True
        ) as resp:
            pass
        assertResponse(resp, 200, "title")
        logging.info("User is viewing Product with id : " + randomProductId)
        logging.info("Body response : " + resp.text)

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
            catch_response=True
        ) as response_1:
            pass
        # to run multiple apis sequentially, directly continue them like below line
        with self.client.post(
            "/viewcart",
            json={
                "cookie":self.token,
                "flag":"false"
                },
            catch_response=True
        ) as response_2:
            pass
        assertResponceCode(response_1, 200)
        assertResponse(response_2, 200, "prod_id")
        logging.info("User is adding Product with id : " + randomProductId + " into Cart")
        # logging.info("Body response Add to Cart : " + response_1.text) # this api response is empty, so I comment the logging
        logging.info("User is viewing selected Product inside Cart")
        logging.info("Body response View Cart : " + response_2.text)

# If you don't nedd any logging, just comment all line started with "logging.info"
