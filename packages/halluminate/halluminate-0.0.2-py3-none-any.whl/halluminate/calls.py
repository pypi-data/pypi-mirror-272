import requests
import json

class HalluminateAPI:
    base_url = "https://api.halluminate.ai/"
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.api_token}"
        }

    def send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return response.status_code

    def get_evaluations(self):
        return self.send_request("GET", "evaluations/")
    
    # TODO: Add upload csv to this
    def create_evaluation(self, name, description=None, assignee_username=None):
        data = {
            "name": name,
            "description": description,
            "assignee_username": assignee_username,
        }
        return self.send_request("POST", "create-evaluation/", data=data)
    
    def get_evaluation(self, evaluation_hash):
        url = f"evaluations/{evaluation_hash}/"
        return self.send_request("GET", url)
    
    def delete_evaluation(self, evaluation_hash):
        url = f"evaluations/{evaluation_hash}/delete"
        return self.send_request("DELETE", url)
    
    # TODO: implement this
    def update_evaluation(self, evaluation_hash, data):
        ...
        # url = f"evaluations/{evaluation_hash}/"
        # return self.send_request("PUT", url, data=data)

    def delete_evaluation(self, evaluation_hash):
        url = f"evaluations/{evaluation_hash}/"
        return self.send_request("DELETE", url)
    
    def create_label(self, evaluation_hash, input_text, output_text):
        url = f"evaluations/{evaluation_hash}/create-label/"
        data = {
            "question": input_text,
            "answer": output_text,
        }
        return self.send_request("POST", url, data=data)
    
    def get_labels(self, evaluation_hash):
        url = f"evaluations/{evaluation_hash}/labels/"
        return self.send_request("GET", url)
    
    def get_label(self, evaluation_hash, label_id):
        url = f"evaluations/{evaluation_hash}/labels/{label_id}/"
        return self.send_request("GET", url)
    
    def update_label(self, evaluation_hash, label_id, data):
        url = f"evaluations/{evaluation_hash}/labels/{label_id}/"
        return self.send_request("PUT", url, data=data)
    
    def delete_label(self, evaluation_hash, label_id):
        url = f"evaluations/{evaluation_hash}/labels/{label_id}/"
        return self.send_request("DELETE", url)
    
    def get_users(self):
        return self.send_request("GET", "users/")
    