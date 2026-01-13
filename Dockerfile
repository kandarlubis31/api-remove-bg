# Gunakan Python Image
FROM python:3.9

# Set working directory
WORKDIR /code

# Copy requirements & Install
COPY ./requirements.txt /code/requirements.txt
# Install library sistem yg dibutuhkan rembg
RUN apt-get update && apt-get install -y libgl1
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy codingan
COPY . .

# Buat folder cache untuk model u2net biar gak download ulang terus
RUN mkdir -p /home/user/.u2net

# Jalankan server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]