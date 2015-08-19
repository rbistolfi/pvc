import requests
import pyslapt
import json
import time
import logging


BASE_URL = "http://localhost:8001/api/1/package"


class PVCClient(object):

    def get(self, package_name):
        url = "{}/{}".format(BASE_URL, package_name)
        response =  requests.get(url)
        return response.json()

    def post(self, document):
        url = BASE_URL
        headers={"Content-Type": "application/json"}
        data = json.dumps(document, ensure_ascii=True)
        response = requests.post(url, data=data, headers=headers)
        logging.debug("Response: %s %s", response.status_code, response.content)
        return response.json()

    def put(self, resource_id, document, etag=None):
        url = "{}/{}".format(BASE_URL, resource_id)
        headers = {"Content-Type": "application/json"}
        if etag:
            headers["If-Match"] = etag
        data = json.dumps(document, ensure_ascii=True)
        response = requests.put(url, data=data, headers=headers)
        logging.debug("Response: %s %s", response.status_code, response.content)
        return response.json()


if __name__ == "__main__":

    available = pyslapt.Available()
    client = PVCClient()

    logging.info("Uploading available packages to REST service")

    for package in available:
        logging.info("Loading %s", package.name)

        # Get some data from package info, continue on errors
        try:
            version, arch, release = package.version.split("-")
            build, vector_version = release.split("vl")
        except:
            continue

        # Check if there is a document in the db already
        existing_document = client.get(package.name)
        document_id = existing_document.get("_id", None)

        if document_id:
            # Use existing document as base
            data = existing_document
        else:
            # Create a new base document
            data = {
                "name": package.name,
                "description": package.description,
                "category": package.location,
                "packages": []
            }

        # Create package data document
        package_data = {
            "repository": package.mirror,
            "url": package.mirror + package.location + "/{p.name}-{p.version}{p.file_ext}".format(p=package),
            "arch": arch,
            "build": build,
            "required": package.required,
            "release": "vl" + vector_version,
            "version": version,
            "filename": "{p.name}-{p.version}{p.file_ext}".format(p=package),
            "md5": package.md5,
            "compressed": package.size_c,
            "uncompressed": package.size_u,
        }

        # Check for dups
        if package_data in data["packages"]:
            continue

        # Add package data to document
        data["packages"].append(package_data)

        try:
            if document_id:
                # Update existing document
                logging.info("Updating existing entry")
                cleaned_data = {k: v for k, v in data.items() if not k.startswith("_")}
                etag = data.get("_etag", None)
                client.put(document_id, cleaned_data, etag=etag)
            else:
                # Create new document
                logging.info("Creating new entry")
                client.post(data)
        except UnicodeDecodeError:
            logging.error("Error loading package metadata: %s", data)

        # Be polite with server
        time.sleep(1)
