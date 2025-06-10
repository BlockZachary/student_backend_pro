from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_config
from app.core.postgresql import PsqlHandler
from app.core.redis import RedisHandler
from app.utils.log import log, LogHelpers

config = get_config()

async def startup_services(app: FastAPI):
    """
    初始化服务

    :param app: FastAPI应用程序实例
    """

    # 初始化日志配置 拦截器
    LogHelpers.init_config()
    # 初始化config
    app.state.config = config
    # 初始化数据库连接
    app.state.psql_engine = await PsqlHandler.init_conn_psql(config.db)
    # 初始化Redis连接
    app.state.redis = await RedisHandler.init_conn_redis(config.redis)


async def close_services(app: FastAPI):
    """
    关闭服务

    :param app: FastAPI应用程序实例
    """
    # 关闭数据库连接
    await PsqlHandler.close_conn_psql(app.state.psql_engine)
    # 关闭Redis连接
    await RedisHandler.close_conn_redis(app.state.redis)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI应用程序的生命周期管理器

    :param app: FastAPI应用程序实例
    """

    # 初始化服务
    await startup_services(app)
    log.info(f"{config.app.name} Startup Success")

    yield

    # 关闭服务
    await close_services(app)
    log.info(f"{config.app.name} Close Success")


# 初始化FastAPI对象
app = FastAPI(
    title=config.app.name,
    description=config.app.description,
    version=config.app.version,
    lifespan=lifespan,
)

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}