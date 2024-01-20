from redis import ConnectionPool, Redis
from src import settings


class SingleTon(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingleTon, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class RedisClient(metaclass=SingleTon):
    def __init__(self, host="localhost", port=6379, password=None):
        self.pool = ConnectionPool(
            host=host, password=password, port=port, decode_responses=True
        )
        self.port = port

    @property
    def conn(self):
        if not hasattr(self, "_conn"):
            self.get_connection()
        return self._conn

    def get_connection(self):
        self._conn = Redis(connection_pool=self.pool, port=self.port)


redis_conn = RedisClient(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD
).conn
