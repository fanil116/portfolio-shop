FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf

# Шаблоны из /etc/nginx/templates рендерятся через envsubst при старте контейнера
# (подставляются только объявленные переменные окружения, $host и т.п. не трогаются).
COPY templates/ /etc/nginx/templates/
COPY includes/ /etc/nginx/includes/
COPY 40-admin-htpasswd.sh /docker-entrypoint.d/40-admin-htpasswd.sh

RUN chmod +x /docker-entrypoint.d/40-admin-htpasswd.sh

ENV SITE_HOST=localhost \
    ADMIN_HTPASSWD=override_if_needed

EXPOSE 80/tcp
