
# Scott's Python Facebook Mining Tool

Dependencies
 * [facepy](https://pypi.python.org/pypi/facepy/0.9.0)
 * [facebook-sdk](http://www.pythonforfacebook.com/)

[Original Documentation](https://docs.google.com/document/d/1g3hY_91WdvssofOhSei
0S3xgdgxXIDCdVQnA_Efq9Is/edit?usp=sharing)

# Getting data from a facebook page


## 1. Make an instance of fbMiner


    import scraper
    import jsonS


    reload(scraper)




    <module 'scraper' from 'scraper.py'>




    fbm = scraper.fbMiner()

## 2. Get the id of the page that you want to get data from and set it in
fbMiner

    you may need to try two ways to do this.  I’m not sure why sometimes one
works and not the other, probably depends on exactly what kind of page it is
(i.e: page, group, profile, event, etc).

    Try this first. Log on to facebook and load the page you want to get posts
from.  If there is a number at the end of the url, this is the page id number.

    If there is no number, then change the url from
“www.facebook.com/page_name_etc” to “graph.facebook.com/page_name_etc” and press
enter.  This will show you a json readout of the page’s information, the id
value is the page id that you want. Here is an example
```
{
   "id": "161018933975937",
   "about": "The official Facebook page for SIGKDD and the KDD 2014 conference.
http://www.kdd.org/kdd2014/",
   "can_post": false,
   "category": "Organization",
   "checkins": 0,
   "cover": {
      "cover_id": 622697014474791,
      "offset_x": 0,
      "offset_y": 0,
      "source": "https://fbcdn-sphotos-b-a.akamaihd.net/hphotos-ak-
xpa1/t31.0-8/s720x720/10431236_622697014474791_6883537713839232534_o.jpg",
      "id": "622697014474791"
   },
   "description": "Get the latest news and updates from ACM's Special Interest
Group on Knowledge Discovery and Data Mining (SIGKDD) and the KDD 2014
conference (http://www.kdd.org/kdd2014/).",
   "has_added_app": false,
   "is_community_page": false,
   "is_published": true,
   "likes": 1726,
   "link": "https://www.facebook.com/SIGKDD",
   "name": "SIGKDD",
   "parking": {
      "lot": 0,
      "street": 0,
      "valet": 0
   },
   "talking_about_count": 23,
   "username": "SIGKDD",
   "website": "http://www.sigkdd.org",
   "were_here_count": 0
}
```



    fbm.setPageId("161018933975937") #SIGKDD Facebook Group

## 3. Set Application Credentials
    To get application credentials you will need the following
        1. A Facebook developer account
        2. An Application account
    Getting a Facebook developer account is pretty easy.  I have heard of people
having difficulty getting an Application account for the purposes of mining
pages though, so be sure to clearly state your intentions when applying for an
application account.

    Once you are done, you can get the App ID and the App secret.  If you are
bold, you can set the fbMiner's application credentials like this...

    fbMiner.app_id = 123456789101112
    fbMiner.app_secret = 123456789101112131415abcdefghijkl


    There is also a function to just read in the credentials from a json file
that would look like this...

    { APP_ID : "123456789101112", APP_SECRET :
"123456789101112131415abcdefghijkl"}




    credsIn = open('app_credentials.json', 'r').read()
    fbm.setAppCredentialsFromJSON(credsIn)

## 4. Get User Credentials

    This part took me a long while to figure out, but this [blog post was very
helpful](http://fearofcoding.blogspot.com/2012/10/python-script-to-fetch-
messages-from.html).

    Here's what you need to do...

    1. Log in to the [Facebook Graph API Explorer
page](https://developers.facebook.com/tools/explorer/)
    2. Set the application from "Graph API Explorer" to the name of your project
using the drop down menu at the top.  If you do not see your app, then make sure
that you logged into a facebook account that is set as a developer for the
application.  You may need to have the person who started the application add
you.
    3. click "Get Access Token" and copy the access token on the right.
    4. This is just the "short token" and will not take long to expire.  If you
are data mining a small page and this is not a concern, you can set the fbMiner
tool's short token as displayed below, otherwise skip to the next step.
        fbm.setShortToken(short_token_string)
    5. If your data mining process will need to run for a while, you will need
to set a long access token.  fbMiner.setLongToken() is a helper method that will
do this for you by passing in the short token.  I suggest that you leave your
long token in a file and read it in by passing the file name to
fbMiner.setLongTokenFromFile(file_name)


    # set Short Token
    short_token = "123456789etc"
    fbm.setShortToken(short_token)
    
    #set Long Token from string
    #fbm.setLongToken(short_token)
    long_token_fileName = "long_token.txt"
    fbm.setLongTokenFromFile(long_token_fileName)

## 5. Start Mining

    At this point you should be able to start collecting data.  If you want to
just grab all the post objects from the timeline use fbMiner.get_data() as
demonstrated below


    posts = fbm.get_data(limit=100)

    page : 1
    c : 0
    lockout time : 0 seconds
    page : 2



    posts[0]




    {u'actions': [{u'link': u'https://www.facebook.com/161018933975937/posts/708284722582686',
       u'name': u'Comment'},
      {u'link': u'https://www.facebook.com/161018933975937/posts/708284722582686',
       u'name': u'Like'}],
     u'application': {u'id': u'103667826405103',
      u'name': u'Buffer',
      u'namespace': u'buffer-app'},
     u'caption': u'www.kdd.org',
     u'created_time': u'2014-11-25T20:24:33+0000',
     u'description': u'20th ACM SIGKDD Conference on Knowledge Discovery and Data Mining: homepage',
     u'from': {u'category': u'Organization',
      u'id': u'161018933975937',
      u'name': u'SIGKDD'},
     u'icon': u'https://fbstatic-a.akamaihd.net/rsrc.php/v2/yD/r/aS8ecmYRys0.gif',
     u'id': u'161018933975937_708284722582686',
     u'likes': {u'data': [{u'id': u'100000017043967', u'name': u'Petro Rudenko'},
       {u'id': u'100000073351348', u'name': u'Shaw Wu'},
       {u'id': u'100002089938324', u'name': u'Rosana Veroneze'},
       {u'id': u'100000276915749', u'name': u'Christos Berberidis'},
       {u'id': u'100000452123860', u'name': u'Tsubasa Takahashi'},
       {u'id': u'550103931', u'name': u'Ibrahim Musa'},
       {u'id': u'714815433', u'name': u'Shishir Pandey'},
       {u'id': u'1619431644', u'name': u'V\u0129 Ng\xf4 V\u0103n'},
       {u'id': u'737483873', u'name': u'Danny Huanca Sevilla'},
       {u'id': u'100000051986201', u'name': u'Ayushi Dalmia'},
       {u'id': u'100003018647877', u'name': u'Masayuki  Ishikawa'},
       {u'id': u'729004290', u'name': u'Arturo Oncevay'},
       {u'id': u'647297753', u'name': u'Shoumik Roychoudhury'},
       {u'id': u'100006101438416', u'name': u'Dew Wardah'},
       {u'id': u'1032972796', u'name': u'Sofus Attila Macsk\xe1ssy'},
       {u'id': u'564453662', u'name': u'Tina Eliassi-Rad'}],
      u'paging': {u'cursors': {u'after': u'NTY0NDUzNjYy',
        u'before': u'MTAwMDAwMDE3MDQzOTY3'}}},
     u'link': u'http://www.kdd.org/kdd2014/?utm_content=buffer31556&utm_medium=social&utm_source=facebook.com&utm_campaign=buffer',
     u'message': u'Watch #kdd2014 talks and videos! SIGKDD + KDD 2014 #kdd2015',
     u'name': u'KDD 2014, 8/24-27, New York: Data Mining for Social Good',
     u'picture': u'https://fbexternal-a.akamaihd.net/safe_image.php?d=AQDui4zVf3788TaO&w=158&h=158&url=http%3A%2F%2Fwww.kdd.org%2Fkdd2014%2Fimg%2Fvideo-lectures.gif',
     u'privacy': {u'value': u''},
     u'status_type': u'shared_story',
     u'type': u'link',
     u'updated_time': u'2014-11-25T20:24:33+0000'}



    If you want to use the graph API object in a more flexible manner, you can
get it directly from fbMiner using fbMiner.getGraphAPI()


    graphAPI = fbm.getGraphAPI()

    It is important to note that fbMiner.get_data() handles pagination
automatically and uses a crude attempt at exponential backoff.  Later, I will
add more documentation on how to use the fbMiner graph API and make the
exponential backoff more clean
