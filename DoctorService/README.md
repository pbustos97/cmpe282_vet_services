[Endpoint](https://xdy9s2ux8i.execute-api.us-west-2.amazonaws.com/dev)

# Get Doctor (GET) /doctor-get
- Requires queries
  - Only 'doctorId' field
- Returns the doctor object and a section of the user object

# Register Doctor (POST) /doctor-register
- Requires body only
  - doctor object
    - doctorId: String
    - email: String
    - clinicId: String
    - speciality: String (Optional but cannot be empty string)
- Return doctor object