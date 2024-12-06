# Use the Ultralytics base image
FROM ultralytics/ultralytics:latest

# Install additional Python packages if needed
RUN pip install numpy==1.23.5 tqdm xmltodict

# Set the working directory in the container
WORKDIR /app

# Copy the entire application directory into the container
COPY . /app

# You can add additional directory setup if required by your application, e.g.,
RUN mkdir -p /app/data
RUN mkdir -p /app/outputs

# Set the default command to something neutral; this can be overridden at runtime
CMD ["/bin/bash"]
