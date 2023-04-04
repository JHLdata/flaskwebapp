from flask import Flask, render_template, request
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

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
                                   select="Title,Ingredients,Instructions")

    # Extract the search results
    results = []
    for result in search_results:
        recipe = {
            'Title': result['Title'],
            'Ingredients': result['Ingredients'],
            'Instructions': result['Instructions']
        }
        results.append(recipe)

    # Render the search results template with the list of results
    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)

