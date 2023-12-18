
import requests
from bs4 import BeautifulSoup
import time

def search_weibo(keyword, max_pages=5):
    results = []

    for page in range(1, max_pages + 1):
        # 微博搜索URL，加入翻页参数
        url = f'https://s.weibo.com/weibo?q={keyword}&page={page}'

        # 发送GET请求
        response = requests.get(url)

        # 检查响应状态
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}")
            continue

        # 解析响应内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 根据页面结构提取微博内容
        weibos = soup.find_all('div', {'class': 'card'})  # 假设每条微博在'div'标签的'class'为'card'中
        for wb in weibos:
            # 提取微博文本
            content = wb.find('p', {'class': 'txt'}).get_text(strip=True)

            # 提取发布时间和发布者
            footer = wb.find('div', {'class': 'footer'})
            time = footer.find('span', {'class': 'time'}).get_text(strip=True)
            author = footer.find('a', {'class': 'name'}).get_text(strip=True)

            # 提取转赞评数量
            stats = wb.find('div', {'class': 'stats'})
            reposts = stats.find('span', {'class': 'reposts'}).get_text(strip=True)
            comments = stats.find('span', {'class': 'comments'}).get_text(strip=True)
            likes = stats.find('span', {'class': 'likes'}).get_text(strip=True)

            results.append({
                'content': content,
                'time': time,
                'author': author,
                'reposts': reposts,
                'comments': comments,
                'likes': likes
            })
            pass  # 解析代码

        #等待
        time.sleep(1)  # 等待1秒

    return results

# 使用示例
keyword = '芭比 电影'
weibo_data = search_weibo(keyword, max_pages=3)
for data in weibo_data:
    print(data)
