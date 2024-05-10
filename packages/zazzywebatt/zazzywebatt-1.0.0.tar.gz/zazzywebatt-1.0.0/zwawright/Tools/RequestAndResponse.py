import aiofiles
import re
import base64
import os
from .Vardata import gloData
import json

class Handler:
    def __init__(self, context):
        self.context = context
        self.request_data_list = []
    # 监听并修改请求事件
    async def edit_request(self,route, request):
        # 动态确定 Sec-Fetch-* 头的值
        sec_fetch_site = 'cross-site' if 'otherdomain.com' in request.url else 'same-origin'
        sec_fetch_mode = 'navigate' if request.resource_type == 'document' else 'no-cors'
        sec_fetch_user = '?1' if request.resource_type == 'document' else ''
        sec_fetch_dest = request.resource_type
        # 动态构造 Sec-CH-UA 请求头的值
        sec_ch_ua = '"Not A Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"'
        sec_ch_ua_mobile = '?0'
        sec_ch_ua_platform = '"macOS"'
        
        # 修改请求头
        modified_headers = {
            **request.headers,
            'Sec-Fetch-Site': sec_fetch_site,
            'Sec-Fetch-Mode': sec_fetch_mode,
            'Sec-Fetch-User': sec_fetch_user,
            'Sec-Fetch-Dest': sec_fetch_dest,
            'Sec-CH-UA': sec_ch_ua,
            'Sec-CH-UA-Mobile': sec_ch_ua_mobile,
            'Sec-CH-UA-Platform': sec_ch_ua_platform,
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        all_cookies = await self.context.cookies(request.url)
        request_data = {
            "request_info": {
                "url": request.url,
                "method": request.method,
                "headers": dict(request.headers),
                "cookies": all_cookies
            }
        }
        
        # 将当前请求数据添加到列表中
        self.request_data_list.append(request_data)

        # 继续请求并应用修改后的头
        await route.continue_(headers=modified_headers)

    #根据当前用例的已请求获取base64图片文件
    async def get_base64_img(self, casecode):
        #将request_data_list倒序排列并保存到另一个临时变量
        list = self.request_data_list[::-1]
        image = 0
        for ms in list:
            if ms['casecode'] == casecode:
                url_match = re.match(r"data:image/(\w+);base64,(.*)",ms["request_info"]["url"])
                if url_match:
                    image = image+1
                    img_type = url_match.group(1)
                    img_data = url_match.group(2)
                    img_path = os.path.join(gloData.current_dir, 'log', 'Cachefiles', f'{casecode}1.jpg')
                    async with aiofiles.open(img_path, 'wb') as file:
                        await file.write(base64.b64decode(img_data))
                    if image ==2:
                        break

    # 监听请求事件，将所有信息保存到文件中
    async def handle_request(self, route, casecode):
        request = route.request
        all_cookies = await self.context.cookies(request.url)
        request_data = {
            "casecode": casecode,
            "request_info": {
                "url": request.url,
                "method": request.method,
                "headers": dict(request.headers),
                "cookies": all_cookies
            }
        }
        
        # 将当前请求数据添加到列表中
        self.request_data_list.append(request_data)
        # # 获取或创建请求事件json文件路径
        # request_file_path = gloData.deffile_path.get('request_json_path', 'requests_{}.json'.format(casecode))

        # async with aiofiles.open(request_file_path, 'w') as file:
        #     await file.write(json.dumps(request_data, indent=4))
        await route.continue_()

    # 监听响应事件
    async def handle_response(self,response):
        all_cookies = await self.context.cookies(response.url)
        response_file_path = gloData.deffile_path['response_file_path']
        async with aiofiles.open(response_file_path, 'a') as file:
            await file.write(f"context上下文: {self.context}\n")

        async with aiofiles.open(response_file_path, 'a') as file:
            await file.write(f"    响应 URL: {response.url}\n")
            await file.write(f"    状态码: {response.status}\n")
            await file.write(f"    响应头: {response.headers}\n")
            try:
                response_body = await response.body()
                await file.write(f"    响应体: {response_body.decode('utf-8', errors='ignore')}\n")
            except Exception as e:
                await file.write(f"    获取响应体异常: {e}\n")
            await file.write(f"    响应时的所有 Cookies: {all_cookies}\n\n")