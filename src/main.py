from dishka.integrations.litestar import setup_dishka
from litestar import Litestar
from litestar.middleware import DefineMiddleware
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import (
    SwaggerRenderPlugin,
    RedocRenderPlugin,
    RapidocRenderPlugin,
    StoplightRenderPlugin,
    ScalarRenderPlugin,
)
from litestar.openapi.spec import Components, SecurityScheme

from src.common.di.container import container
from src.user_service.presentation.controllers.auth import AuthController
from src.user_service.presentation.controllers.role import RoleController
from src.user_service.presentation.controllers.user import UserController
from src.user_service.presentation.middlewares.auth import AuthMiddleware

app = Litestar(
    debug=True,
    route_handlers=[UserController, AuthController, RoleController],
    # on_app_init=[jwt_refresh_auth.on_app_init, jwt_access_auth.on_app_init],
    middleware=[DefineMiddleware(AuthMiddleware)],
    openapi_config=OpenAPIConfig(
        title="Litestar Example",
        description="Example of litestar",
        version="0.0.1",
        components=Components(
            security_schemes={
                "bearer": SecurityScheme(
                    type="http",
                    scheme="bearer",
                    bearer_format="JWT",
                    description="Access token в формате Bearer <token>",
                )
            }
        ),
        security=[{"bearer": []}],
        path="/docs",
        render_plugins=[
            SwaggerRenderPlugin(
                path="/swagger",
            ),
            RedocRenderPlugin(
                path="/redoc",
            ),
            StoplightRenderPlugin(path="/stoplight"),
            RapidocRenderPlugin(path="/rapid"),
            ScalarRenderPlugin(path="/scalar"),
        ],
    ),
)

setup_dishka(container, app)
