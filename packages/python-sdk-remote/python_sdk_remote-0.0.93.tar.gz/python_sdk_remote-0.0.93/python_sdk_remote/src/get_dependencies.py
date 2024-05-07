# pip install BeautifulSoup4 requests importlib-metadata
import subprocess
import sys
import json
from collections import defaultdict

import importlib_metadata
import requests
from bs4 import BeautifulSoup


def install(packages):
    print("Installing...", packages)
    if isinstance(packages, str):
        packages = [packages]
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "--no-deps"] + packages, check=False)
    except Exception as e:
        print(e)


def get_dependencies_per_package(include_packages):
    dependencies_per_package = defaultdict(list)
    for dist in importlib_metadata.distributions():
        package_name = dist.metadata['Name']
        if package_name not in include_packages:
            continue

        dependencies = dist.metadata.get_all('Requires-Dist', [])
        for dependency in dependencies:
            depend_on = dependency.split()[0]
            if depend_on in include_packages:
                dependencies_per_package[depend_on].append(package_name)

    return dependencies_per_package


def get_included_packages():
    url = "https://pypi.org/user/circles/"
    class_name = "package-snippet__title"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    package_names = soup.find_all("h3", class_=class_name)
    included_packages = [package_name.text for package_name in package_names]
    install(included_packages)
    return included_packages


def main():
    include_packages = get_included_packages()
    dependencies_per_package = get_dependencies_per_package(include_packages)
    with open('dependencies.json', 'w') as f:
        json.dump(dependencies_per_package, f, indent=4)


if __name__ == "__main__":
    main()
