INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown', 'andrew@example.com', 'MOCK'),
  ('Andrew Bayko', 'bayko', 'bayko@example.com', 'MOCK'),
  ('Robert', 'robert', 'robert@example.com', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid FROM public.users WHERE handle = 'andrewbrown'),
    'Just deployed a Flask backend to ECS Fargate with RDS PostgreSQL. Cloud engineering is the future.',
    NOW() + INTERVAL '30 days'
  ),
  (
    (SELECT uuid FROM public.users WHERE handle = 'bayko'),
    'Working through AWS architecture patterns today. ALB + ECS + RDS is a solid production stack.',
    NOW() + INTERVAL '30 days'
  ),
  (
    (SELECT uuid FROM public.users WHERE handle = 'robert'),
    'Schema migrations via ECS one-off tasks — cleaner than you think once you nail the command override format.',
    NOW() + INTERVAL '30 days'
  );