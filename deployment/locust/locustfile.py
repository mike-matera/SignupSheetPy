from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/jobs/Food/")

    def on_start(self):
        # id_password
        # id_username

        response = self.client.get('/accounts/login/?next=/jobs/Gate/')
        csrftoken = response.cookies['csrftoken']
        self.client.post('/accounts/login/?next=/jobs/Gate/',
                         {'username': 'test', 'password': 'test'},
                         headers={'X-CSRFToken': csrftoken})
