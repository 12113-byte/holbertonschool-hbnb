-- Create tables
/*
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(260),
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (place_id) REFERENCES Place(id),
    UNIQUE (user_id, place_id)
);

CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY, 
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS amenityplacemap (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    FOREIGN KEY (place_id) REFERENCES Place(id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id)
);
*/
-- inserting admin user 
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$oAFoH6mmuyGqM0hNZu.aOezz64eD0lzwk6CspMChsstPHkw1pJfH6',
    TRUE
);
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '2ca1f05a-720e-47f9-be39-1171e212312d',
    'User',
    'Example',
    'user@hbnb.io',
    '$2b$12$oAFoH6mmuyGqM0hNZu.aOezz64eD0lzwk6CspMChsstPHkw1pJfH6',
    FALSE
);

INSERT INTO places (id, title, description, image_url, price, latitude, longitude, user_id)
VALUES (
    '3b022b58-796a-4a14-90b2-2e35fc7f1b98',
    'Brand New Apartment',
    'New Apartment that looks amazing! Freshly squeezed',
    '../static/images/beautiful-new-apartment.jpg',
    '25',
    '15',
    '12',
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);
INSERT INTO places (id, title, description, image_url, price, latitude, longitude, user_id)
VALUES (
    '3ec67d3a-0c14-4e0f-950d-9b1b343c5815',
    'Old Apartment',
    'Ancient, Haunted, filled with ghosts, spiders, and ghost-spiders',
    '../static/images/haunted-house-gothic-style.jpg',
    '75',
    '50',
    '-7',
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);
INSERT INTO places (id, title, description, image_url, price, latitude, longitude, user_id)
VALUES (
    'aee46255-37ff-44f1-9cef-5460147ecae8',
    'Apartment',
    'It is actually a house',
    '../static/images/house-not-apartment.jpg',
    '1150',
    '56',
    '33',
    '2ca1f05a-720e-47f9-be39-1171e212312d'
);

-- inserting amenities 
INSERT INTO amenities (id, name) VALUES ('78c49624-1d50-4b6b-a909-a83a82bbb08b', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('e92d4244-823f-48e2-b4f2-d02e3f64845e', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('058d929a-a677-4eff-8db0-ea88f4c20bba', 'Air Conditioning');

-- Wifi and AC into New Apartment --
INSERT INTO amenityplacemap (id, place_id, amenity_id)
VALUES (
    '8d01ecb5-5802-482b-8114-c35e8178c55d',
    '3b022b58-796a-4a14-90b2-2e35fc7f1b98',
    '78c49624-1d50-4b6b-a909-a83a82bbb08b'
);

INSERT INTO amenityplacemap (id, place_id, amenity_id)
VALUES (
    '84b40606-6461-49c8-85b9-8d2a7cf93565',
    '3b022b58-796a-4a14-90b2-2e35fc7f1b98',
    '058d929a-a677-4eff-8db0-ea88f4c20bba'
);

-- Wifi, Simming and AC into Apartment --
INSERT INTO amenityplacemap (id, place_id, amenity_id)
VALUES (
    '391df0f0-850a-4c68-b981-5b135daa1327',
    'aee46255-37ff-44f1-9cef-5460147ecae8',
    '78c49624-1d50-4b6b-a909-a83a82bbb08b'
);
INSERT INTO amenityplacemap (id, place_id, amenity_id)
VALUES (
    'b4fbbc7e-8607-4ef5-8954-ce49f3abf0c6',
    'aee46255-37ff-44f1-9cef-5460147ecae8',
    'e92d4244-823f-48e2-b4f2-d02e3f64845e'
);
INSERT INTO amenityplacemap (id, place_id, amenity_id)
VALUES (
    '7a6b8ded-d806-43b0-8d97-071436744a30',
    'aee46255-37ff-44f1-9cef-5460147ecae8',
    '058d929a-a677-4eff-8db0-ea88f4c20bba'
);


