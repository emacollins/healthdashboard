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
