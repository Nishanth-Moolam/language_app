FROM node:19-alpine

COPY language-fe /app/

WORKDIR /app

RUN npm install

CMD ["npm", "start"]