import uiautomation as uia

def Action(target: str | uia.Control, button: str, clickType: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, keyModifiers: list = None, simulateType: str = 'simulate', moveSmoothly: bool = False) -> uia.Control:
    '''
    点击目标元素

    WinMouse.Action(element, \'left\', \'click\', 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, keyModifiers=None, simulateType=\'simulate\', moveSmoothly=False)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param button: [必选参数]鼠标点击。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"
    :param clickType: [必选参数]点击类型。单击:"click" 双击:"dbclick" 按下:"down" 弹起:"up"
    :param searchDelay: [必选参数]超时时间(毫秒)。
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :param setForeground: [可选参数]激活窗口。默认True
    :param cursorPosition: [可选参数]光标位置。中心(默认):"center"  左上角:"topLeft"  右上角:"topRight"  左下角:"bottomLeft"  右下角:"bottomRight"
    :param cursorOffsetX: [可选参数]横坐标偏移。默认0
    :param cursorOffsetY: [可选参数]纵坐标偏移。默认0
    :param keyModifiers: [可选参数]辅助按键 "Alt","Ctrl","Shift","Win",可多选，默认None
    :param simulateType: [可选参数]操作类型。模拟操作(默认):"simulate"   消息操作:"message"
    :param moveSmoothly: [可选参数]平滑移动。默认False
    :return:目标元素对象
    '''
def Hover(target: str | uia.Control, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, keyModifiers: list = None, simulateType: str = 'simulate', moveSmoothly: bool = True) -> uia.Control:
    '''
    移动到目标上

    WinMouse.Hover(element, 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, keyModifiers=None, simulateType=\'simulate\', moveSmoothly=False)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :param setForeground: [可选参数]激活窗口。默认True
    :param cursorPosition: [可选参数]光标位置。中心(默认):"center"  左上角:"topLeft"  右上角:"topRight"  左下角:"bottomLeft"  右下角:"bottomRight"
    :param cursorOffsetX: [可选参数]横坐标偏移。默认0
    :param cursorOffsetY: [可选参数]纵坐标偏移。默认None
    :param keyModifiers: [可选参数]辅助按键 "Alt","Ctrl","Shift","Win",可多选，默认None
    :param simulateType: [可选参数]操作类型。模拟操作(默认):"simulate"   消息操作:"message"
    :param moveSmoothly: [可选参数]平滑移动。默认False
    :return:目标元素对象
    '''
def Click(button: str, clickType: str, keyModifiers: list, delayAfter: int = 100, delayBefore: int = 100) -> None:
    '''
    模拟点击

    WinMouse.Click("left", "click", [], delayAfter=100, delayBefore=100)

    :param button: [必选参数]鼠标点击。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"
    :param clickType: [必选参数]点击类型。单击:"click" 双击:"dbclick" 按下:"down" 弹起:"up"
    :param keyModifiers: [必选参数]辅助按键 "Alt","Ctrl","Shift","Win",可多选，默认空
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    '''
def Move(x: int, y: int, isRelativeMove: bool, delayAfter: int = 100, delayBefore: int = 100) -> None:
    """
    # 模拟移动

    WinMouse.Move(0, 0, False, delayAfter=100, delayBefore=100)

    :param x: [必选参数]横坐标
    :param y: [必选参数]纵坐标
    :param isRelativeMove: [必选参数]是否相对移动
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    """
def GetPos() -> tuple[int, int]:
    """
    获取鼠标位置

    WinMouse.GetPos()

    :return:pointX, pointY
    """
def Drag(x1: int, y1: int, x2: int, y2: int, button: str, keyModifiers: list = None, delayAfter: int = 100, delayBefore: int = 100) -> None:
    '''
    模拟拖动

    WinMouse.Drag(0, 0, 0, 0, \'left\', None, delayAfter=100, delayBefore=100)

    :param x1: [必选参数]起始横坐标
    :param y1: [必选参数]起始纵坐标
    :param x2: [必选参数]结束横坐标
    :param y2: [必选参数]结束纵坐标
    :param button: [必选参数]鼠标点击。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"
    :param keyModifiers: [必选参数]辅助按键 "Alt","Ctrl","Shift","Win",可多选，默认None
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    '''
def Wheel(scrollNum: int, scrollDirection: str, keyModifiers: list = None, delayAfter: int = 100, delayBefore: int = 100) -> None:
    '''
    模拟滚轮

    WinMouse.Wheel(0, "down", None, delayAfter=100, delayBefore=100)

    :param scrollNum: [必选参数]滚动次数
    :param scrollDirection: [必选参数]滚动方向
    :param keyModifiers: [必选参数]辅助按键 "Alt","Ctrl","Shift","Win",可多选，默认None
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    '''
