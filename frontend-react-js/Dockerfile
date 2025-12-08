FROM node:18-alpine

WORKDIR /app

# Install frontend dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend source code
COPY . .

EXPOSE 3000

CMD [ "npm", "start" ]

