# redis_client.py - Shared module for initializing Redis connection pool

import redis

# Function to get Redis connection from the pool
def get_redis_connection(host_name, port=6379, db = 0):
    # Initialize Redis connection pool (shared across services)
    redis_pool = redis.ConnectionPool(host=host_name, port=port, db=db)
    return redis.StrictRedis(connection_pool=redis_pool)
