from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from urllib.parse import urlparse
import os


from network import RegistryClient

client = RegistryClient.RestClient(os.environ['REGISTRY_HOST'])

app = Flask(__name__)


def parent_url(url, current_segments):
    return url[0:url.index(current_segments)]


@app.route('/favicon.ico')
def favicon():
    print(os.path.join(app.root_path, 'static'))
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    repositories = client.list_repositories()
    return render_template('index.html', registry_info=os.environ['REGISTRY_HOST'], repositories=repositories)


@app.route('/<path:repository_name>/')
def repository(repository_name):
    parent = parent_url(request.url, repository_name)
    raw_repo = client.get_repository(repository_name)
    return render_template('repository.html', parent=parent, repository_name=raw_repo.get("name"),
                           repository_tags=raw_repo.get("tags"))


@app.route('/<path:repository_name>/:<path:tag>')
def image(repository_name, tag):
    parent = parent_url(request.url, ':' + tag)
    rsp = client.get_manifest(repository_name, tag)
    raw_image = rsp.content()

    return render_template('image.html', parent=parent, registry_host=urlparse(os.environ['REGISTRY_HOST']).netloc,
                           image_name=raw_image.get('name'),
                           image_tag=raw_image.get('tag'),
                           image_digest=rsp.headers()["Docker-Content-Digest"])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
