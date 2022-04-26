[Endpoint](https://2va96t2eh7.execute-api.us-west-2.amazonaws.com/dev)

# Register Pet endpoint (POST) /pet-register
- Requires body only (all fields required)
  - pet object
    - name: String
    - age: String
    - ownerId: String
    - petId: String
    - breed: String
    - species: String
    - weight: String
- Returns the pet object

# Update User endpoint (POST) /pet-update
- Requires body only
  - user object
    - userId: String (Required)
    - all other fields optional
- Returns the user object

# Get role endpoint (GET) /pet-get
- Requires queries
  - userId: String
  - petId: String (-1 to get a list of all pets)
- Returns the pet object if a specific petId has been provided or returns a list of petId.