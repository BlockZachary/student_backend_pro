from collections.abc import AsyncGenerator

import pytest

from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.deps import get_engine_from_fastapi
from app.core.postgresql import PsqlHandler
from app.server import app


class TestPsqlHandler:
    """
    测试数据库连接工具类
    """

    @pytest.mark.asyncio
    async def test_init_conn_psql(self, postgresql_db, fake_get_config):
        """
        测试数据库连接是否成功

        :param postgresql_db: pytest-postgresql 创建的数据库实例
        :param fake_get_config:  测试配置
        """

        fake_get_config.db.username = postgresql_db.info.user
        fake_get_config.db.password = SecretStr(postgresql_db.info.password)
        fake_get_config.db.host = postgresql_db.info.host
        fake_get_config.db.port = postgresql_db.info.port
        fake_get_config.db.database = postgresql_db.info.dbname
        async_engine = await PsqlHandler.init_conn_psql(fake_get_config.db)

        async with AsyncSession(async_engine) as session:
            # 创建临时表
            await session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, username TEXT)"
                )
            )
            await session.commit()

            # 插入数据
            await session.execute(
                text("INSERT INTO test_table (username) VALUES ('test_user')")
            )
            await session.commit()

            # 查询插入的数据
            result = await session.execute(
                text("SELECT * FROM test_table WHERE username = 'test_user'")
            )
            row = result.fetchone()

            # 验证数据是否插入成功
            assert row is not None

    @pytest.mark.asyncio
    async def test_get_async_session(self, fake_async_engine):
        """
        测试获取异步会话生成器

        :param fake_async_engine: 异步引擎
        """

        session = PsqlHandler._get_async_session(fake_async_engine)
        assert isinstance(session, AsyncSession)
        await session.close()

    @pytest.mark.asyncio
    async def test_get_session(self, fake_async_engine):
        """
        测试获取数据库引擎并创建会话

        :param fake_async_engine: 异步引擎
        """

        # 覆盖依赖项
        app.dependency_overrides[get_engine_from_fastapi] = fake_async_engine

        session = PsqlHandler.get_session()
        assert isinstance(session, AsyncGenerator)
        # 恢复原始的依赖项
        app.dependency_overrides = {}
