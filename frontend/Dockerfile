# frontend/Dockerfile
FROM node:18

WORKDIR /app

COPY ./ ./

RUN npm install
RUN npm run build

# Serve React app with static file server
RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]
