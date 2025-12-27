-- db/schema.sql
-- Cruddur minimal schema (activities + replies)
-- Enable UUID helper
CREATE EXTENSION IF NOT EXISTS pgcrypto;

DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS activities;

CREATE TABLE activities (
  uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  handle text NOT NULL,
  message text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz NULL,
  likes_count integer NOT NULL DEFAULT 0,
  reposts_count integer NOT NULL DEFAULT 0,
  replies_count integer NOT NULL DEFAULT 0
);

CREATE TABLE replies (
  uuid uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  reply_to_activity_uuid uuid NOT NULL REFERENCES activities(uuid) ON DELETE CASCADE,
  handle text NOT NULL,
  message text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  likes_count integer NOT NULL DEFAULT 0,
  reposts_count integer NOT NULL DEFAULT 0,
  replies_count integer NOT NULL DEFAULT 0
);

-- Helpful index for thread lookups
CREATE INDEX IF NOT EXISTS replies_reply_to_idx ON replies(reply_to_activity_uuid);

-- db/seed.sql
TRUNCATE replies, activities;

-- Insert three activities (store UUIDs so replies can reference)
WITH a1 AS (
  INSERT INTO activities (handle, message, created_at, expires_at, likes_count, replies_count)
  VALUES (
    'Andrew Brown',
    'Cloud is fun!',
    now() - interval '2 days',
    now() + interval '5 days',
    5,
    1
  )
  RETURNING uuid
),
a2 AS (
  INSERT INTO activities (handle, message, created_at, expires_at)
  VALUES (
    'Worf',
    'I am out of prune juice',
    now() - interval '7 days',
    now() + interval '2 days'
  )
  RETURNING uuid
),
a3 AS (
  INSERT INTO activities (handle, message, created_at, expires_at)
  VALUES (
    'Garek',
    'My dear doctor, I am just simple tailor',
    now() - interval '1 hours',
    now() + interval '12 hours'
  )
  RETURNING uuid
)
INSERT INTO replies (reply_to_activity_uuid, handle, message, created_at)
SELECT a1.uuid, 'Worf', 'This post has no honor!', now() - interval '2 days'
FROM a1;
