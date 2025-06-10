from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine


def get_engine_from_fastapi(request: Request) -> AsyncEngine:
    """
    从FastAPI请求中获取异步引擎
    用于解耦在postgresql.py中的FastAPI的request和数据库层

    :param request: FastAPI请求对象
    :return: 异步引擎
    """

    return request.app.state.psql_engine
