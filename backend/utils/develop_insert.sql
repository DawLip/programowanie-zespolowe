-- SQLite
-- Create test users
INSERT INTO users (email, name, surname, password, created_at, updated_at)
VALUES 
    ('john@admin', 'John', 'Admin', 'admin123', datetime('now'), datetime('now')),
    ('basic@user', 'Basic', 'User', 'user123', datetime('now'), datetime('now'));

-- Create rooms
INSERT INTO room (type, name, created_at, description)
VALUES 
    ('GROUP', 'General Chat', datetime('now'), 'Test chat for users 1'),
    ('GROUP', 'Private Room', datetime('now'), 'Test chat for users 2');

-- Add users to rooms
INSERT INTO room_users (room_id, user_id, role, joined_at)
VALUES 
    -- Both users in Room 1 (General Chat)
    (1, 1, 'SUPERADMIN', datetime('now')),  -- John as SUPERADMIN
    (1, 2, 'USER', datetime('now')),  -- Basic as USER
    
    -- Only John in Room 2 (Private Room)
    (2, 1, 'SUPERADMIN', datetime('now'));  -- John as SUPERADMIN

-- Add some test messages
INSERT INTO messages (user_id, room_id, content, message_type, timestamp)
VALUES
    (1, 1, 'Hello everyone!', 'TEXT', datetime('now')),
    (2, 1, 'Hi John!', 'TEXT', datetime('now')),
    (1, 2, 'Private note to myself', 'TEXT', datetime('now'));

-- Create a friendship
INSERT INTO friends (user_id, friend_id, created_at)
VALUES (1, 2, datetime('now'));

-- 1. Dodanie trzeciego użytkownika
INSERT INTO users (email, name, surname, password, created_at, updated_at)
VALUES 
    ('jane@doe', 'Jane', 'Doe', 'jane123', datetime('now'), datetime('now'));

-- 2. Tworzenie pokoju dla 3 osób
INSERT INTO room (type, name, created_at)
VALUES 
    ('GROUP', 'Team Chat', datetime('now'));

-- 3. Dodanie członków
INSERT INTO room_users (room_id, user_id, role, joined_at)
VALUES 
    (3, 1, 'SUPERADMIN', datetime('now')),
    (3, 2, 'ADMIN', datetime('now')),
    (3, 3, 'USER', datetime('now'));

-- 4. Przykładowe wiadomości
INSERT INTO messages (user_id, room_id, content, message_type, timestamp)
VALUES
    (1, 3, 'Witajcie w pokoju zespołowym!', 'TEXT', datetime('now')),
    (2, 3, 'Cześć John!', 'TEXT', datetime('now')),
    (3, 3, 'Hej wszystkim!', 'TEXT', datetime('now'));

-- 5. Aktualizacja znajomości
INSERT INTO friends (user_id, friend_id, created_at)
VALUES 
    (1, 3, datetime('now')),
    (3, 2, datetime('now'));


--Kod do czyszczenia bazy danych
PRAGMA foreign_keys = OFF;

-- Usuń dane w odpowiedniej kolejności (od najbardziej zależnych)
DELETE FROM friends;
DELETE FROM messages;
DELETE FROM room_users;
DELETE FROM room;
DELETE FROM users;

-- Włącz klucze obce z powrotem
PRAGMA foreign_keys = ON;