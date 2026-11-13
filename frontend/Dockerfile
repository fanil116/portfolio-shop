FROM node:24-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
# Скрипты (nuxt prepare, git-хуки) запускаются после копирования исходников
RUN npm ci --ignore-scripts

COPY . .
RUN npx nuxt prepare && npm run build


FROM node:24-alpine AS final

ARG USER_ID=1901
ARG GROUP_ID=1901
RUN addgroup -g ${GROUP_ID} appgroup && \
    adduser -u ${USER_ID} -G appgroup -S -D -h /app appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/.output /app/.output
COPY --chown=appuser:appgroup entrypoint.production.sh /app/entrypoint.production.sh

RUN chmod +x /app/entrypoint.production.sh && \
    mkdir -p /app/nuxt_volume && \
    chown appuser:appgroup /app/nuxt_volume

USER appuser
ENV NODE_ENV=production \
    HOST=0.0.0.0 \
    PORT=3000

EXPOSE 3000

ENTRYPOINT ["/app/entrypoint.production.sh"]
CMD ["node", ".output/server/index.mjs"]
