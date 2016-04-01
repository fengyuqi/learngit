import os
import urllib
import re
from gevent import monkey;monkey.patch_all()
import gevent

# img_url in the html web page
def parse_img_url(html):
  rex=re.compile(r'"(http://[0-9]+.media.tumblr.com/[0-9a-z]+/tumblr_[0-9a-zA-Z\_]+.jpg)"')
  m=re.findall(rex,html)
  return m

# other img_url in the photoset of the html web page
def parse_photoset(html):
  rex = re.compile(r'src="(http://[0-9a-z]+.tumblr.com/post/[0-9]+/photoset_iframe/[0-9a-z]+/tumblr_[0-9a-zA-Z_]+/[0-9]+/[a-z]+)"') 
  m = re.findall(rex, html)
  return m

# video_src is url whose html contains mp4_url
def parse_video_src(html):
  rex = re.compile(r"<iframe src='(https://www.tumblr.com/video/.+/\d+/\d+/)'") 
  m = re.findall(rex, html)
  return m

# mp4_url in the video_src of the html web page
def parse_mp4_url(html):
  rex = re.compile(r'<source src="https://www.tumblr.com/video_file/\d+/(.+)" type="video/mp4">')
  m=re.findall(rex,html)
  r= ['https://vt.tumblr.com/' + '_'.join(i.split('/')) + '.mp4' for i in m]
  return r

def wget(url, name):
  urllib.urlretrieve(url, './' + name)
  print('retrieve completed from %s' % url)

def filename(img_url):
  # import hashlib
  # return hashlib.md5(img_url).hexdigest()+'.mp4'
  return img_url.split('/')[-1]


HTML = ''
def complete_html(url):
  html = urllib.urlopen(url).read()
  global HTML
  HTML += html
  print(len(HTML))

if __name__=='__main__':
  global HTML
  HTML += urllib.urlopen('http://.tumblr.com/page/1').read()
  with open("./html.txt", 'wb') as f:
    f.write(HTML)

  src = []
  video_src = parse_video_src(HTML)
  src.extend(video_src)
  img_src = parse_photoset(HTML)
  src.extend(img_src)
  print src
  gevent.joinall([gevent.spawn(complete_html , i) for i in src])

  mp4_urls = parse_mp4_url(HTML)
  img_urls = parse_img_url(HTML)
  mp4_urls.extend(img_urls)
  print mp4_urls
  with open("./log.txt",'wb') as f:
    for i in mp4_urls:
      f.write(i+'\n') 

  gevent.joinall([gevent.spawn(wget , i, filename(i)) for i in mp4_urls])
