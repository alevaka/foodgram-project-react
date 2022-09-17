# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN echo "-----FILES------"
RUN echo "$PWD"
RUN echo ls
RUN npm run build
CMD cp -r build result_build
