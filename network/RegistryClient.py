import sys

from network.Request import Request

__author__ = 'wangc31'

# media type
MEDIA_TYPE_DM_JSON = 'application/vnd.emc.documentum+json'
MEDIA_TYPE_HOME_JSON = 'application/home+json'
MEDIA_TYPE_OCTET_STREAM = 'application/octet-stream'


class RestClient:
    def __init__(self, root_context):
        self.root_context = root_context

    def verify(self):
        rsp = self._get()
        version_header = rsp.headers()["Docker-Distribution-Api-Version"]
        if not (200 == rsp.status() and version_header == "registry/2.0"):
            print("The Docker registry version is not supported.")
            sys.exit(0)

    def list_repositories(self, last=None, n=None):
        params = {}

        if last:
            params["last"] = last

        if n:
            params["n"] = n

        return self._get("/v2/_catalog", params=params).content().get("repositories")

    def get_repository(self, name):
        return self._get("/v2/<name>/tags/list".replace("<name>", name)).content()

    def get_manifest(self, name, tag):
        return self._get("/v2/<name>/manifests/<reference>".replace("<name>", name).replace("<reference>", tag))

    def delete_image(self, name, tag):
        return self._delete("/v2/<name>/manifests/<reference>".replace("<name>", name).replace("<reference>", tag))

    def next_page(self, response):
        return self._get(response.link_href())

    def _generate_request(self, href=None):
        if href is None:
            return Request(self.root_context)
        else:
            return Request(self.root_context + href)

    def _get(self, href=None, params=None):
        req = self._generate_request(href)
        return req.get(params=params)

    def _delete(self, href=None):
        req = self._generate_request(href)
        return req.delete()


def main():
    pass


if __name__ == '__main__':
    main()
else:
    print('RestClient as a module\n')
