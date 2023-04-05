FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/CrossZeros

COPY requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY CrossZeros ./CrossZeros

CMD ["python", "-m", "CrossZeros"]

# -------------------------------
# Build an image from a Dockerfile:
# $ docker build -t cross_zeros .
# -------------------------------
# Create and run a new container from an image:
# $ docker run -d --name CrossZeros cross_zeros
# -------------------------------
# Stop running container:
# $ docker stop CrossZeros
# -------------------------------
# Start stopped container:
# $ docker start CrossZeros
# -------------------------------
# Remove container:
# $ docker rm CrossZeros
# -------------------------------
# Remove image:
# $ docker rmi CrossZeros
# -------------------------------
# Execute a command in a running container:
# $ docker exec -it CrossZeros bash
