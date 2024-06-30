class Error:
    REQUEST_FAILED = {"message": "Request failed to complete"}
    BAD_REQUEST = {"message": "Bad Request"}
    NOT_FOUND = {"message": "Not Found"}
    SCHEMA_VALIDATION_FAILED = {"message": "Failed to validate schema"}
    UNAUTHORIZED = {"message": "Unauthorized"}
    INTERNAL_SERVER_ERROR = {"message": "Internal Server Error"}
    INVALID_API_KEY = {"message": "Invalid API Key"}
    OPENAI_AUTHENTICATION_ERROR = {"message": "OpenAI Invalid API Key"}
    OPENAI_RATE_LIMIT_ERROR = {"message": "OpenAI Rate Limit Exceeded"}
    OPENAI_ASSISTANT_NOT_FOUND = {"message": "OpenAI Assistant not found"}
    OPENAI_THREAD_NOT_FOUND = {"message": "OpenAI Thread not found"}
    OPENAI_THREAD_IS_CURRENTLY_BEING_RUN = {
        "message": "OpenAI Thread is currently being run"
    }


class Info:
    ACCEPTED = {"message": "accepted"}
    RECORD_NOT_FOUND = {"message": "Record not found"}
    NO_RECORDS_FOUND = {"message": "No records found"}
