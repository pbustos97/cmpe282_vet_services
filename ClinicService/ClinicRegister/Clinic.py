class Clinic:
    def __init__(self, clinicId, clinicName, clinicEmail, clinicAddress, clinicCountry):
        self.id = clinicId
        self.name = clinicName
        self.address = clinicAddress
        self.country = clinicCountry
        self.email = clinicEmail,
    
    def toJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'country': self.country,
            'email': self.email
        }

    def toDict(self):
        return {
            'clinicId': self.id,
            'clinicName': self.name,
            'Address': self.address,
            'Country': self.country,
            'email': self.email
        }