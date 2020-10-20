# Main python image for Django
FROM python:3.8-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
		gettext \
		libxml2-dev \
		libxslt1-dev \
		libxmlsec1-dev \
		pkg-config \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

# Install required Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django app
COPY ./ .

EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

