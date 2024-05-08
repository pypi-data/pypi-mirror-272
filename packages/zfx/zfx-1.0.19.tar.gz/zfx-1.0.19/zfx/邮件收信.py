import poplib


import poplib

def 登录邮箱(邮件服务器, 端口号, 邮箱地址, 邮箱密码):
    """
    连接到邮件服务器并登录邮箱。

    Args:
        邮件服务器 (str): 邮件服务器的地址。
        端口号 (int): 邮件服务器的端口号。
        邮箱地址 (str): 要登录的邮箱地址。
        邮箱密码 (str): 要登录的邮箱密码。

    Returns:
        poplib.POP3 or None: 如果登录成功，返回一个 POP3 对象；如果登录失败，返回 None。

    Raises:
        无异常抛出。

    Examples:
        >>> server = 登录邮箱('mail.example.com', 110, 'user@example.com', 'password')
        登陆成功
        >>> if server:
        ...     print("登录成功")
        ... else:
        ...     print("登录失败")
        ...
        登录成功
    """
    # 连接到邮件服务器
    服务器 = poplib.POP3(邮件服务器, 端口号)

    # 登录邮箱
    if 服务器.user(邮箱地址).startswith(b'+OK') and 服务器.pass_(邮箱密码).startswith(b'+OK'):
        print("登陆成功")
        return 服务器
    else:
        print("登陆失败")
        return None



def 获取邮件数量(服务器):
    """
    获取邮箱中的邮件数量。

    Args:
        服务器 (poplib.POP3): 已连接的 POP3 服务器对象。

    Returns:
        int: 邮箱中的邮件数量。

    Raises:
        poplib.error_proto: 如果与服务器通信出现错误。

    Examples:
        >>> server = 登录邮箱('mail.example.com', 110, 'user@example.com', 'password')
        >>> 邮件数量 = 获取邮件数量(server)
        >>> print(邮件数量)
        10
    """
    # 获取邮箱中的邮件数量和占用空间大小
    邮件数量, _ = 服务器.stat()
    return 邮件数量



# 使用示例
服务器 = 登录邮箱('mail.zczfx.com', 110, 'abc@zczfx.asia', 'Aa1199882233')
if 服务器:
    获取邮件数量(服务器)
