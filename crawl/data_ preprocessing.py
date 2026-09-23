import pandas as pd 
import re
movie_data  = pd.read_csv("crawl/movie_original.csv" , usecols=["movie_name" , "movie_data" , "movie_scores" , "movie_lang" ,"movie_len" , "movie_type"] , nrows= None)
pd.set_option('display.max_rows',100)

"""
评分检查
"""
assert(  (( 0 <movie_data['movie_scores'])&(movie_data['movie_scores']< 100)).all()  ) , "评分异常"

"""
日期检查
"""
for data in movie_data['movie_data'].values :
    
    assert( re.match('^\d{4}-\d{2}-\d{2}$' , data) ) , '日期异常'

"""
语言检查
"""
mask = (movie_data['movie_lang'].isnull())|( movie_data["movie_lang"].str.match(r'\$\d+')) |(movie_data['movie_lang']=='-')
movie_data.loc[mask , "movie_lang"]="unkonwn"



"""
时长检查
"""
mask = movie_data["movie_len"].apply(lambda x : isinstance (x , int))
assert mask.all()


"""
类型检查
"""
idx= movie_data["movie_type"]==" "
movie_data.loc[idx , "movie_type"]="未知"


movie_data.to_csv("crawl/movie_processed.csv")

# print(movie_data)
# print(movie_data[movie_data.isnull ()])

