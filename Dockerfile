# Python बेस इमेज
FROM python:3.9-slim

# ऑडियो प्रोसेसिंग के लिए जरूरी लाइब्रेरीज
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# वर्किंग डायरेक्टरी सेट करें
WORKDIR /app

# dependencies इंस्टॉल करें
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ऐप कॉपी करें
COPY . .

# पोर्ट एक्सपोज़ करें
EXPOSE 8080

# ऐप चलाएं (बड़े मॉडल के लिए टाइमआउट बढ़ाया)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "app:app"]
