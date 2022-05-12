class Doctor:
    def __init__(self, doctorId, email, speciality):
        self.doctorId = doctorId
        self.email = email
        self.speciality = speciality

    def toDict(self):
        return {
            'docterId': self.doctorId,
            'email': self.email,
            'ClinicId': self.clinicId,
            'Speciality': self.speciality
        }
    
    def toJson(self):
        return {
            'doctorId': self.doctorId,
            'email': self.email,
            'clinicId': self.clinicId,
            'speciality': self.speciality
        }