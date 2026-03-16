-- Create tables 
CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY, 
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id)
    REFERENCES Amenity(id)
);

-- inserting admin user 
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$oAFoH6mmuyGqM0hNZu.aOezz64eD0lzwk6CspMChsstPHkw1pJfH6',
    TRUE
);

-- inserting amenities 
INSERT INTO Amenity (id, name) VALUES ('78c49624-1d50-4b6b-a909-a83a82bbb08b', 'WiFi');
INSERT INTO Amenity (id, name) VALUES ('e92d4244-823f-48e2-b4f2-d02e3f64845e', 'Swimming Pool');
INSERT INTO Amenity (id, name) VALUES ('058d929a-a677-4eff-8db0-ea88f4c20bba', 'Air Conditioning');