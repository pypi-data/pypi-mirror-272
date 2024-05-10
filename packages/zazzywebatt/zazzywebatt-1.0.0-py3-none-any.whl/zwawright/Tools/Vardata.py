import os


class gloData:
    def __init__(self) -> None:
        pass
    # 获取UITest的目录路径
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # print("这是当前的路径：", current_dir)

    # JSON 文件名
    TestCases = "TestCases.json"
    debugger = "debugger"
    request = "log/requests.log"
    response = "log/responses.log"
    
    filepaths = {
        "json_file_path" : os.path.join(current_dir, TestCases),
        "debugger_folder_path" : os.path.join(current_dir, debugger),
        "request_file_path" : os.path.join(current_dir, request),
        "response_file_path" : os.path.join(current_dir, response),
    }