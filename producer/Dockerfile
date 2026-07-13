FROM python:3.13-slim

#crea cartella app 
WORKDIR /app 

#copia i requirements e li installa in ambiente
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# copia contenuto di /src
COPY src/ .

# all'avvio fa partire main.py ovvero il producer
CMD ["python", "main.py"]