FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3
WORKDIR ${LAMBDA_TASK_ROOT}
CMD [ "src.lambdas.event_handler.lambda_handler" ]

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}/

# Project initialization and view what was added to image
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --no-dev && ls -R

# Copy app to Docker Image
COPY src ${LAMBDA_TASK_ROOT}/src
