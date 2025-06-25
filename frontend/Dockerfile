# Use official Node image as a builder
FROM node:18 as builder

WORKDIR /app

# Copy package files separately to leverage caching
COPY package*.json ./

RUN npm install

# Copy the rest of the source files
COPY . .

# Build the React app
RUN npm run build

# ------------------------------

# Use a lightweight image to serve the build
FROM node:18-slim

# Install only serve globally
RUN npm install -g serve

# Create app directory
WORKDIR /app

# Copy built app from builder
COPY --from=builder /app/build ./build

# Expose port (optional but good for documentation)
EXPOSE 3000

# Serve the app
CMD ["serve", "-s", "build", "-l", "3000"]
