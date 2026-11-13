FROM python:3.13-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/

# Для production передаётся "--no-dev"
ARG UV_SYNC_ARGS=""

WORKDIR /app
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project ${UV_SYNC_ARGS}
COPY . /app
RUN chmod +x entrypoint.* wait-for


FROM python:3.13-alpine AS final

ARG APP_USER_UID=1001
ARG APP_USER_GID=1001

RUN addgroup -g ${APP_USER_GID} -S appgroup && \
    adduser -u ${APP_USER_UID} -S appuser -G appgroup

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/
COPY --from=builder /app /app

RUN mkdir -p /app/static/ /app/media/ && \
    chown -R appuser:appgroup /app

WORKDIR /app
USER appuser
# UV_NO_SYNC: `uv run` использует уже собранный .venv и не доустанавливает пакеты
# при старте (иначе в prod-образе с --no-dev подтягивалась бы dev-группа)
ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    UV_NO_SYNC=1
