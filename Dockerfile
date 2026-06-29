FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
ENV PYTHONPATH=/app/src

RUN apt-get update \
    && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

RUN rm -f /etc/nginx/sites-enabled/default

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh


EXPOSE 80

CMD ["/app/start.sh"]