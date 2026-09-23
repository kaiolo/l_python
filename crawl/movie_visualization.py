import pandas as pd
import matplotlib.pyplot as plt

fig , axes = plt.subplots(nrows = 2 , ncols= 2 ,figsize=(12, 8 ) )
fig1 , fig2 , fig3 , fig4 = axes.flat

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.suptitle("TMTD-TOP300" , fontsize = 30)
plt.subplots_adjust(hspace = 0.6)
movie_data = pd.read_csv ("crawl/movie_processed.csv")
movie_data['movie_year'] = movie_data['movie_data'].apply (lambda year : int(year[:4]))
n_year=movie_data.groupby("movie_year")["movie_year"].count()
max_year = movie_data['movie_year'].max()
min_year = movie_data['movie_year'].min()
year = [year for year in range(min_year , max_year+1)]
y_year=[n_year.get(num , 0) for num in year]
"""
fig1:不同年份电影数量折线图
"""
fig1.plot(year , y_year, color = "purple" )
fig1.set_xticks(year[::10])
fig1.grid(alpha = 0.3 , linestyle = ":")
fig1.set_xlabel("年份")
fig1.set_ylabel("数量")
fig1.set_title("年份-数量折线图")
fig1.xaxis.set_label_coords(1.01, -0.04)


n_lang = movie_data.groupby("movie_lang")["movie_lang"].count().sort_values(ascending=False).values.tolist()
lang = movie_data.groupby("movie_lang")["movie_lang"].count().sort_values(ascending=False).index.tolist()



"""
电影语言数量柱状图
"""
fig2.bar(lang , n_lang , color = "pink")
fig2.tick_params(rotation = -90)
fig2.set_title("语言-数量柱状图")
fig2.set_xlabel("语言")
fig2.set_ylabel("数量")
fig2.xaxis.set_label_coords(1.01, -0.04)

movie_type = movie_data['movie_type']
dic_type = {}
for types in movie_type.values :
    for type in types.split(",") :
        if type in dic_type :
           dic_type[type]+=1 
        else : dic_type[type]=1

      
x_type = list(dic_type.keys())
n_type = list(dic_type.values())


"""
电影类型数量柱状图
"""

fig3.bar(x_type , n_type , color = "plum")
fig3.tick_params(rotation = -90)
fig3.set_title("类型-数量柱状图")
fig3.set_xlabel("类型")
fig3.set_ylabel("数量")
fig3.xaxis.set_label_coords(1.01, -0.04)


movie_scores = movie_data.groupby("movie_scores")['movie_scores'].count()
large_scores = movie_scores[movie_scores>10]
small_scores = movie_scores[movie_scores<=10]
if small_scores.tolist() != [] :
    large_scores.loc["其他"] = small_scores.sum()
n_scores = large_scores.values.tolist()
scores = large_scores.index.tolist()
"""
电影评分饼状图
"""
fig4.pie(n_scores  )
fig4.legend(ncols=4 , loc = "lower center" ,bbox_to_anchor = (0.5 , -0.25) , labels =scores)
fig4.set_title("电影评分饼状图")
plt.show()
