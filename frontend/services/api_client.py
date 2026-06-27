import httpx

class ApiClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/generate"
    
    def generate(self,action : str, text : str):
        response = httpx.post(f"{self.base_url}",
                              json = {
                                  "action" : action,
                                  "text" : text
                              },
                              timeout=120.0
                              )
        return response.json()
        