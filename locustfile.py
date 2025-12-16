from locust import HttpUser, task, between

class APITestUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        payload = {
            "username": "admin",
            "password": "Admin123"
        }

        # Send as FORM DATA
        with self.client.post(
            "/auth/login",
            data=payload,
            catch_response=True
        ) as response:

            print("LOGIN RESPONSE:", response.json())

            if response.status_code == 200 and "access_token" in response.json():
                self.token = response.json()["access_token"]
            else:
                raise Exception("Login failed — Could not get access token")

    @task
    def get_students(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        self.client.get("/students", headers=headers)
