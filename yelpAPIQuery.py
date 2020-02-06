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

  restaurants = []

  # search(term: "restaurants", location: "Corvallis, OR" radius:30000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: "Eugene, OR" radius:40000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", latitude: 44.051837, longitude: -123.087199, radius:40000, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: Cottage Grove, OR, limit: 50, offset: ''' + str(i * 50) + ''')
  # search(term: "restaurants", location: "97424", limit: 50, offset: ''' + str(i * 50) + ''')

  # 25.21km between these two points

  # Distance between GPS Points
  # distance = sqrt((gps2[0] - gps1[0]) ** 2 + (gps2[1] - gps1[1]) ** 2)
  # 25.21km ~= 0.26765299955913757
  # print(0.26765299955913757 / 25.21)
  # 1km ~= 0.010616937705638142
  # print(distance)

  n = 10
  latFactor = (abs(gps1[0] - gps2[0]) / n)
  longFactor = (abs(gps1[1] - gps2[1]) / n)

  gps = []

  minLat, minLong = min(gps1[0], gps2[0]), min(gps1[1], gps2[1])
  
  for i in range(n):
      lat = minLat + latFactor * i
      long = minLong + longFactor * i
      gps.append([lat, long])

  print(f"GPS: {gps}")

  for i in range(n):
    print(f"i = {i}\n{gps[i][0]}\n{gps[i][1]}")

    q = ('''

    {
          search(term: "restaurants", latitude: ''' + str(gps[i][0]) + ", longitude: " + str(gps[i][1]) + ''', limit: 20) {
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

    restaurants += rq

    print(restaurants[0]['name'], restaurants[-1]['name'])

    # print(response_query)
    # print(rq)
  # print(restaurants[0])

    # # execute and print this query
    # print('-'*3000)
  # print('-'*3000)
    # print(client.execute(query))

    # # 15:11
  return restaurants