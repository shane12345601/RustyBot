from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

page_url = 'https://www.chegg.com/homework-help/questions-and-answers/python-programming-q25481936'

req = Request(page_url, headers={'User-Agent': 'XYZ/3.0'})
webpage = urlopen(req, timeout=10).read()

page_soup = soup(urlopen(req, timeout=10).read(), "lxml")

print(page_soup)

containers = page_soup.findAll("div", {"class": "answer-given-body ugc-base"})

print(containers)