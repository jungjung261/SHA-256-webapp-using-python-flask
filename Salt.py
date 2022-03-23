import secrets

class Salt: 
    def __init__(self):
        self.salt = secrets.token_bytes(16)
        
    def generate(self):
        self.salt = secrets.token_bytes(16)
        
    def getsalt(self):
        return self.salt