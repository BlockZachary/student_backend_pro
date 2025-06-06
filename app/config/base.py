from pydantic_settings import BaseSettings
from pydantic import SecretStr

class AppConfig(BaseSettings):
    """
    FastAPI的应用配置
    """

    # 应用名称
    name: str
    # 应用描述
    description: str
    # 应用接口
    api: str
    # 应用主机地址
    host: str
    # 应用端口
    port: int
    # uvicorn应用入口
    uvicorn: str
    # 应用版本
    version: str
    # 是否自动重载应用
    reload: bool


class DatabaseConfig(BaseSettings):
    """
    PostgreSQL配置
    """

    # 数据库主机地址
    host: str
    # 数据库端口
    port: int
    # 数据库用户名
    username: str
    # 数据库密码
    password: SecretStr
    # 数据库名称
    database: str
    # 数据库连接驱动
    driver_name: str
    # 是否开启sqlalchemy日志
    echo: bool
    # 允许溢出连接池大小的最大连接数
    max_overflow: int
    # 连接池大小，0表示连接数无限制
    pool_size: int
    # 连接回收时间（单位：秒）
    pool_recycle: int
    # 连接池中没有线程可用时，最多等待的时间（单位：秒）
    pool_timeout: int


class RedisConfig(BaseSettings):
    """
    Redis配置
    """

    # Redis主机地址
    host: str
    # Redis端口
    port: int
    # Redis用户名
    username: str
    # Redis密码
    password: SecretStr
    # Redis数据库索引
    db: int


class BaseConfig(BaseSettings):
    """
    基础配置所有环境通用的配置
    """

    # 基础配置
    app: AppConfig
    # PostgreSQL配置
    db: DatabaseConfig
    # Redis配置
    redis: RedisConfig

