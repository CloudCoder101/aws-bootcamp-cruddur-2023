import uuid
from datetime import datetime, timedelta, timezone
from services.db import get_conn

class CreateActivity:
  def run(message, user_handle, ttl):
    model = {
      'errors': None,
      'data': None
    }
    
    now = datetime.now(timezone.utc).astimezone()
    
    # TTL parsing
    ttl_offset = None
    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30)
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7)
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3)
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1)
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12)
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3)
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1)
    else:
      model['errors'] = ['ttl_blank']
    
    # Validation
    if user_handle is None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']
    
    if message is None or len(message) < 1:
      model['errors'] = ['message_blank']
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars']
    
    if model['errors']:
      model['data'] = {
        'handle': user_handle,
        'message': message
      }
      return model
    
    expires_at = (now + ttl_offset)
    activity_uuid = str(uuid.uuid4())
    
    print(f"🔍 DEBUG: About to insert for {user_handle}")
    
    # DB INSERT
    try:
      with get_conn() as conn:
        with conn.cursor() as cur:
          cur.execute("""
            INSERT INTO public.activities (
              uuid,
              handle,
              message,
              expires_at,
              created_at
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING
              uuid::text,
              handle,
              message,
              created_at,
              expires_at;
          """, (activity_uuid, user_handle, message, expires_at, now))
          
          row = cur.fetchone()
          
          if row is None:
            model['errors'] = ['Insert failed']
            return model
          
          conn.commit()
          print(f"✅ Activity created: {row['uuid']}")
      
      model['data'] = {
        'uuid': row['uuid'],
        'display_name': 'Andrew Brown',
        'handle': row['handle'],
        'message': row['message'],
        'created_at': row['created_at'].isoformat(),
        'expires_at': row['expires_at'].isoformat()
      }
      
    except Exception as e:
      print(f"❌ Database error: {e}")
      model['errors'] = [f'Database error: {str(e)}']
    
    return model