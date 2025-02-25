from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__)

# 公共请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.bilibili.com'
}

# 校验 BV 号格式
def is_valid_bv(bv):
    bv_pattern = re.compile(r'^BV[a-zA-Z0-9]{10}$')
    return bool(bv_pattern.match(bv))

# 从 URL 中提取 BV 号
def extract_bv_from_url(url):
    bv_pattern = re.compile(r'BV[a-zA-Z0-9]{10}')
    match = bv_pattern.search(url)
    return match.group(0) if match else None

def get_video_details(bv):
    """获取视频详情信息（封面、标题等）"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def get_download_url(avid, cid):
    """获取视频下载链接"""
    url = f"https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&qn=80&type=mp4&platform=html5&high_quality=1"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_video():
    user_input = request.form.get('bv', '').strip()

    # 检查用户输入的格式，如果是 URL，提取其中的 BV 号
    bv = extract_bv_from_url(user_input) if not is_valid_bv(user_input) else user_input

    # 检查 BV 号是否有效
    if not bv or not is_valid_bv(bv):
        return jsonify({"error": "请输入有效的 BV 号"}), 400

    video_details = get_video_details(bv)
    if video_details:
        data = video_details.get('data', {})
        cover_url = data.get('pic', '未找到封面链接')
        video_name = data.get('title', '未找到视频标题')
        avid = data.get('aid')
        cid = data.get('cid')

        if avid and cid:
            download_info = get_download_url(avid, cid)
            if download_info and 'data' in download_info:
                # 提供下载链接（如果有多个清晰度，选择第一个清晰度链接）
                download_url = download_info['data']['durl'][0].get('url', '未找到下载链接')
            else:
                download_url = '获取下载信息失败'
        else:
            download_url = '获取Avid或Cid失败'

        # 提供 B 站预览链接
        preview_url = f"https://www.bilibili.com/video/{bv}"

        return jsonify({
            "video_name": video_name,
            "cover_url": cover_url,
            "download_url": download_url,
            # "preview_url": preview_url  # 直接返回B站预览页面链接
            "preview_url": download_url
        })
    else:
        return jsonify({"error": "获取视频详细信息失败"}), 500

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
