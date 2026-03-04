README!!!

**Authors - Max Brook , Pavith Raj , Karen Andrianaharison , Joleen Thelen

=========================================================================================================================
HBnB is a backend web application inspired by accommodation platforms such as Airbnb.
The goal of this project is to design and implement a layered API using:

--Flask + Flask-RESTx

--Facade Pattern

--Repository Pattern

--Object-Oriented Design

--Clean Architecture 
 
 
This repository contains the backend implementation responsible for managing application entities such as:

--Users

--Places

--Amenities

--Reviews

===========================================================================================================


-----------------------------------------------------------------------
+ 1.0 File Structure
-------------------------------------------------------------

```
/hbnb
├── /app
│   ├── /api
│   │   ├── __init__.py            # Registers API namespaces
│   │   └── /v1
│   │       ├── places.py          # Place API endpoints (POST, GET, PUT)
│   │       ├── users.py           # (To be implemented by team)
│   │       ├── amenities.py       # Amenity endpoints (team extension)
│   │       └── reviews.py         # (Planned – future task)
│   │
│   ├── /models
│   │   ├── __init__.py
│   │   ├── place.py               #  Place entity with validation & relationships
│   │   ├── user.py                # (To be implemented)
│   │   ├── amenity.py             # Amenity model
│   │   └── review.py              # (Future implementation)
│   │
│   ├── /services
│   │   ├── __init__.py
│   │   └── facade.py              # HBnBFacade (business logic)
│   │
│   ├── /persistence
│   │   ├── __init__.py
│   │   └── repository.py          # InMemoryRepository (data abstraction layer)
│   │
│   └── __init__.py                # Flask app initialization
│
├── run.py                         # Application entry point
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

-------------------------------------------------------------
+ 2.0 Architecture 
-------------------------------------------------------------

API (Presentation Layer) : Handles HTTP requests and responses,Defines API endpoints,Validates request input,Calls the Facade layer
         
Facade  + Models [Place , Users , Amenity]  (Business Logic Layer) : Data validation,Relationship handling,Business rules enforcemet
         
Repository (Persistence Layer) : Abstracts data storage using repositories

---------------------------------------------------------------
+ 3.0 How to Run!
-------------------------------------------------------------


 Step 1 : create virtual environment
			python3 -m venv venv

 Step 2 : activate
			source venv/bin/activate

 Step 3 : install dependencies
			pip install -r requirements.txt

 Step 4 : run server
			python run.py

--------------------------------------------------------------
+ 4.0 Features Implemented 
-------------------------------------------------------------

++ 4.1.1 Users Endpoints


File in Repo —--> app/api/v1/users.py

| Method |	|Endpoint |					          |Description|

POST  		/api/v1/users/ 						  Create a new user
GET  		/api/v1/users/ 						  Get all users
GET  		/api/v1/users/<user_id> 			  Get a user by ID
PUT  		/api/v1/users/<user_id> 			  Update a user

Features:
	–-Request validation using Flask-Restx models
	–-Proper HTTP status codes
	-–Facade integration
	-–Email uniqueness enforces (no duplicates)
	-–Password hashing for security

++ 4.1.2 User Model

File in Repo —-> app/models/user.py

Features:
	-–User entity definition
	-–Attribute validation via property setters
	--Email must contain @ and be unique 
	--First_name and last_name cannot be empty
	--Password is hashed before storage

**Relationships:
	Places (a user can own multiple places)
	Reviews (a user can write multiple reviews)
	
	
++ 4.2.1 Amenities API endpoints


File in Repo —-> app/api/v1/amenities.py


|Method|	|Endpoint|							|Description|
POST		/api/v1/amenities/					Create a new amenity
GET			/api/v1/amenities/					Retrieve all amenities
GET			/api/v1/amenities/<amenity_id>		Retrieve amenity details
PUT			/api/v1/amenities/<amenity_id>		Update an amenity

Features
 --Request validation using Flask-RESTx models
 --Proper RESTful HTTP status codes
 --Integration with the HBnB Facade
 --Input validation for data
 --Consistent API response structure

++ 4.2.2 Amenity Model

File  in Repo  —->  app/models/amenity.py

Features:
 --Amenity entity definition
 --Validation for required attributes
 --Integration with persistence layer through the Facade
 
**Relationships
	--Amenities can be associated with multiple Place entities.
	--Acts as a reusable feature descriptor for places (e.g., Wi-Fi, Parking, Air Conditioning).


++ 4.3.1 Places API Endpoints

FIle in Repo -----> app/api/v1/places.py

| Method |		|Endpoint |					    |Description|
POST			/api/v1/places/					Create a new place
GET				/api/v1/places/					Retrieve all places
GET				/api/v1/places/<place_id>		Retrieve place details
PUT				/api/v1/places/<place_id>		Update a place 

Features:
	--Request validation using Flask-RESTx models
	--Proper HTTP status codes
	--Facade integration
	--Owner & amenities included in responses

++ 4.3.2 Place Model

File in Repo -----> app/models/place.py

Features:
	--Place entity definition
	--Attribute validation via property setters
		price ≥ 0
		latitude between -90 and 90
		longitude between -180 and 180
	--Enforces business rules
	--Maintains entity integrity

**Relationships:
		Owner (User)
		Amenities list
		Responsibilities:


++ 4.4.1 Reviews API Endpoints

File in Repo —-> app/api/v1/reviews.py

| Method | Endpoint | Description|

POST  		/api/v1/reviews/ 					Create a new review|
GET  		/api/v1/reviews/   					Get all reviews|
GET 		/api/v1/reviews/ <review_id>  		Get a review by ID|
PUT  		/api/v1/reviews/ <review_id>>  		Update a review|
DELETE  	/api/v1/reviews/ <review_id>  		Update a review|

Features:
	-–Request validation using Flask-Restx models
	-–Proper HTTP status codes
	-–Facade integration
	-–Only entity in the project that supports DELETE
	-–Validates user and place exist before creating review

++ 4.4.2 Review model

File in Repo —-> app/models/review.py

Features:
 -–Review entity definition
 -–Attribute validation via property setters
 --Rating must be between 1 and 5
 --Text cannot be empty
 --User_id must reference an existing user
 --Place_id must reference existing place

**Relationships:
		User (author of the review)
		Place (subject of the review)


--------------------------------------------------------------
5.0 Facade Layer
--------------------------------------------------------------

The HBnBFacade acts as the central coordination layer between the API (Presentation Layer), Business Logic, and Persistence Layer.

++ 5.1.1 User Management

**Implemented Methods
	create_user()
	get_user()
	get_all_users()
	update_user()

**Responsibilities
	Validates user input data before creation
	Coordinates repository operations
	Ensures user entity integrity
	Acts as the single entry point for user-related operations

**Features

--Repository integration

--Centralised validation handling

--Business rule orchestration

--Separation between API and persistence layers

++ 5.2.1 Place Management

**Implemented Methods
	create_place()
	get_place()
	get_all_places()
	update_place()

**Responsibilities
	--Validates place attributes (price, latitude, longitude)
	--Verifies owner existence
	--Links amenities to places
	--Coordinates persistence operations

**Features
	--Relationship handling (Owner + Amenities)
	--Validation orchestration
	--Repository abstraction
	--Centralised business coordination

++ 5.3.1 Amenity Management

**Implemented Methods
	create_amenity()
	get_amenity()
	get_all_amenities()
	update_amenity()

**Responsibilities
	--Validates amenity data
	--Manages amenity lifecycle
	--Interfaces with persistence repositories

**Features
	--Input validation
	--Repository integration
	--Business logic encapsulation

++ 5.4.1 Review Management

**Implemented Methods
	create_review()
	get_review()
	get_all_reviews()
	update_review()

**Responsibilities
	Validates review data (rating, content)
	Ensures referenced user and place exist
	Coordinates review persistence
	Maintains relationships between users and places

**Features
	--Relationship validation (User ↔ Place)
	--Centralised business logic
	--Repository coordination
	--Data integrity enforcement

--------------------------------------------------------------
6.0 Testing 
--------------------------------------------------------------

Endpoints can be tested using:

curl -X GET http://localhost:5000/api/v1/places/

Test Plan 

------------------------------------
1.0 Users
-------------------------------------

Case 1 - Create a User 

curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Jane",
  "last_name": "Doee",
  "email": "janedoee@email.com",
  "password": "strongpassword"
}'

Expected output(201):
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "janedoee@email.com",
  "password": "strongpassword"
}

------------------------------------
2.0 Amenities
-------------------------------------

Case 1 : create amenity
	POST /api/vi/amenities

%curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/amenities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string"
}'
{"id": "52a45620-2d5e-43f2-abe0-9cd929c7795c", "name": "string"}

Response:
201 Amenity successfully created
400 Invalid input data

Case 2 : Get all amenities
	GET /api/vi/amenities/

%curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/amenities/' \
  -H 'accept: application/json'

[]

Response:
	200 List of amenities retrieved successfully

Case 3: Get one amenity
	Returns a specific amenity by ID

GET /api/vi/amenities/amenity_id

% curl -X 'GET' \
  'http://127.0.0.1:5000/api/v1/amenities/dfc40eeb-634e-41ce-a065-f87abc374e07' \
  -H 'accept: application/json'
{"id": "dfc40eeb-634e-41ce-a065-f87abc374e07", "name": "string"}

Response:
200 Amenity details retrieved successfully
404 Amenity not found

Case 4: Update amenity
	**STILL UNDER TESTING, CAN’T GET A SUCCESSFUL RESULT** 

PUT /amenities/<amenity_id>

Updates an existing amenity

Request body (JSON):

{
    “name”: “stringi”
}

Response:
200 Amenity updated successfully
400 Invalid input data
404 Amenity not found


---------------------------------
3.0 Places
---------------------------------


case 1 : Create Place
	Creates a new place associated with an owner and amenities.

curl -X POST \
http://127.0.0.1:5000/api/v1/places/ \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d '{
  "title": "Shit Apartment",
  "description": "A bad place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "amenities": []
}'
Successful Response
{
  "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}

Status Codes
	-201 Created — Place successfully created
	-400 Bad Request — Invalid input data

Case 2 : Get All Places
	Returns a list of all registered places.

curl -X GET \
http://127.0.0.1:5000/api/v1/places/ \
-H "accept: application/json"
Example Response
[
  {
    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Cozy Apartment",
    "latitude": 37.7749,
    "longitude": -122.4194
  }
]

Status Codes
	200 OK — List of places retrieved successfully

Case 3 : Get Place Details
	Retrieves full details of a place, including its owner and amenities.

curl -X GET \
http://127.0.0.1:5000/api/v1/places/1fa85f64-5717-4562-b3fc-2c963f66afa6 \
-H "accept: application/json"
Example Response
{
  "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  },
  "amenities": [
    {
      "id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "Wi-Fi"
    }
  ]
}

Status Codes
	200 OK — Place retrieved successfully
	404 Not Found — Place does not exist

Case 4 : Update Place
	Updates an existing place. Only provided fields are modified.

curl -X PUT \
http://127.0.0.1:5000/api/v1/places/1fa85f64-5717-4562-b3fc-2c963f66afa6 \
-H "Content-Type: application/json" \
-d '{
  "title": "Luxury Condo",
  "price": 200.0
}'
Expected Response
{
  "message": "Place updated successfully"
}

Status Codes
	200 OK — Place updated successfully
	400 Bad Request — Invalid input data

404 Not Found — Place not found

**Validation Rules For places
	--Handled in the Place Model:
    --price must be ≥ 0
    --latitude must be between -90 and 90
	--longitude must be between -180 and 180
    --Invalid values raise exceptions handled by the API layer.


--------------------------------
4.0 ReviewS
----------------------------------


Case 1  - Create a Review
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/review/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Amazing place in town!",
  "rating": 5,
  "user_id": "<user_id>",
  "place_id": "<place_id>"
}'

Expected output(201):
'{
  "text": "Amazing place in town!",
  "rating": 5,
  "user_id": "string",
  "place_id": "string"
}'
