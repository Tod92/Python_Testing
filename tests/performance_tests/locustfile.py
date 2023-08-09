from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")
    
    @task(3)
    def login(self):
        self.client.post("/showSummary", {"email":"john@simplylift.co"})

    @task(2)
    def book(self):
        self.client.get("/book/Spring Festival/Simply Lift")
    
    @task
    def purchase(self):
        self.client.post("/purchasePlaces", {"competition":"Fall Classic", "club":"She Lifts", "places":"1"})