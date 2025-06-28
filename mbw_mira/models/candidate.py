class Candidate:
    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def update_info(self, name=None, email=None, phone_number=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number

    def get_info(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number
        }