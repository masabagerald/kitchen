import  json
import urllib,urllib2

BING_API_KEY =00000

def run_query(search_terms):

    root_url ='https://api.datamarket.azure.com/Bing/Search/'
    source = 'web'

    result_per_page = 10
    offset =0;

    query = "'{0}' ".format(search_terms)
    query = urllib.quote(query)

    search_url ="{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,
        source,
        result_per_page,
        offset,
        query )
    username = ''

    password_mng = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mng.add_password(None,search_url,username,BING_API_KEY)

    results = []

    try:
        handler = urllib2.HTTPBasicAuthHandler(password_mng)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        response = urllib2.urlopen(search_url).read()

        json_response = json.loads(response)

        for result in json_response['d']['results']:
            result.append({
                'title':result['Title'],
                'origin':result['origin'],
                'summary':result['Description']})
    except urllib2.URLError as e:
        print "Error when querying the Bing API: ", e

        return  results