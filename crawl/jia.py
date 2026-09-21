import lxml
from lxml import html
import csv
import requests
import re


TMDB_URL='https://www.themoviedb.org/'
TMDB_MOVIE_URL='https://www.themoviedb.org/movie/top-rated'


response=requests.post('https://www.themoviedb.org/discover/movie/items',
                data=f"air_date.gte=&air_date.lte=&certification=&certification_country=CN&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page=3&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=2027-03-13&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&watch_region=CN&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400")
movie_doc= html.fromstring(response.text)

movie_list=movie_doc.xpath('//*[@class="media-list-results contents"]/div')

for movie in movie_list :
    movie_link=movie.xpath('.//a/@href')
    movie_url=TMDB_URL+movie_link[0]
    print(f"正在从{movie_url}获取电影信息")
    movie_response=requests.get(movie_url)
    movie_docs=html.fromstring(movie_response.text)
    movie_name  =movie_docs.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
    movie_len   =movie_docs.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[@class="runtime"]/text()')
    print(f"正在导入{movie_name[0].strip()}的信息")
    print(movie_len[0])


