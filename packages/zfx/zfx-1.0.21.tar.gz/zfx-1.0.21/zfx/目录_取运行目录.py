import os


def 目录_取运行目录():
    """
    获取当前运行目录

    Returns:
        str: 当前运行目录的路径，如果获取失败则返回 None。
    """
    try:
        return os.getcwd()  # 尝试获取当前运行目录
    except Exception as e:
        print("无法获取当前运行目录:", e)  # 如果获取失败，打印错误信息
        return None