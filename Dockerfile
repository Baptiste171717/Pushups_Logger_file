# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION= 3.10
ARG INSTALL_NODE_VERSION=20

FROM node:20-buster-slim AS node
FROM python:3.10-slim-buster AS builder

WORKDIR /app

COPY --from=node /usr/local/bin/ /usr/local/bin/
COPY --from=node /usr/lib/ /usr/lib/
# See https://github.com/moby/moby/issues/37965
RUN true
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY package.json ./
RUN npm install

COPY pushups_logger pushups_logger
COPY webpack.config.js autoapp.py ./
COPY assets assets
COPY instance instance
COPY .env.example .env

RUN npm run-script build

EXPOSE 2992
EXPOSE 5000

CMD ["npm", "start"]