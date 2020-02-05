from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import api_key
from jsonmerge import Merger

def yelpAPIQuery(gps1, gps2):

  # define our headers
  header = {'Authorization':'bearer {}'.format(api_key),
  'Content-Type':"application/json"}

  # Build the request framework
  transport = RequestsHTTPTransport(url='https://api.yelp.com/v3/graphql', headers=header, use_json=True)

  # Create the client
  client = Client(transport=transport, fetch_schema_from_transport=True)

  cityList = []

  # search(term: "restaurants", location: "Corvallis, OR" radius:30000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: "Eugene, OR" radius:40000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", latitude: 44.051837, longitude: -123.087199, radius:40000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: Cottage Grove, OR, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: "97424", limit: 50, offset: ''' + str(i * 50) + ''')

  for i in range(len()):
    q = ('''

    {
        search(term: "restaurants", location: "Springfield, OR", limit: 20, offset: ''' + str(i * 50 + 1) + ''') {
                business {
                  photos
                    name
                    url
                    phone
                    display_phone
                  rating
                  review_count                 
                    location {
                        address1
                      address2
                        city
                        state
                        postal_code
                    }
                    price
                  coordinates {
                    latitude
                    longitude
                  }
                  categories {
                    title
                    alias
                  }
                  reviews {
                    text
                    }
            }
        }
    }

    ''')

    # define a simple query
    query = gql(q)

    response_query = client.execute(query)
    # print(response_query)

    # Strip the extra headers
    # rq += response_query
    rq = response_query['search']['business']
    # print(rq)

    cityList += rq

    # print(response_query)
    # print(rq)
  print(cityList[0])

    # # execute and print this query
    # print('-'*3000)
  # print('-'*3000)
    # print(client.execute(query))

    # # 15:11
  return cityList