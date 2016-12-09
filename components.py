import os
import urllib
import requests

# ----

# This component
NAME = os.getenv("SDC_LION", "sdc-lion")

# The set of components we want to allow calls from:
SDC_GIRAFFE = os.getenv("SDC_GIRAFFE", "sdc-giraffe")
components = [
    SDC_GIRAFFE
]

# The URL pattern that will be used to turn component names into links
url_pattern = os.getenv("URL_PATTERN", "https://{}.herokuapp.com/")

# ----

# Set up

# The set of URLs for the components we want to we want to allow calls from:
urls = {}

# The set of public keys for those components
public_keys = {}

for component in components:
    # Compute links
    urls[component] = url_pattern.format(component)
    # Initialise empty dict of keys
    public_keys[component] = {}

print("Configured components: " + repr(urls))

# ----


def __key_url(component, key_id):
    url = urllib.parse.urlparse(urls[component])
    parts = urllib.parse.ParseResult(
        scheme=url.scheme,
        netloc=url.netloc,
        path='/keys',
        params='',
        query=urllib.parse.urlencode({"id": key_id}),
        fragment=None
    )
    return urllib.parse.urlunparse(parts)


def __request_key(component, key_id):
    url = __key_url(component, key_id)
    print("Attempting to get key " + repr(key_id) + " from " + repr(component) + " at " + repr(url))
    response = requests.get(url)
    if response.status_code == 200:
        # We should have the expected Json response
        keys = response.json()
        print("Got key(s): " + repr(keys))
        if repr(key_id) in keys:
            public_keys[component][key_id] = keys[repr(key_id)]
            print("Found key id " + repr(key_id) + " for component " + repr(component))
        else:
            print("Key id " + repr(key_id) + " not found for component " + repr(component))
    else:
        print("Unexpected response from " + repr(component) + ": " + repr(response.status_code))


def get_key(component, key_id):
    key = None

    # Do we allow this component to talk to us?
    if component in components:

        # Fetch and cache the key if necessary
        if key_id not in public_keys[component]:
            __request_key(component, key_id)
        else:
            print("Using cached key " + repr(key_id) + " for component " + repr(component))

        # Get the key from the cache
        if key_id in public_keys[component]:
            key = public_keys[component][key_id]
        else:
            print("Unable to get key id " + repr(key_id) +
                  " from " + repr(component) +
                  " (at " + repr(__key_url(component, key_id)) + ")")
    else:
        print("Component " + repr(component) + " is not a recognised client.")

    #print("Key cache is:\n" + repr(public_keys))
    #print("Selected key is:\n" + repr(key))
    return key
