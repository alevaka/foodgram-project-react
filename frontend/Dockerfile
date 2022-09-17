# build env
FROM node:13.12.0-alpine as build
RUN echo "$PWD"
WORKDIR /app
RUN echo $(ls)
COPY package*.json ./
RUN echo $(ls)
COPY ./frontend/ ./
RUN echo $(ls)
RUN npm install
RUN echo "$PWD"
RUN echo $(ls)
RUN npm run build
CMD cp -r build result_build
