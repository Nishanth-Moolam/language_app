FROM node:19-alpine

COPY language-fe /app/

WORKDIR /app

RUN npm install -g npm@9.6.7

RUN npm install

CMD npm start