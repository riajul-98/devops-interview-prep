FROM python:3.11-slim

LABEL maintainer="moabukar"
LABEL description="DevOps Interview Prep CLI - Master Your Next DevOps Interview"
LABEL version="1.0.0"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -e .

RUN useradd --create-home --shell /bin/bash devops-interviewer && \
    chown -R devops-interviewer:devops-interviewer /app

USER devops-interviewer

ENTRYPOINT ["devops-ip"]
CMD ["--help"]