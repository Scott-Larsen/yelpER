from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import api_key
from jsonmerge import Merger
from math import sqrt

def yelpER():
  # define our headers
  header = {'Authorization':'bearer {}'.format(api_key),
  'Content-Type':"application/json"}

  # Build the request framework
  transport = RequestsHTTPTransport(url='https://api.yelp.com/v3/graphql', headers=header, use_json=True)

  # Create the client
  client = Client(transport=transport, fetch_schema_from_transport=True)

  restaurants = []

  # search(term: "restaurants", location: "Corvallis, OR" radius:30000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: "Eugene, OR" radius:40000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", latitude: 44.051837, longitude: -123.087199, radius:40000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: Cottage Grove, OR, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: "97424", limit: 50, offset: ''' + str(i * 50) + ''')

  gps1 = [34.149827, -118.021034]
  gps2 = [34.062720, -118.274116]
  # 25.21km between these two points

  # Distance between GPS Points
  # distance = sqrt((gps2[0] - gps1[0]) ** 2 + (gps2[1] - gps1[1]) ** 2)
  # 25.21km ~= 0.26765299955913757
  # print(0.26765299955913757 / 25.21)
  # 1km ~= 0.010616937705638142
  # print(distance)

  n = 10
  latFactor = ((gps1[0] - gps2[0]) / n)
  longFactor = ((gps1[1] - gps2[1]) / n)

  gps = []
  for i in range(n):
      lat = gps1[0] + latFactor * i
      long = gps1[1] + longFactor * i
      gps.append([lat, long])

  print(gps)

  for i in range(n):
    q = ('''

    {
        search(term: "restaurants", latitude: ''' + str(gps[i][0]) + ", longitude: " + str(gps[i][1]) + ''', limit: 20) {
                total
                business {
                    name
                    rating
                    location {
                        address1
                      address2
                        city
                        state
                        postal_code
                    }
                  coordinates {
                    latitude
                    longitude
                  }
                  phone
                  categories {
                    title
                    alias
                  }
            }
        }
    }

  #   ''')

    # define a simple query
    query = gql(q)

    response_query = client.execute(query)
    # print(response_query)

    # Strip the extra headers
    # rq += response_query
    rq = response_query['search']['business']
    # print(rq)

    restaurants += rq

    # print(response_query)
    # print(rq)
  print(restaurants[0])

    # # execute and print this query
    # print('-'*3000)
  # print('-'*3000)
    # print(client.execute(query))

    # # 15:11
  return restaurants