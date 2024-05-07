import setuptools

long_description = None
with open("README.txt","r",encoding="utf8") as f:
    long_description = f.read() 

setuptools.setup(
    name = "rdb_json_parser",
    version = "0.3",
    author = "Nikunj Pathak",
    author_email = "nik.twister@gmail.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ["rdb_json_parser"]
)

