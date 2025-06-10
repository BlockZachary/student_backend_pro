from multiprocessing.context import AuthenticationError

from app.config.base import RedisConfig
from redis import asyncio as aioredis
from redis.exceptions import RedisError

from app.utils.log import log


class RedisHandler:
    """
    Redis 连接处理类
    """

    @classmethod
    async def init_conn_redis(cls, redis_config: RedisConfig):
        """
        初始化 Redis 连接

        :param redis_config: Redis 配置对象
        :return: Redis 连接对象
        :raises: RedisError: 如果连接失败
        :raises AuthenticationError: 如果用户名或密码错误
        :raises TimeoutError: 如果连接超时
        """

        redis = await aioredis.from_url(
            url=f"redis://{redis_config.host}",
            port=redis_config.port,
            username=redis_config.username,
            password=redis_config.password,
            db=redis_config.db,
            encoding="utf-8",
            decode_responses=True,
        )
        connection = None

        try:
            connection = await redis.ping()
            if not connection:
                raise RedisError("Redis connection failed, ping returned False")
            log.info("Redis Connection Initialized")
            return redis
        except AuthenticationError as e:
            log.error(f"Username or password error, details: {e}")
            raise
        except TimeoutError as e:
            log.error(f"Redis connection timeout, details: {e}")
            raise
        except RedisError as e:
            log.error(f"Redis connection error, details: {e}")
            raise
        finally:
            # 如果发生异常，关闭连接
            if "connection" not in locals() or not connection:
                await redis.close()

    @classmethod
    async def close_conn_redis(cls, redis):
        """
        关闭redis链接

        :param redis: Redis连接对象
        """

        await redis.close()
        log.info("Redis Connection Closed")

