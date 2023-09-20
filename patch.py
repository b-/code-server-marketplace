#!/usr/bin/env python3

################
## Set this to where you have code-server installed. 
## The below is the default path for most installations.
## If you're running code-server on Docker, you'll probably
## have to do something a little bit different.
################
import sys
import json
import os

hello_text = '''patch.py
Based on the AUR packages code-marketplace and code-features
'''

help_text = ''' usage: sudo " + sys.argv[0] + " (patch | restore) [/usr/lib/code-server]

'''
path_text = ''' if you don't have code-server installed in /usr/lib/code-server,
  set the path with the second argument, or edit patch.py.
'''

print(hello_text)

if len(sys.argv) == 1:
    print(help_text + path_text)
    exit(1)

product_json_subpath ="lib/vscode/product.json"
if len(sys.argv) == 3:
    code_server_path = sys.argv[3]
else:
    code_server_path = "/usr/lib/code-server/"
product_path = os.path.join(code_server_path, product_json_subpath)
if not os.path.exists(product_path):
    print('product.json not found. ' + path_text)
    exit(64)

script_dir = os.path.dirname(__file__)
patch_file = "patch.json"
patch_path = os.path.join(script_dir, patch_file)
cache_file = "cache.json"
cache_path = os.path.join(script_dir, cache_file)
operation = sys.argv[1]

if not os.path.exists(cache_path):
    with open(cache_path, 'w') as file:
        file.write("{}")

if not os.path.exists(patch_path):
    print('please download the whole package and try again!')
    exit(32)

def patch():
    with open(product_path, "r") as product_file:
        product_data = json.load(product_file)
    with open(patch_path, "r") as patch_file:
        patch_data = json.load(patch_file)
    cache_data = {}
    for key in patch_data.keys():
        if key in product_data:
            cache_data[key] = product_data[key]
        product_data[key] = patch_data[key]
    with open(product_path, "w") as product_file:
        json.dump(product_data, product_file, indent='\t')
    with open(cache_path, "w") as cache_file:
        json.dump(cache_data, cache_file, indent='\t')

def restore():
    with open(product_path, "r") as product_file:
        product_data = json.load(product_file)
    with open(patch_path, "r") as patch_file:
        patch_data = json.load(patch_file)
    with open(cache_path, "r") as cache_file:
        cache_data = json.load(cache_file)
    for key in patch_data.keys():
        if key in product_data:
            del product_data[key]
    for key in cache_data.keys():
        product_data[key] = cache_data[key]
    with open(product_path, "w") as product_file:
        json.dump(product_data, product_file, indent='\t')

if operation == "patch":
    patch()
elif operation == "restore":
    restore()
