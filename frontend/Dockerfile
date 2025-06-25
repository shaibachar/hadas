# Use an official Node.js runtime as a parent image
FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

# Build the production-optimized React app
RUN npm run build

# Install serve to serve the build directory
RUN npm install -g serve

# Copy only the build output for a smaller image
FROM node:20-alpine as production
WORKDIR /app
COPY --from=0 /app/build ./build
RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
