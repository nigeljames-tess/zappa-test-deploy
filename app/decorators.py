import functools
import os
import traceback
from uuid import uuid4

from flask import abort, current_app, g
from marshmallow import ValidationError

from app import db, logger
from app.controllers.user_controller import UserController
from app.errors import ProcessingException, ValidationException
from app.errors.authentication import AuthenticationException
from app.errors.openai_wrapper import ThreadRunException
from app.errors.rate_limit import RateLimitException
from app.models.user_models import Organization, Role, User
from app.utils.messages import Error
from app.utils.response import Response


def permission_required(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not hasattr(g, "current_user"):
                abort(Response.HTTP_UNAUTHORIZED)
            if not g.current_user.can(permission):
                abort(Response.HTTP_FORBIDDEN)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def handle_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationException as ve:
            logger.info(str(ve.messages))
            return Response.make(ve.messages, Response.HTTP_BAD_REQUEST)
        except ValueError as ve:
            logger.info(str(ve.args[0]))
            return Response.make(str(ve.args[0]), Response.HTTP_BAD_REQUEST)
        except ProcessingException as pe:
            logger.info(str(pe.messages))
            return Response.make(pe.messages, Response.HTTP_BAD_REQUEST)
        except ThreadRunException as tre:
            logger.info(str(tre.messages))
            return Response.make(tre.messages, Response.HTTP_BAD_REQUEST)
        except ValidationError as err:
            logger.info(err)
            return Response.make(err.messages, Response.HTTP_BAD_REQUEST)
        except RateLimitException as rle:
            logger.info(rle)
            return Response.make(rle.messages, Response.HTTP_TOO_MANY_REQUESTS)
        except AuthenticationException as ae:
            logger.info(ae)
            return Response.make(ae.messages, Response.HTTP_UNAUTHORIZED)
        except Exception as e:
            traceback.print_exc()
            logger.error(f"general exception {e}")
            return Response.make(Error.REQUEST_FAILED, Response.HTTP_ERROR)

    return wrapper


def app_context_required(func):
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        app = current_app
        user_controller = UserController()

        with app.app_context():
            organization = (
                db.session.query(Organization)
                .filter_by(name="Test Organization")
                .first()
            )
            user = (
                db.session.query(User)
                .filter_by(email=current_app.config["ADMINS"][0])
                .first()
            )

            if user and organization:
                g.current_user = user
                return func(*args, **kwargs)

            organization = Organization(
                id=str(uuid4()),
                name="Test Organization",
                openai_api_key=os.environ.get("OPENAI_API_KEY"),
            )
            db.session.add(organization)
            db.session.commit()

            Role.insert_roles()

            user = User(
                id=str(uuid4()),
                email=current_app.config["ADMINS"][0],
                organization_id=organization.id,
                invited_by=None,
                waitlist=True,
                role_id=db.session.query(Role)
                .filter_by(name="Admin")
                .first()
                .id,
            )
            db.session.add(user)
            db.session.commit()

            test_api_key = os.environ.get("TEST_API_KEY")
            assert (
                test_api_key is not None
            ), "TEST_API_KEY environment variable should not be None"

            user.api_key = test_api_key
            user.api_key_active = True
            db.session.commit()

            g.current_user = user_controller.get_user_by_agentive_api_key(
                api_key=test_api_key
            )
            assert (
                g.current_user is not None
            ), "g.current_user should not be None"

            return func(*args, **kwargs)

    return decorated_function
