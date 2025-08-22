# Stage 1 — Build React App
FROM node:18 AS build

WORKDIR /app

# Copy package files first for caching
COPY package*.json ./
COPY tsconfig.json ./
COPY vite.config.ts ./

# Install dependencies
RUN npm install

# Copy all source code
COPY . .

# Build Vite app
RUN npm run build

# Stage 2 — Production Image with Nginx
FROM nginx:stable-alpine

# Copy build output to Nginx HTML folder
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
