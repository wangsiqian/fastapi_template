import pkgutil
from importlib import import_module

from fastapi import FastAPI

from extensions.fastapi import GlobalExceptionHandler, GlobalMiddleware


def create_app() -> FastAPI:
    """create fastapi app
    """
    app = FastAPI()

    # 导入所有的子模块
    for module in pkgutil.iter_modules(['apps']):
        if not module.ispkg:
            continue

        sub_app = import_module(f'apps.{module.name}')
        for router in sub_app.routers:
            app.include_router(router)

    GlobalExceptionHandler(app).init()
    GlobalMiddleware(app).init()

    return app
