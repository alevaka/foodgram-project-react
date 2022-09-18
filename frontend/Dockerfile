# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
COPY ./frontend/ ./
COPY ../docs/ ./
RUN npm install
RUN npm run build
COPY ./docs/ ./build/docs/
CMD cp -r build result_build
 