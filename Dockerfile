FROM python
MAINTAINER Chen Wang "Chen.Wang@emc.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["docker_registry.py"]