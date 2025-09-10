# Dockerfile for Next.js frontend
FROM node:20-alpine

ENV NODE_ENV=production
ENV TZ=America/Santiago

WORKDIR /app

# Install dependencies based on package.json
COPY package.json package-lock.json* ./
RUN npm install --production --silent

# Copy the rest of the application code
COPY . .

# Build the Next.js app
RUN npm run build

# Expose the port used by the app
EXPOSE 8080

# Start the Next.js server
CMD ["npm", "start"]
