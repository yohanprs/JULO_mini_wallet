import http
import importlib
import os
from typing import Any, Tuple
from flask import Flask, Response, jsonify
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app() -> Flask:
    """
    This method used to handle app creation and configure some objects

    Keyword Arguments:
        test {bool}
          -- [The test flag to distinguish between main app and test app]
          (default: {False})

    Returns:
        Flask -- [Configured Flask App]
    """
    app = Flask(__name__, instance_relative_config=False)   
    app.config.from_object("mini_wallet.config.Config")

    with app.app_context():
        scan_models(app.name)
        db.init_app(app)
        ma.init_app(app)
        migrate.init_app(app, db)        

        blueprints = discover_blueprints(os.path.dirname(os.path.abspath(__file__)))

        for blueprint in blueprints:
            try:
                app.register_blueprint(blueprint)
            except Exception as e:
                raise Exception(f"Failed to register blueprint {blueprint}: {e}")       

        app.register_error_handler(Exception, exception_handler)
        app.register_error_handler(http.HTTPStatus.NOT_FOUND, resource_not_found)
        app.register_error_handler(http.HTTPStatus.UNAUTHORIZED, unauthorized)
        app.register_error_handler(http.HTTPStatus.FORBIDDEN, forbidden)
        app.register_error_handler(
            http.HTTPStatus.METHOD_NOT_ALLOWED, method_not_allowed
        )

        return app
    
def discover_blueprints(path: str) -> list:
    """
    This method used to load blueprints from given path

    Arguments:
        path {str} -- [The path that contains blueprints module]

    Returns:
        list -- [The list of blueprints object]
    """
    blueprints = list()
    dir_name = os.path.basename(path)
    packages = os.listdir(f"{path}/blueprints")

    for package in packages:
        if str(package).endswith(".py") and str(package) != "__init__.py":
            package = str(package).replace(".py", "")
            module_name = f"{dir_name}.blueprints.{package}"
            module = importlib.import_module(module_name)
            module_blueprints = [bp for bp in dir(module) if bp.endswith("_blueprint")]

            for mb in module_blueprints:
                blueprints.append(getattr(module, mb))

    return blueprints
    
# ERROR HANDLER
def exception_handler(e: Exception) -> Response:
    """
    This method used to handle unhandled exception

    Arguments:
        e {Exception} -- [Exception object]

    Returns:
        Response -- [Return internal server error message]
    """
    return (
        jsonify({"code": 500, "message": str(e)}),
        http.HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def resource_not_found(e: Any = "Not Found") -> Tuple[Any, http.HTTPStatus]:
    """
    This method is a error handler for http status Not Found

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Not Found"})

    Returns:
        [Response] -- [404 Response]
    """
    return jsonify({"code": 404, "message": str(e)}), http.HTTPStatus.NOT_FOUND
    # return make_json_response(http_status=404, data={"code": 404, "message": str(e)})


def unauthorized(e: Any = "Unauthorized") -> Tuple[Any, http.HTTPStatus]:
    """
    This method is a error handler for http status Unauthorized

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Unauthorized"})

    Returns:
        [Response] -- [401 Response]
    """
    return (
        jsonify({"code": 401, "message": str(e)}),
        http.HTTPStatus.UNAUTHORIZED,
    )
    # return make_json_response(http_status=401, data={"code": 401, "message": str(e)})


def forbidden(e: Any = "Forbidden") -> Tuple[Any, http.HTTPStatus]:
    """
    This method is a error handler for http status Forbidden

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Forbidden"})

    Returns:
        [Response] -- [403 Response]
    """
    return jsonify({"code": 403, "message": str(e)}), http.HTTPStatus.FORBIDDEN
    # return make_json_response(http_status=403, data={"code": 403, "message": str(e)})


def method_not_allowed(
    e: Any = "Method Not Allowed",
) -> Tuple[Any, http.HTTPStatus]:
    """
    This method is a error handler for http status Method Not Allowed

    Keyword Arguments:
        e {Any} -- [Exception or a message] (default: {"Method Not Allowed"})

    Returns:
        [Response] -- [403 Response]
    """
    return (
        jsonify({"code": 405, "message": str(e)}),
        http.HTTPStatus.METHOD_NOT_ALLOWED,
    )
    # return make_json_response(http_status=405, data={"code": 405, "message": str(e)})


def scan_models(app_name: str):
    for dirpath, dirnames, filenames in os.walk(f"./{app_name}/models"):
        head, tail = os.path.split(dirpath)
        if tail == "models":
            for filename in filenames:
                if filename.endswith(".py") and filename != "__init__.py":
                    filename_no_ext, _ = os.path.splitext(
                        os.path.join(dirpath, filename)
                    )
                    filename_no_ext = filename_no_ext[2:]
                    module_path = filename_no_ext.replace(os.sep, ".")
                    importlib.import_module(module_path)