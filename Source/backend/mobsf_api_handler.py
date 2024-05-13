import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

DEFAULT_SERVER = "http://localhost:8000"
DEFAULT_API = "e4184916a87a19dedcc0c500e9e3db4f2ec7752819b569d6fb4a37d665fbcf79"


class MobSFAPIHandler:
    def __init__(self, apikey=None, server=None):
        self.__server = server.rstrip("/") if server else DEFAULT_SERVER
        self.__apikey = apikey if apikey else DEFAULT_API

    def upload(self, file):
        multipart_data = MultipartEncoder(fields={"file": (file, open(file, "rb"), "application/octet-stream")})
        headers = {
            "Content-Type": multipart_data.content_type,
            "Authorization": self.__apikey,
        }

        r = requests.post(f"{self.__server}/api/v1/upload", data=multipart_data, headers=headers)
        return r.json()

    def scan(self, filename, scanhash):
        post_dict = {
            "scan_type": "apk",
            "file_name": filename,
            "hash": scanhash,
            "re_scan": False,
        }

        headers = {"Authorization": self.__apikey}

        r = requests.post(f"{self.__server}/api/v1/scan", data=post_dict, headers=headers)
        return r.json()

    def report_pdf(self, scanhash, pdfname=None):
        pdfname = pdfname if pdfname else "report.pdf"

        headers = {"Authorization": self.__apikey}
        data = {"hash": scanhash}

        r = requests.post(f"{self.__server}/api/v1/download_pdf", data=data, headers=headers, stream=True)

        with open(pdfname, "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)

        return pdfname

    def report_json(self, scanhash):
        headers = {"Authorization": self.__apikey}
        data = {"hash": scanhash}

        r = requests.post(f"{self.__server}/api/v1/report_json", data=data, headers=headers)
        return r.json()

    def scorecard(self, scanhash):
        headers = {"Authorization": self.__apikey}
        data = {"hash": scanhash}

        r = requests.post(f"{self.__server}/api/v1/scorecard", data=data, headers=headers)
        return r.json()

    def delete_scan(self, scanhash):
        headers = {"Authorization": self.__apikey}
        data = {"hash": scanhash}

        r = requests.post(f"{self.__server}/api/v1/delete_scan", data=data, headers=headers)
        return r.json()
