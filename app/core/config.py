import yaml
from functools import lru_cache

from app.config.base import BaseConfig
from app.utils.profile import Profile

@lru_cache
def get_config(config_file="config.yaml", env=None) -> BaseConfig:
    """
    获取对应的环境变量

    :param config_file: 配置文件路径，默认为 "config.yaml"
    :param env: 环境变量，默认为 None，如果为 None 则根据 config.yaml 中的 env 字段获取
    :return: 不同环境对应的配置类对象
    """
    # 获取项目根目录
    project_root = Profile.get_profile_root()
    # 获取config文件路径
    config_path = project_root.joinpath(config_file)
    # 读取 yaml 配置文件
    with open(config_path, "r", encoding="utf-8") as f:
        yaml_config = yaml.safe_load(f)

    # 根据环境是dev还是prod
    if env:
        yaml_config["env"] = env
    else:
        env = yaml_config.get("env", "dev")

    # 根据环境获取对应的配置
    env_config = yaml_config.get(env, {})

    # 返回对应的配置类实例
    return BaseConfig(**env_config)