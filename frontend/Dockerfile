# build env
FROM node:13.12.0-alpine as build
RUN echo "$PWD"
WORKDIR /app
COPY package*.json ./
COPY . ./
RUN npm install
RUN echo "-----FILES------"
RUN echo "$PWD"
RUN echo $(ls)
RUN npm run build
CMD cp -r build result_build
