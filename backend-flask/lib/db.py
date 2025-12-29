import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

class Db:
  def __init__(self):
    self.conn = None

  def connect(self):
    if self.conn is None:
      try:
        self.conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
      except psycopg2.Error as e:
        print(f"Unable to connect to database: {e}")
        sys.exit(1)

  def query_array_json(self, sql, params=None):
    self.connect()
    with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
      cur.execute(sql, params)
      json = cur.fetchall()
      return json

db = Db()
