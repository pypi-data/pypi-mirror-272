from .Vardata import gloData
from PIL import Image  
import os
import aiofiles
import numpy as np  
import io
# 传入code、传入图片路径，对比后将数据写入json文件
# async def compare_images(CaseMessage,img1_path,img2_path):
#     data_list=[]
#     file_paths = gloData()

#     path_parts = img1_path.split("_")
#     path_parts[-1] = "diff.png"
#     diff_path = "_".join(path_parts)

#     async with aiofiles.open(img1_path, mode='rb') as img1_file, aiofiles.open(img2_path, mode='rb') as img2_file:
#         img1_data = await img1_file.read()
#         img2_data = await img2_file.read()

#     # 读取图像数据
#     img1_data = np.array(Image.open(io.BytesIO(img1_data)))
#     img2_data = np.array(Image.open(io.BytesIO(img2_data)))

#     # 创建差异图像数组
#     diff_data = np.copy(img2_data)

#     # 计算差异像素数量并更新差异图像数据
#     num_diff_pixels = np.sum(img1_data != img2_data)
#     color = np.array([255, 0, 0])
#     color = np.tile(color, (diff_data.shape[0], diff_data.shape[1], 1))
#     diff_data = np.where((img1_data[..., :3] != img2_data[..., :3]).any(axis=-1, keepdims=True), [255, 0, 0, 255], diff_data)
#     diff_data = diff_data.astype(np.uint8)

#     # 计算差异率 
#     deviation_rate = 1 - num_diff_pixels / (img1_data.shape[0] * img1_data.shape[1])

#     # 将差异图像保存为文件
#     diff_image = Image.fromarray(diff_data)
#     diff_image.save(diff_path)
#     try:
#         assert deviation_rate >= 0.9995
#         pass
#     except AssertionError as e:
#         data = {"断言结果":"失败","用例名": CaseMessage['casetitle'], "用例编号": CaseMessage['casecode'],"相似度":deviation_rate,"期望图片":img2_path,"运行图片":img1_path,"对比图片":diff_path}
#         data_list.append(data)
#         # await re.mylog(data)  # 记录断言失败的错误信息
#     else:
#         data = {"断言结果":"成功","用例名": CaseMessage['casetitle'], "用例编号": CaseMessage['casecode'],"相似度":deviation_rate,"期望图片":img2_path,"运行图片":img1_path,"对比图片":diff_path}
#         data_list.append(data)


async def compare_images(CaseMessage, img1_path, img2_path):
    """
    异步比较两幅图像的差异，通过计算像素差异并生成差异图像及差异报告。
    
    参数:
    - CaseMessage (dict): 包含用例详细信息（如用例名称和用例编号）的字典对象，用于在结果中记录测试详情。
    - img1_path (str): 第一幅待比较图像的文件路径，通常为实际运行环境中的截图或输出图片。
    - img2_path (str): 第二幅待比较图像的文件路径，作为期望的标准图像。

    返回值:
    - data_list (list): 一个包含比较结果的列表，每个元素是一个字典，记录了断言结果、用例名、用例编号、相似度等信息。

    功能：
    此函数的主要目的是在自动化测试场景中，快速准确地判断两幅图像是否几乎完全一致。通过计算两幅图像的像素差异，并生成差异图像以及差异率，
    根据预设阈值判断两张图是否足够相似，最终将断言结果和其他相关信息存储到data_list中。

    使用异步IO库aiofiles读取大文件以提高效率，并使用NumPy处理图像数据进行像素级别的比较。
    """

    data_list = []

    # 获取全局数据，这里假设gloData是获取全局路径等数据的函数，但在这个示例中没有直接使用file_paths
    file_paths = gloData()

    # 构造差异图像保存路径，基于img1_path并在其基础上添加"_diff.png"
    path_parts = img1_path.split("_")
    path_parts[-1] = "diff.png"
    diff_path = "_".join(path_parts)

    # 异步打开并读取两幅图像的二进制数据，提高文件读取性能
    async with aiofiles.open(img1_path, mode='rb') as img1_file, aiofiles.open(img2_path, mode='rb') as img2_file:
        img1_data = await img1_file.read()
        img2_data = await img2_file.read()

    # 将读取到的二进制图像数据转换为NumPy数组以便进一步处理
    img1_data = np.array(Image.open(io.BytesIO(img1_data)))
    img2_data = np.array(Image.open(io.BytesIO(img2_data)))

    # 创建一个新的数组来存储差异图像，初始化为img2_data的副本
    diff_data = np.copy(img2_data)

    # 计算两幅图像之间的不同像素数量，更新diff_data为差异部分红色表示
    num_diff_pixels = np.sum(img1_data != img2_data)
    color = np.array([255, 0, 0])  # 设置差异像素颜色为红色
    color = np.tile(color, (diff_data.shape[0], diff_data.shape[1], 1))  # 扩展颜色至与原图像大小相同
    diff_data = np.where((img1_data[..., :3] != img2_data[..., :3]).any(axis=-1, keepdims=True), [255, 0, 0, 255], diff_data)  # 更新差异像素
    diff_data = diff_data.astype(np.uint8)  # 确保数据类型正确，便于后续保存为图像

    # 计算差异率，即两幅图像相同的像素占比
    deviation_rate = 1 - num_diff_pixels / (img1_data.shape[0] * img1_data.shape[1])

    # 保存差异图像
    diff_image = Image.fromarray(diff_data)
    diff_image.save(diff_path)

    try:
        # 断言差异率是否大于等于预设阈值(此处为99.95%)
        assert deviation_rate >= 0.9995
        pass
    except AssertionError as e:
        # 如果断言失败，则记录失败信息到data_list中
        data = {"断言结果": "失败", "用例名": CaseMessage['casetitle'], "用例编号": CaseMessage['casecode'],
                "相似度": deviation_rate, "期望图片": img2_path, "运行图片": img1_path, "对比图片": diff_path}
        data_list.append(data)
        # await re.mylog(data)  # 在实际应用中会调用日志记录函数，注释已省略
    else:
        # 如果断言成功，则记录成功信息到data_list中
        data = {"断言结果": "成功", "用例名": CaseMessage['casetitle'], "用例编号": CaseMessage['casecode'],
                "相似度": deviation_rate, "期望图片": img2_path, "运行图片": img1_path, "对比图片": diff_path}
        data_list.append(data)