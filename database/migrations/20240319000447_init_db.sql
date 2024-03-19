-- Replace 'mydatabase' with your desired database name
-- Replace 'mynewuser' with your desired user name
-- Replace 'mypassword' with your desired password

-- 1. Create a New Database
-- This command needs to be run from a client connected to a default database like 'postgres'
CREATE DATABASE applehealth;

-- Connect to the newly created database to execute the following commands
-- \c mydatabase;

-- 2. Create a New Role
CREATE ROLE eric WITH LOGIN PASSWORD 'XXXXXXX';

-- 3. Grant Privileges to the Role on the Database
GRANT ALL PRIVILEGES ON DATABASE applehealth TO eric;

-- Assuming you're now connected to 'mydatabase', create a simple table
CREATE TABLE example_table (
    id SERIAL PRIMARY KEY,
    example_text VARCHAR(255) NOT NULL,
    example_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- 4. Grant privileges on the table to your new role
GRANT ALL PRIVILEGES ON TABLE example_table TO eric;
