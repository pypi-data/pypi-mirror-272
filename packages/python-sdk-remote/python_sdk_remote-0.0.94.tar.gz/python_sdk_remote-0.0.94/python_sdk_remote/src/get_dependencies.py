# pip install BeautifulSoup4 requests importlib-metadata
import subprocess
import sys
import json
from collections import defaultdict

import importlib_metadata
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Union
import os


def install(packages):
    print("Installing...", packages)
    if isinstance(packages, str):
        packages = [packages]
    # for package in packages:
    #     # We can't install multiple packages in a single command, because pip will stop at the first error
    #     subprocess.run([sys.executable, "-m", "pip", "install", "-U", "--no-deps", package], check=False)
    subprocess.run([sys.executable, "-m", "pip", "install", "-U", "--no-deps"] + packages, check=False)



def get_dependencies_per_package(include_packages):
    dependencies_per_package = defaultdict(list)
    for dist in importlib_metadata.distributions():
        package_name = dist.metadata['Name']
        if package_name not in include_packages:
            continue

        dependencies = dist.metadata.get_all('Requires-Dist', [])
        for dependency in dependencies:
            depend_on = dependency.split()[0]
            if depend_on in include_packages and depend_on not in dependencies_per_package[package_name]:
                dependencies_per_package[depend_on].append(package_name)

    for package in include_packages:
        if package not in dependencies_per_package:
            dependencies_per_package[package] = []
    return dependencies_per_package


def get_included_packages():
    url = "https://pypi.org/user/circles/"
    class_name = "package-snippet__title"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    package_names = soup.find_all("h3", class_=class_name)
    included_packages = [package_name.text for package_name in package_names]
    return included_packages

# def build_dependency_tree(dependencies_per_package: Dict[str, List[str]]) -> List[Union[str, Dict[str, List[Union[str, Dict]]]]]:
#     called = set()
#     def build_tree(package: str) -> Union[str, Dict[str, List[Union[str, Dict]]]]:
#         if package in called:
#             return package
#         called.add(package)
#         if package not in dependencies_per_package:
#             return package
#         return {package: [build_tree(dep) for dep in dependencies_per_package[package]]}
#
#     trees = []
#     for package in dependencies_per_package:
#         trees.append(build_tree(package))
#
#     return trees
#
# printed = []
#
# def display_dependency_tree(tree: Union[str, Dict[str, List[Union[str, Dict]]]], indent: int = 0) -> None:
#     if isinstance(tree, dict):
#         for package, dependencies in tree.items():
#             if package not in printed:
#                 print("-" * indent + package)
#                 printed.append(package)
#                 for dep in dependencies:
#                     display_dependency_tree(dep, indent + 1)
#     else:
#         if tree not in printed:
#             print("-" * (indent + 1) + tree)
#             printed.append(tree)

def main():
    # otherwise pip raise
    remove = """CirclesS3Storage
age-detection-local-python-package
rest-api-vacancy-scraper-local
recruitment-employer-local-python-package
local-logger-python-backend
local-age-detection-python-backend
age-detection
external-user-local
message-send-platform-invitation
profile-instagram
smartlink-restapi-python-serverless-com
profile-reddit-local-restapi-imp-python-package
operational-hours-local-python-package-local
Age-detection
CirclesGenderDetectorPython
business-profile-yelp-local-python
profile-yelp-local-python-circles
OpenCage-local
circles-bert-local
community-waiting-list-local-python-package
contact-locations-local
contact-user-external-local
dialog-workflow
dialog-workflow-local-python-package
local-dialog-workflow-python-backend
email-local
item-local-python-package-local
labels-local
location-profile-local-python-package-local
phone-local
profile-instagram-graphql-imp-local-python-package-local
profile-zoominfo-graphql-imp
real-estate-realtor.com-imp-local
recruitment-employer-monster-com-indeed-com-vacancy-scraper-local
sms-message-aws-local-python-package
variable-local-python-package
circles-bert-local""".splitlines()
    # too_popular = ["logger-local", "database-mysql-local", "python-sdk-remote", "url-remote", "user-context-remote", "language-remote", "database-infrastructure-local"]
    # remove += too_popular
    add = ['profiles-local', 'database-without-orm-local',
           'python-sdk-local', 'url-local']
    if os.path.exists('dependencies.json'):
        print("getting from dependencies.json")
        with open('dependencies.json', 'r') as f:
            dependencies_per_package = json.load(f)
        with open('dependencies.json', 'w') as f:
            json.dump(dependencies_per_package, f, indent=4, sort_keys=True)
    else:
        include_packages = get_included_packages()
        include_packages = [package for package in include_packages if package not in remove]
        install(include_packages)
        include_packages += add
        dependencies_per_package = get_dependencies_per_package(include_packages)
        print("writing to dependencies.json")
        with open('dependencies.json', 'w') as f:
            json.dump(dependencies_per_package, f, indent=4, sort_keys=True)

    # clean dependencies_per_package keys and values
    for package in list(dependencies_per_package.keys()):
        if package in remove:
            dependencies_per_package.pop(package)
        else:
            dependencies_per_package[package] = [dep for dep in dependencies_per_package[package]
                                                 if dep not in remove]

    print("num of edges per node, sorted by num of edges:")
    for package, dependencies in sorted(dependencies_per_package.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{package}: {len(dependencies)}")
    #
    # dependency_trees = build_dependency_tree(dependencies_per_package)
    # for tree in dependency_trees:
    #     display_dependency_tree(tree)

def plot_graph(dependencies_per_package: Dict[str, List[str]]):
    import networkx as nx
    import matplotlib.pyplot as plt

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes (packages) to the graph
    for package in dependencies_per_package:
        G.add_node(package)

    # Add edges (dependencies) to the graph
    for package, dependencies in dependencies_per_package.items():
        for dep in dependencies:
            G.add_edge(dep, package)

    # nx.kamada_kawai_layout, nx.circular_layout, nx.shell_layout, nx.spectral_layout
    # nx.random_layout, nx.spring_layout, nx.spiral_layout
    # error: nx.planar_layout, nx.planar_layout, nx.bipartite_layout, nx.rescale_layout, nx.multipartite_layout

    # max_len = max(len(dependencies) for dependencies in dependencies_per_package.values())
    # def weight_func(v, u, e):
    #     return  0.2 * (len(dependencies_per_package.get(v, [])) + len(dependencies_per_package.get(u, [])))
    #
    # pos = nx.kamada_kawai_layout(G, scale=2, weight=weight_func)

    pos = nx.circular_layout(G)
    # Draw the graph
    plt.figure(figsize=(20, 15))  # Increase the figure size
    nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=6, font_color="black", node_size=1000, width=1,
            edge_color="gray", arrowsize=5)
    plt.axis("off")  # Hide the axes
    plt.tight_layout()  # Adjust the layout to fit the figure

    # Save the plot as an image file
    print("Saving to dependencies_tree.png")
    plt.savefig("dependencies_tree.png", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
