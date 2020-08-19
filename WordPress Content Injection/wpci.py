import json
import sys
import urllib2

from lxml import etree


def get_api_url(wordpress_url):
    response = urllib2.urlopen(wordpress_url)

    data = etree.HTML(response.read())
    u = data.xpath('//link[@rel="https://api.w.com/"]/@href')[0]

    if 'rest_route' in u:
        print(' ! Warning, looks like permalinks are not enabled. This might not work!')

    return u


def get_posts(api_base):
    respone = urllib2.urlopen(api_base + 'wp/v2/posts')
    posts = json.loads(respone.read())

    for post in posts:
        print(' - Post ID: {}, Title: {}, Url: {}'
              .format(post['id'], post['title']['rendered'], post['link']))


def update_post(api_base, post_id, post_content):

    data = json.dumps({
        'content': post_content
    })

    url = api_base + 'wp/v2/posts/{post_id}/?id={post_id}abc'.format(post_id=post_id)
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(req).read()

    print('* Post updated. Check it out at {}'.format(json.loads(response)['link']))


def print_usage():
    print('Usage: {} <url> (optional: <post_id> <file with post_content>)'.format(__file__))


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    if 2 < len(sys.argv) < 4:
        print('Please provide a file with post content with a post id')
        print_usage()
        sys.exit(1)

    print('* Discovering API Endpoint')
    api_url = get_api_url(sys.argv[1])
    print('* API is at: {}'.format(api_url))

    if len(sys.argv) < 3:
        print('* Getting available posts')
        get_posts(api_url)

        sys.exit(0)

    print('* Updating post {}'.format(sys.argv[2]))
    with open(sys.argv[3], 'r') as content:
        new_content = content.readlines()

    update_post(api_url, sys.argv[2], ''.join(new_content))

    print('* Update complete!')
