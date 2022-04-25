class Doctor:
    def __init__(self, doctorId, email, clinicId, speciality):
        self.doctorId = doctorId
        self.email = email
        self.clinicId = clinicId
        self.speciality = speciality

    def toDict(self):
        return {
            'doctorId': self.doctorId,
            'email': self.email,
            'ClinicId': self.clinicId,
            'Speciality': self.speciality
        }