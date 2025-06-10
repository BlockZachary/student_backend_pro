from pathlib import Path


class Profile:
    @staticmethod
    def get_profile_root() -> Path:
        """
        获取项目根目录

        :return: 项目根目录
        """
        return Path(__file__).parent.parent.parent
