# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

extras_require = {
    "vanilla": [
        "mosaic-utils==1.0.1",
    ],
    "complete-with-utils": [
        "mosaic-utils[complete]==1.0.1"
    ],
    "complete": [
        "mosaic-utils[complete]==1.0.1",
    ],
    "utils_flavours": [
        "mosaic-utils[flavours]==1.0.1",
    ],
    "utils_common": [
        "mosaic-utils[common]==1.0.1",
    ],
    "utils_metrics": [
        "mosaic-utils[metrics]==1.0.1",
    ],
    "utils_k8": [
        "mosaic-utils[k8]==1.0.1",
    ],
    "common": [
        "mosaic-utils[nb-template-serving]==1.0.1",
        "importlib-resources==5.4.0",
        "Pillow==8.4.0",
    ],
}


setup(
    name="fosforml",
    package_dir={"fosforml":"fosforml"},
    version="1.0.0",
    description="REST API client for Fosfor AI",
    url="https://gitlab.fosfor.com/fosfor-decision-cloud/intelligence/mosaic-ai-client.git",
    author="Rakesh Gadiparthi",
    author_email="rakesh.gadiparthi@fosfor.com",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cloudpickle==1.6.0",
        "requests_toolbelt==0.9.1",
        "shutils==0.1.0",
        "PyYAML==6.0",
        "mosaic-utils",
	"urllib3==1.26.15"
    ],
    extras_require=extras_require,
)
 
