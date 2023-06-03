# Use official node image as the base image
FROM node:14.17.6 as build

# Set the working directory
WORKDIR /usr/local/app

# Add the source code to app
COPY language-fe /usr/local/app

# Install all the dependencies
RUN npm install

# Generate the build of the application
RUN npm run build

# Use official nginx image as the base image
FROM nginx:latest

# Copy the build output to replace the default nginx contents.
COPY --from=build /usr/local/app/dist/language-fe /usr/share/nginx/html

# Expose port 80
EXPOSE 80