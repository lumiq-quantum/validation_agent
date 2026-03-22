FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY validation_agent/ validation_agent/

EXPOSE 8001

CMD ["uvicorn", "validation_agent.agent:a2a_app", "--host", "0.0.0.0", "--port", "8001"]
