"""
Utility for emitting real-time logs to WebSocket clients via Redis
"""
import redis
import os

def emit_log(page_id: str, message: str):
    """
    Emit a log message to Redis for WebSocket streaming
    This is a synchronous function that can be called from the workflow
    """
    try:
        redis_host = os.getenv('REDIS_HOST', 'redis')
        r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        
        log_key = f"logs:{page_id}"
        r.rpush(log_key, message)
        r.expire(log_key, 300)  # Expire logs after 5 minutes
        # Keep only last 5 logs
        r.ltrim(log_key, -5, -1)
    except Exception as e:
        print(f"Failed to emit log: {e}")
