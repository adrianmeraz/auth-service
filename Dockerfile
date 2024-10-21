FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3
WORKDIR ${LAMBDA_TASK_ROOT}
CMD [ "src.lambdas.event_handler.lambda_handler" ]

# Install Poetry, Install Dependencies, and view what was added to image
RUN pip install "poetry==$POETRY_VERSION" && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --no-dev && ls -R

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}/
# Copy app to Docker Image
COPY src ${LAMBDA_TASK_ROOT}/src
