FROM wangsiqian/python-driver:3.10

WORKDIR /opt/app
ENV PYTHONPATH="${PYTHONPATH}:/opt/app" \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONUNBUFFERED=1

# Install dependencies via poetry, 先安装依赖再复制代码
COPY src/pyproject.toml src/poetry.lock  /opt/app/

RUN poetry config virtualenvs.create false &&  \
    poetry install -vvv --no-dev --no-interaction --no-ansi || \
    poetry install -vvv --no-dev --no-interaction --no-ansi

COPY src/ /opt/app
