import random
import json

import webapp2
import logging
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import passwords
import models

def search(args):
    """ Search flickr api for images. args is dict in the format of {"tags": "chicken,pig","text":"chicken pig","license":"1,2,3,4,5","sort":"relevance","page":1}
    licenses refer to flickr license numbers availible at <https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html> """

    url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+passwords.FLICKR_API_KEY+"&tags="+args["tags"]+"&text="+args["text"]+"&license="+args["license"]+"&safe_search=1&format=json&nojsoncallback=1&sort="+args["sort"]+"&page="+str(args["page"])

    result = urlfetch.fetch(
        url=url,
        method=urlfetch.GET,
        headers={'Referer': 'https://chickenaday.appspot.com'}
    )
    logging.info(result.content)

    return json.loads(result.content)

def buildFlickrPhotoURL(photo):
    url = "https://farm"+str(photo["farm"])+".staticflickr.com/"+photo["server"]+"/"+photo["id"]+"_"+photo["secret"]+"_d.jpg"

    return url

def randomChickenPhoto():
    """Get a random chicken photo url and it's corresponding photographer name, and flickr user page link
    All images creative commons most restrictive or above. Check the search function for details on possible licenses and then modify the numbers to fit the licenses you need.
    Because the images are sorted by relevance, after adjusting anything you may have to modify the maxPageNum below"""
    maxPageNum = 35 # after 35 the results start to get less relevant

    pageNum = random.randint(0, maxPageNum)
    itemNum = random.randint(0, 99) # 100 items a page so 0-99 with python's index starting at 0

    page = search({"tags": "chicken", "text": "chicken", "license": "1,2,3,4,5,6,7,8,9,10", "sort": "relevance", "page": pageNum})

    photos = page["photos"]["photo"]

    photo = photos[itemNum]
    person = getFlickrUser(photo["owner"])

    return {"url": buildFlickrPhotoURL(photo), "name": person["name"], "profile": person["profile"]}

def getFlickrUser(id):
    """get a username and profile id for a flickr user id"""
    url = "https://api.flickr.com/services/rest/?method=flickr.people.getInfo&api_key="+passwords.FLICKR_API_KEY+"&user_id="+id+"&format=json&nojsoncallback=1"

    result = urlfetch.fetch(
        url=url,
        method=urlfetch.GET,
        headers={'Referer': 'https://chickenaday.appspot.com'}
    )

    response = json.loads(result.content)

    profile = response["person"]["profileurl"]["_content"]
    try:
        name = response["person"]["realname"]["_content"]
    except KeyError:
        name = profile

    return {"name": name, "profile": profile}

class RandomImageHandler(webapp2.RequestHandler):
    def get(self):
        photo = randomChickenPhoto()
        self.response.out.write(json.dumps(photo))
class StoreImageHandler(webapp2.RequestHandler):
    def get(self):
        photo = randomChickenPhoto()

        query = models.General.query(models.General.key == "dailyImage")
        results = query.fetch()

        if len(results) == 0: # then this property doesn't exists,  this is probably the first run. Let's create it
            savedPhoto = models.General(key = "dailyImage")
        else:
            savedPhoto = results[0] # there should be only one

        if photo["name"] == "":
            photo["name"] = photo["profile"]

        savedPhoto.url = photo["url"]
        savedPhoto.name = photo["name"]
        savedPhoto.profile = photo["profile"]

        savedPhoto.put() # save the changes that we made
class TodayImageMetadataHandler(webapp2.RequestHandler):
    def get(self):
        query = models.General.query(models.General.key == "dailyImage")
        results = query.fetch()

        photo = results[0]

        self.response.out.write(json.dumps({"url": photo.url, "name": photo.name, "profile": photo.profile, "license": "This photo is licenses under <= the most restrictive creative commons license. Give attribution, no derivatives, and non commercial use only unless you go to the photo on "
                                "flickr and find that it has a less restrictive license"}))
class TodayImageHandler(webapp2.RequestHandler):
    def get(self):
        query = models.General.query(models.General.key == "dailyImage")
        results = query.fetch()

        photo = results[0]

        self.redirect(photo.url, permanent = False)

app = webapp2.WSGIApplication([
    ("/image/random", RandomImageHandler),
    ("/image/store", StoreImageHandler),
    ("/image/today", TodayImageMetadataHandler),
    ("/image/today.jpg", TodayImageHandler)
], debug=True)


