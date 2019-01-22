#coding-utf-8
import requests
import re
import json
from flask import Flask,request,render_template
w1='<!--火车头地址开始'
w2='火车头地址结束-->'
def get_m3u8(id):
    _url=''
    _url='http://yongjiuzy.cc'+id
    _html=requests.get(_url)
    html_data=_html.text
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(html_data)
    #print(result[0])
    
    m3u8_url=re.findall('<li>(.*?)\$(.*?)</li>',result[0],re.S)
    return(m3u8_url)
def local_search(name):
    wd=''
    wd=name
    #name=input("请输入想要搜索的影片：")    #获取电影名称
    data_post={"wd":wd}  #定义post数据 用于搜索影片
    url_post='http://yongjiuzy.cc/index.php?m=vod-search' #定义post提交url，用于搜索影片
    html=requests.post(url_post,data=data_post)   #提交post数据
    text_html=html.text   #将返回数据转换为text文本形式
    #print(text_html)

    movie_url=re.findall('<td class="l"><a href="(.*?)" target="_blank">',text_html,re.S)
    for text in movie_url:
        data_result=get_m3u8(text)
        list2=[str(i) for i in data_result]
        list3=' '.join(list2)
        #return data_result
        #print(data_result)
        #json_txt=json.dumps(data_result)
        return list3
        #print(json_txt)
        #print(text)
app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/search/',methods=['get'])
def search():
    #return request.args.get('wd')
    #print(wd)
    f_get=request.args.get('wd')
    if f_get == None:
        return 'None'
    elif f_get=='':
        return 'None'
    else:
        return local_search(f_get)
if __name__ == '__main__':
    app.run(debug=False,port=80)




    
