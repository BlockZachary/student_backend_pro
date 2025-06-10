import fakeredis.aioredis
import pytest
from pytest_postgresql import factories
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import get_config


@pytest.fixture(scope="function")
def fake_get_config():
    """
    模拟配置对象，用于测试配置相关的操作

    :return: 模拟的配置对象
    """

    return get_config()


# 利用 pytest-postgresql 定义一个数据库工厂
postgresql_instance = factories.postgresql("postgresql_proc")


@pytest.fixture(scope="function")
async def postgresql_db(postgresql_instance):
    """
    创建 pytest-postgresql 数据库工厂实例

    :param postgresql_instance:  pytest-postgresql 创建的数据库实例
    :return:  pytest-postgresql 创建的数据库实例
    """

    return postgresql_instance


@pytest.fixture(scope="function")
async def fake_async_engine(postgresql_db):
    """
    创建数据库引擎，根据 pytest-postgresql 创建的数据库信息生成连接字符串

    :param postgresql_db: pytest-postgresql 创建的数据库实例
    :return: 数据库引擎
    """

    # 创建数据库引擎
    engine = create_async_engine(
        f"postgresql+asyncpg://{postgresql_db.info.user}:{postgresql_db.info.password}@{postgresql_db.info.host}:{postgresql_db.info.port}/{postgresql_db.info.dbname}"
    )
    # 通过 yield 将引擎传递给测试用例使用
    yield engine
    # 测试用例执行完毕后，关闭引擎
    await engine.dispose()


@pytest.fixture(scope="function")
async def fake_redis_client():
    """
    创建 fakeredis 实例的 fixture

    :return: fakeredis 实例
    """

    # 创建 fakeredis 实例
    # decode_responses=True 返回的是字符串，否则是字节
    fake_redis = fakeredis.aioredis.FakeRedis(
        decode_responses=True,
    )
    yield fake_redis

    # 清理
    await fake_redis.flushall()
    await fake_redis.aclose()


@pytest.fixture(scope="function")
async def fake_redis_username():
    """
    模拟redis用户名

    :return: 模拟的redis用户名
    """

    return "test@mail.com"
