import uiautomation as uia

def Close(target: str | uia.Control) -> None:
    """
    # 关闭窗口

    WinWindow.Close(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象(指定被获取子元素的根节点元素)
    :return: None
    """
def GetActive() -> uia.Control:
    """
    # 获取活动窗口

    WinWindow.GetActive()

    :return:control
    """
def SetActive(target: str | uia.Control) -> bool:
    """
    设置活动窗口

    WinWindow.SetActive(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :return: bool。激活成功返回True，否则返回False
    """
def Show(target: str | uia.Control, showStatus: str) -> bool:
    '''
    更改窗口显示状态

    WinWindow.Show(element, "show")

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param showStatus: [必选参数] 显示：\'show\' 隐藏：\'hide\' 最大化：\'max\' 最小化：\'min\' 还原：\'restore\'
    :return: bool。执行成功返回True，否则返回False
    '''
def Exists(target: str | uia.Control) -> bool:
    """
    判断窗口是否存在

    WinWindow.Exists(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :return: bool。窗口存在返回True,否则返回False
    """
def GetSize(target: str | uia.Control) -> dict:
    '''
    获取窗口大小

    WinWindow.GetSize(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :return: {"height":int, "width":int, "x":int, "y":int}
    '''
def SetSize(target: str | uia.Control, width: int, height: int) -> None:
    """
    改变窗口大小

    WinWindow.SetSize(element, 800, 600)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param width: [必选参数]窗口宽度
    :param height: [必选参数]窗口高度
    :return: None
    """
def Move(target: str | uia.Control, x: int, y: int) -> None:
    """
    移动窗口位置

    WinWindow.Move(element, 0, 0)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param x: [必选参数]移动到新位置的横坐标
    :param y: [必选参数]移动到新位置的纵坐标
    :return: None
    """
def TopMost(target: str | uia.Control, topMost: bool) -> None:
    """
    窗口置顶

    WinWindow.TopMost(element, True)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param topMost: [必选参数]是否使窗口置顶，窗口置顶:true 窗口取消置顶:false
    :return: None
    """
def GetClass(target: str | uia.Control) -> str:
    """
    获取窗口类名

    WinWindow.GetClass(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :return: 窗口的类名称
    """
def GetPath(target: str | uia.Control) -> str:
    """
    获取窗口程序的文件路径

    WinWindow.GetPath(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :return: 文件绝对路径
    """
def GetPID(target: str | uia.Control) -> int:
    """
    获取进程PID

    WinWindow.GetPID(element)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :return: PID
    """
