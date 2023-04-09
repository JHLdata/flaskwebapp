from flask import Flask, render_template, request
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobClient

BLOB_URL = "https://foodimagestorage.blob.core.windows.net/foodimages/"

connect_str = 'DefaultEndpointsProtocol=https;AccountName=foodimagestorage;AccountKey=CnZCPsj3CUu8UpqfakzO/INzfYcIvyJb+Ap+E4MzEtlHIHrLx1L+ynCw/Li2YnwwsC/F7sHuxNb7+AStrppYRQ==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = 'foodimages'
container_client = blob_service_client.get_container_client(container_name)

# Replace with your search service URL and API key
SEARCH_ENDPOINT = "https://search-web-static-1.search.windows.net/"
SEARCH_API_KEY = "0lj9J6Y7KQh1VUgPbgmdi93R3vpScRlpUqAHTmwIJ4AzSeCltvAb"

app = Flask(__name__)

# Define the home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define the search results route
@app.route('/search')
def search():
    # Get the query entered in the search bar
    query = request.args.get('q')

    # Create a SearchClient to connect to the Azure Search service
    credential = AzureKeyCredential(SEARCH_API_KEY)
    client = SearchClient(endpoint=SEARCH_ENDPOINT,
                          index_name='food-data',
                          credential=credential)

    # Build the search query
    search_results = client.search(search_text=query,
                                   filter="",
                                   select="Title,Ingredients,Instructions,Image_Name")

    # Extract the search results
    results = []
    for result in search_results:
        ingredients = result['Ingredients'].split(",")
        ingredients[0] = ingredients[0].lstrip("[")
        ingredients[-1] = ingredients[-1].rstrip("]")
        recipe = {
            'Title': result['Title'],
            'Ingredients': ingredients,
            'Instructions': result['Instructions'],
            'ImageURL': BLOB_URL + result['Image_Name'] + ".jpg"
        }
        # get the corresponding image from Blob Storage
        #blob_client = container_client.get_blob_client(result['Image_Name'])
        #recipe['image_url'] = blob_client.url
        results.append(recipe)

    # Render the search results template with the list of results
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)