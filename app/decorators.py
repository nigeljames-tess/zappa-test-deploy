import functools
import traceback

from app import logger
from app.errors import ProcessingException, ValidationException
from app.utils.messages import Error
from app.utils.response import Response


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
        except Exception as e:
            traceback.print_exc()
            logger.error(f"general exception {e}")
            return Response.make(Error.REQUEST_FAILED, Response.HTTP_ERROR)

    return wrapper

