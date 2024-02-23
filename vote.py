import requests
from bs4 import BeautifulSoup

def contain_vote(text):
    s=''
    for char in text:
        if char.isalpha():
            s+=char.lower() #小写
        else:
            s+=char
    return 'vote' in s
    

def get_url(url): #获取一页讨论帖, url:网址
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    poster=[x.text for x in soup.select('cite>span')] #发帖人
    post_time=[x.text.strip() for x in soup.select('.postinfo>em:nth-child(2)')] #发帖时间
    content=[x.text.strip() for x in soup.select('.t_msgfont')] #帖子内容文本

    s=''
    for i in range(len(poster)):
        if contain_vote(content[i]):
            s+=f"{poster[i]}({post_time[i]})> {content[i]}\n\n"
    return s

def get_topic(topic,start,end):
    #获取多页讨论帖, topic:讨论帖编号, start:开始页数, end:结束页数    
    output=''
    for i in range(start,end+1):
        url=f'https://keyfc.com/bbs/showtopic-{topic}-{i}.aspx'
        output+=get_url(url)
        print(url+'获取完成')

    #将文本写入txt文件
    file=open(f'vote-{topic}({start}-{end}).txt','w',encoding='utf-8')
    file.write(output)
    file.close()

if __name__=='__main__':
    '''
    示例：获取有投票的讨论帖
    从https://keyfc.com/bbs/showtopic-69988-28.aspx
    到https://keyfc.com/bbs/showtopic-69988-42.aspx
    '''
    get_topic(69988,53,60)
