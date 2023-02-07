import json
import urllib.request

DEFAULT_ENCODING = 'utf-8'

url = 'http://127.0.0.1:8000/stories_service.html'
urlResponse = urllib.request.urlopen(url)
if hasattr(urlResponse.headers, 'get_content_charset'):
    encoding = urlResponse.headers.get_content_charset(DEFAULT_ENCODING)
else:
    encoding = urlResponse.headers.getparam('charset') or DEFAULT_ENCODING

stories = json.loads(urlResponse.read().decode(encoding))
print(stories[:2])

# for i in stories
# print(i['author'])