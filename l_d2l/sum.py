import pandas as pd

movie_df = pd.read_csv ('./crawl/movie.csv' , usecols= ['movie_name' , 'movie_data' ,'movie_scores'] ,
                        index_col='movie_name')

# print (movie_df)
# print=(movie_df.info() , '\n ', movie_df.describe())

# print(movie_df.loc['安昂传奇：最后的气宗' :'鬼灭之刃：无限城篇 第一章 猗窝座再袭']==movie_df.iloc[0:5])
# print(movie_df["movie_data"].values[0:5].reshape(5,1))

