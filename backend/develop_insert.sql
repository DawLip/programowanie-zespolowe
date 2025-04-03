-- SQLite
-- Create test users
INSERT INTO users (email, name, surname, password, created_at, updated_at)
VALUES 
    ('john@admin', 'John', 'Admin', 'admin123', datetime('now'), datetime('now')),
    ('basic@user', 'Basic', 'User', 'user123', datetime('now'), datetime('now'));

-- Create rooms
INSERT INTO room (type, name, created_at)
VALUES 
    ('GROUP', 'General Chat', datetime('now')),
    ('GROUP', 'Private Room', datetime('now'));

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