from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from config import api_key
from jsonmerge import Merger
from geopy import distance
from math import log

def yelpAPIQuery(businessType, gps1, gps2):

  # define our headers
  header = {'Authorization':'bearer {}'.format(api_key),
  'Content-Type':"application/json"}

  # Build the request framework
  transport = RequestsHTTPTransport(url='https://api.yelp.com/v3/graphql', headers=header, use_json=True)

  # Create the client
  client = Client(transport=transport, fetch_schema_from_transport=True)

  businesses = []

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

  dist = distance.distance(gps1, gps2).m
  print(f"Distance - {dist}")

  numberOfQueryLocations = 7
  centerQueryRadiusRelativeToDistance = 1 / 8
  latIncrement = (abs(gps1[0] - gps2[0]) / (numberOfQueryLocations - 1))
  longIncrement = (abs(gps1[1] - gps2[1]) / (numberOfQueryLocations - 1))

  # gps = []

  minLat, minLong = min(gps1[0], gps2[0]), min(gps1[1], gps2[1])

  for i in range(numberOfQueryLocations):
    lat = minLat + latIncrement * i
    long = minLong + longIncrement * i
    # gps.append([lat, long])

    j = i if i < numberOfQueryLocations // 2 else numberOfQueryLocations - i - 1

    radius = int(dist * j * (centerQueryRadiusRelativeToDistance / (numberOfQueryLocations // 2)) + 1000)

    # print(f"i = {i}\n{gps[i][0]}\n{gps[i][1]}")
    print(f"{lat}, {long}, Radius: {int(radius / 1000)}, Radius (in miles): {int(radius * 0.000621371)}")

    q = ('''

    {
          search(term: "''' + str(businessType) + '", latitude: ' + str(lat) + ", longitude: " + str(long) + ", radius:" + str(radius) + ''', limit: 20) {
                  business {
                    id
                    name
                    photos
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

    businesses += rq

    # print(businesses[0]['name'], businesses[-1]['name'])

    # print(response_query)
    # print(rq)
  # print(businesses[0])

    # # execute and print this query
    # print('-'*3000)
  # print('-'*3000)
    # print(client.execute(query))

    # # 15:11

  uniqueBusinesses = { each['id'] : each for each in businesses }.values()

  print(f"# of businesses - {len(businesses)}")
  print(f"# of unique businesses - {len(uniqueBusinesses)}")


  minLat, maxLat, minLong, maxLong = False, False, False, False

  for b in uniqueBusinesses:
    # print(type(b['coordinates']['latitude']))
    if minLat == False or b['coordinates']['latitude'] < minLat:
      minLat = b['coordinates']['latitude']
    if maxLat == False or b['coordinates']['latitude'] > minLat:
      maxLat = b['coordinates']['latitude']
    if minLong == False or b['coordinates']['longitude'] < minLong:
      minLong = b['coordinates']['longitude']
    if maxLong == False or b['coordinates']['longitude'] > minLong:
      maxLong = b['coordinates']['longitude']

    curve, rating = (log(b['review_count']) + 4) / 7 if b['review_count'] < 20 else b['rating'], b['rating']
    # print(b['review_count'], curve, rating, curve * rating)

  print(minLat, maxLat, minLong, maxLong)

  sortedUniqueBusinesses = sorted(uniqueBusinesses, key=lambda k: k['rating'] * (log(k['review_count']) + 4) / 7 if k['review_count'] < 20 else k['rating'], reverse=True)

  # print(businesses)
  # print(sortedUniqueBusinesses[0])
  return sortedUniqueBusinesses, minLat, maxLat, minLong, maxLong