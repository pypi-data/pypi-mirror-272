import os

from prisma import Prisma


class SingletonPrisma:
    """测试."""

    # 这里我们只是简单地将db初始化为None，
    # 具体的初始化方式取决于你的实际需求
    _instance: Prisma = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Prisma(
                auto_register=True,
                datasource={"url": os.environ["DB_URL"]},
                http={"http2": True},
            )
        return cls._instance


# 使用单例模式
dbCLI = SingletonPrisma()
