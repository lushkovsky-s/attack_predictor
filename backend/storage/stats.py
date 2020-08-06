from redis import Redis

import settings

r = Redis.from_url(settings.REDIS_URI)

def get():
    count = int(r.get('requests_count').decode()) if r.exists('requests_count') else 0
    avg_time = float(r.get('requests_avg_time').decode()) if r.exists('requests_avg_time') else 0
    
    return count, avg_time 
    
def set(count, avg_time):
    r.set('requests_count', count)
    r.set('requests_avg_time', avg_time)
