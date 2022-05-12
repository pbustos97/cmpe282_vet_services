[Endpoint](https://2pai97g6d5.execute-api.us-west-2.amazonaws.com/dev)

# Register clinic endpoint (POST) /clinic-register
- Requires body only (all fields required)
  - clinic object
    - userId: String
    - clinicId: String
    - address: String
    - country: String
    - email: String
    - name: String

- Returns the created clinic object
- Ex.
    {'clinic': {'clinicId': 'clinic001', 'name': 'Cat Heaven', 'address': '1234 A St.', 'country': 'USA', 'email': 'clinic001@gmail.com'}}


# Get clinic endpoint (GET) /clinic-get
- Requires queries
  - 'clinicId' field
    - If 'clinicId' = '-1', then it will return a list of all clinics in the table
- Returns the object of the requested clinic