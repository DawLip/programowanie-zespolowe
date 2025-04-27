-- SQLite
-- Dodanie użytkowników
INSERT INTO users (email, name, surname, phone, address, facebook, instagram, linkedin, password, is_active, about_me, created_at, updated_at)
VALUES 
    ('john@admin', 'John', 'Admin', '+48111111111', '123 Main St, Warsaw', 'https://facebook.com/john', 'https://instagram.com/john', 'https://linkedin.com/in/john', 'admin123', 1, 'Admin account', datetime('now'), datetime('now')),

    ('basic@user', 'Basic', 'User', '+48222222222', '456 Second St, Krakow', 'https://facebook.com/basic', 'https://instagram.com/basic', 'https://linkedin.com/in/basic', 'user123', 1, 'Simple user', datetime('now'), datetime('now')),

    ('jane@doe', 'Jane', 'Doe', '+48333333333', '789 Third St, Wroclaw', 'https://facebook.com/jane', 'https://instagram.com/jane', 'https://linkedin.com/in/jane', 'jane123', 1, 'Hello World', datetime('now'), datetime('now')),

    ('alice@wonder', 'Alice', 'Wonderland', '+48444444444', '10 Wonderland Ave, Poznan', 'https://facebook.com/alice', 'https://instagram.com/alice', 'https://linkedin.com/in/alice', 'alice123', 1, 'Dreamer', datetime('now'), datetime('now')),

    ('bob@builder', 'Bob', 'Builder', '+48555555555', '11 Builder St, Gdansk', 'https://facebook.com/bob', 'https://instagram.com/bob', 'https://linkedin.com/in/bob', 'bob123', 1, 'Can we fix it?', datetime('now'), datetime('now')),

    ('charlie@choco', 'Charlie', 'Chocolate', '+48666666666', '12 Chocolate Rd, Lublin', 'https://facebook.com/charlie', 'https://instagram.com/charlie', 'https://linkedin.com/in/charlie', 'charlie123', 1, 'Sweet life', datetime('now'), datetime('now')),

    ('daisy@flower', 'Daisy', 'Flower', '+48777777777', '13 Flower Blvd, Szczecin', 'https://facebook.com/daisy', 'https://instagram.com/daisy', 'https://linkedin.com/in/daisy', 'daisy123', 1, 'Flower power', datetime('now'), datetime('now')),

    ('eve@hacker', 'Eve', 'Hacker', '+48888888888', '14 Hacker Way, Bialystok', 'https://facebook.com/eve', 'https://instagram.com/eve', 'https://linkedin.com/in/eve', 'eve123', 1, 'Ethical hacker', datetime('now'), datetime('now')),

    ('frank@ocean', 'Frank', 'Ocean', '+48999999999', '15 Ocean Drive, Katowice', 'https://facebook.com/frank', 'https://instagram.com/frank', 'https://linkedin.com/in/frank', 'frank123', 1, 'Ocean vibes', datetime('now'), datetime('now')),

    ('grace@hopper', 'Grace', 'Hopper', '+48101010101', '16 Hopper Lane, Lodz', 'https://facebook.com/grace', 'https://instagram.com/grace', 'https://linkedin.com/in/grace', 'grace123', 1, 'Code queen', datetime('now'), datetime('now'));

-- Stworzenie pokoi
INSERT INTO room (type, name, created_at, description)
VALUES 
    ('GROUP', 'General Chat', datetime('now'), 'Test chat for users 1'),
    ('GROUP', 'Private Room', datetime('now'), 'Test chat for users 2'),
    ('GROUP', 'Team Chat', datetime('now'), 'Test chat for users 3'),
    ('GROUP', 'Developers', datetime('now'), 'Dev talk and coding'),
    ('GROUP', 'Random', datetime('now'), 'Anything goes');

