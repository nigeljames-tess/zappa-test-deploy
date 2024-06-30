class Error:
    REQUEST_FAILED = {"message": "Request failed to complete"}
    BAD_REQUEST = {"message": "Bad Request"}
    NOT_FOUND = {"message": "Not Found"}
    UNAUTHORIZED = {"message": "Unauthorized"}
    INTERNAL_SERVER_ERROR = {"message": "Internal Server Error"}


class Info:
    ACCEPTED = {"message": "accepted"}
    RECORD_NOT_FOUND = {"message": "Record not found"}
    NO_RECORDS_FOUND = {"message": "No records found"}
