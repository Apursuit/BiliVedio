import requests 

# 设置自定义header，包括Referer 和 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.bilibili.com'
}

def get_video_details(bv):
    # 根据BV获取视频详细信息
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
        return response.json()  # 返回JSON格式的响应内容
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("响应不是有效的JSON格式")
        return None

def get_download_url(avid, cid):
    # 根据Avid和Cid获取下载地址
    url = f"https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&qn=80&type=mp4&platform=html5&high_quality=1"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.json()  # 返回JSON格式的响应内容
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("响应不是有效的JSON格式")
        return None

# 示例使用
bv = 'BV15frBYGEez'  # 替换为实际的BV号

# 获取视频详细信息
video_details = get_video_details(bv)

if video_details:
    # 提取视频封面链接
    cover_url = video_details.get('data', {}).get('pic')
    if cover_url:
        print("视频封面链接:", cover_url)
    else:
        print("未找到视频封面链接")

    # 提取Avid和Cid
    avid = video_details.get('data', {}).get('aid')
    cid = video_details.get('data', {}).get('cid')

    if avid and cid:
        # 获取下载链接
        download_info = get_download_url(avid, cid)
        if download_info:
            download_url = download_info.get('data', {}).get('durl', [{}])[0].get('url')
            if download_url:
                print("下载接口:", download_url)
            else:
                print("未找到下载链接")
        else:
            print("获取下载信息失败")
    else:
        print("获取Avid或Cid失败")
else:
    print("获取视频详细信息失败")