-- Dodanie użytkowników do pokoi
INSERT INTO room_users (room_id, user_id, role, joined_at)
VALUES 
    (1, 1, 'OWNER', datetime('now')),
    (1, 2, 'USER', datetime('now')),
    (1, 4, 'USER', datetime('now')),
    (1, 5, 'USER', datetime('now')),
    (1, 6, 'USER', datetime('now')),

    (2, 1, 'OWNER', datetime('now')),
    (2, 3, 'USER', datetime('now')),
    (2, 4, 'USER', datetime('now')),

    (3, 1, 'OWNER', datetime('now')),
    (3, 2, 'ADMIN', datetime('now')),
    (3, 3, 'USER', datetime('now')),

    (4, 5, 'OWNER', datetime('now')),
    (4, 6, 'ADMIN', datetime('now')),
    (4, 7, 'USER', datetime('now')),
    (4, 8, 'USER', datetime('now')),

    (5, 9, 'USER', datetime('now')),
    (5, 10, 'USER', datetime('now'));

-- Dodanie przykładowych wiadomości
INSERT INTO messages (user_id, room_id, content, message_type, timestamp)
VALUES
    (1, 1, 'Hello everyone!', 'TEXT', datetime('now')),
    (2, 1, 'Hi John!', 'TEXT', datetime('now')),
    (1, 2, 'Private note to myself', 'TEXT', datetime('now')),
    (1, 3, 'Witajcie w pokoju zespołowym!', 'TEXT', datetime('now')),
    (2, 3, 'Cześć John!', 'TEXT', datetime('now')),
    (3, 3, 'Hej wszystkim!', 'TEXT', datetime('now')),
    (5, 4, 'Cześć developerzy!', 'TEXT', datetime('now')),
    (6, 4, 'Hej!', 'TEXT', datetime('now')),
    (9, 5, 'Cześć wszystkim!', 'TEXT', datetime('now')),
    (10, 5, 'Siema!', 'TEXT', datetime('now'));

-- Stworzenie znajomości
INSERT INTO friends (user_id, friend_id, created_at, status)
VALUES
    (1, 2, datetime('now'), 'accepted'),
    (1, 3, datetime('now'), 'accepted'),
    (2, 3, datetime('now'), 'accepted'),
    (2, 4, datetime('now'), 'accepted'),
    (5, 6, datetime('now'), 'accepted'),
    (5, 7, datetime('now'), 'pending'),
    (8, 9, datetime('now'), 'accepted'),
    (9, 10, datetime('now'), 'accepted'),
    (1, 5, datetime('now'), 'declined'); 

INSERT INTO room (type, name, description, created_at)
VALUES
    ('PRIVATE', 'Private Chat John-Basic', 'Private chat between John and Basic', datetime('now')),
    ('PRIVATE', 'Private Chat John-Jane', 'Private chat between John and Jane', datetime('now')),
    ('PRIVATE', 'Private Chat Basic-Jane', 'Private chat between Basic and Jane', datetime('now')),
    ('PRIVATE', 'Private Chat Basic-Alice', 'Private chat between Basic and Alice', datetime('now')),
    ('PRIVATE', 'Private Chat Bob-Charlie', 'Private chat between Bob and Charlie', datetime('now')),
    ('PRIVATE', 'Private Chat Eve-Frank', 'Private chat between Eve and Frank', datetime('now')),
    ('PRIVATE', 'Private Chat Frank-Grace', 'Private chat between Frank and Grace', datetime('now'));


INSERT INTO room_users (room_id, user_id, role, joined_at)
VALUES
    -- Private Chat John-Basic (room_id = 6)
    (6, 1, 'USER', datetime('now')),
    (6, 2, 'USER', datetime('now')),

    -- Private Chat John-Jane (room_id = 7)
    (7, 1, 'USER', datetime('now')),
    (7, 3, 'USER', datetime('now')),

    -- Private Chat Basic-Jane (room_id = 8)
    (8, 2, 'USER', datetime('now')),
    (8, 3, 'USER', datetime('now')),

    -- Private Chat Basic-Alice (room_id = 9)
    (9, 2, 'USER', datetime('now')),
    (9, 4, 'USER', datetime('now')),

    -- Private Chat Bob-Charlie (room_id = 10)
    (10, 5, 'USER', datetime('now')),
    (10, 6, 'USER', datetime('now')),

    -- Private Chat Eve-Frank (room_id = 11)
    (11, 8, 'USER', datetime('now')),
    (11, 9, 'USER', datetime('now')),

    -- Private Chat Frank-Grace (room_id = 12)
    (12, 9, 'USER', datetime('now')),
    (12, 10, 'USER', datetime('now'));


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