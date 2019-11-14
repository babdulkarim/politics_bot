FROM grahamdumpleton/mod-wsgi-docker:python-3.5

RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

ADD . / app/

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		python3-pip \
		python3-dev \
		unattended-upgrades && \
	rm -r /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip install \
	"requests==2.22.0" \
	"bs4==0.0.1" \
	"lxml==4.4.1"

ENV LANG=en_US.UTF-8 PYTHONHASHSEED=random \
    PATH=/usr/local/python/bin:/usr/local/apache/bin:$PATH

WORKDIR /app
