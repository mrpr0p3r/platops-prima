#build stage
FROM python:3.13 as build
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

#runtime stage
FROM python:3.13
WORKDIR /app
COPY --from=build /root/.local/lib/python3.13/site-packages /root/.local/lib/python3.13/site-packages

COPY --from=build /root/.local /root/.local
COPY . .
ENV FLASK_APP=./index.py
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]