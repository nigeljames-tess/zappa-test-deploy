FROM amazon/aws-lambda-python:3.12

ARG FUNCTION_DIR="/var/task/"

COPY ./ $FUNCTION_DIR

WORKDIR /var/task

# Install dependencies
RUN pip install -r requirements.txt

# Grab the zappa handler.py and put it in the working directory
RUN ZAPPA_HANDLER_PATH=$( \
    python -c "from zappa import handler; print (handler.__file__)" \
    ) \
    && echo $ZAPPA_HANDLER_PATH \
    && cp $ZAPPA_HANDLER_PATH $FUNCTION_DIR

CMD ["handler.lambda_handler"]
