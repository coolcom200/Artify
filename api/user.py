from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    uid: str
    password_hash: str
    
    def __init__(self, elasticsearch_result):
        user_data = elasticsearch_result["_source"]
        self.name = user_data['name']
        self.email = user_data['email']
        self.uid = elasticsearch_result['_id']
        self.password_hash = user_data['password_hash']
