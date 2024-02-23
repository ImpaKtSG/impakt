FROM oven/bun:1.0.29

WORKDIR /app

COPY . .

ENV NODE_ENV=development
RUN bun i --frozen-lockfile 

EXPOSE 3000
CMD ["bun", "run", "dev"]