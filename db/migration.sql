-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('admin', 'user'))
);

-- Create ongoing_parking table
CREATE TABLE ongoing_parking (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    vehicle_type VARCHAR(10) NOT NULL,
    floor INT NOT NULL,
    slot_count INT NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create parking_history table
CREATE TABLE parking_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    vehicle_type VARCHAR(10) NOT NULL,
    floor INT NOT NULL,
    slot_count INT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    fee NUMERIC(10, 2) NOT NULL
);

-- Add police_number column to ongoing_parking table
ALTER TABLE ongoing_parking ADD COLUMN police_number VARCHAR(20) NOT NULL;

-- Add police_number column to parking_history table
ALTER TABLE parking_history ADD COLUMN police_number VARCHAR(20) NOT NULL;
