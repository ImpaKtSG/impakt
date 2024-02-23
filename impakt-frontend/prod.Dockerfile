FROM oven/bun:1.0.29 AS build

WORKDIR /app

COPY . .

ENV NODE_ENV=production
RUN bun i --frozen-lockfile
RUN bun run build

FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]