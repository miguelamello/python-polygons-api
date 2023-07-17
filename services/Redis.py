import json
import redis
from appconfig import env

class Redis:
    def __init__(self):
      try:
        self.redis_conn = redis.Redis(host=env['redis_host'], port=6379, db=0)
      except:
        pass

    def get_data(self, key):
      try:
        cached_data = self.redis_conn.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None
      except:
        pass

    def set_data(self, key, data, ttl):
      try:
        self.redis_conn.setex(key, ttl, json.dumps(data))
      except:
        pass

    def delete_data(self, key):
      try:
        self.redis_conn.delete(key)
      except:
        pass
      
      