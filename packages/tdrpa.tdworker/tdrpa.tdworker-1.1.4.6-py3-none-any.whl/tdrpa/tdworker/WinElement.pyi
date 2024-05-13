import uiautomation as uia

def findElement(selectorString: str = None, anchorsElement: uia.Control = None, searchDelay: int = 10000, continueOnError: bool = False) -> uia.Control | None:
    """
    获取元素

    WinElement.findElement('', anchorsElement=None, searchDelay=10000, continueOnError=False)

    :param selectorString: 目标元素特征码
    :param anchorsElement: 从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）
    :param searchDelay: 查找延时（豪秒）。默认10000
    :param continueOnError: 错误继续执行。默认False
    :return: 目标元素
    """

def GetChildren(target: str | uia.Control, searchType: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> list | uia.Control:
    '''
    获取子元素

    WinElement.GetChildren(element, \'all\', 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象(指定被获取子元素的根节点元素)
    :param searchType: [必选参数]搜索方式。全部子元素(默认):"all" 首个子元素:"first" 最后一个子元素:"last"
    :param searchDelay: [必选参数]超时时间(毫秒)。
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: 目标元素对象的子元素列表 或 首个子元素 或 最后一个子元素
    '''
def GetParent(target: str | uia.Control, searchDelay: int, anchorsElement: uia.Control = None, searchTop: bool = False, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> uia.Control:
    """
    获取父元素

    WinElement.GetParent(element, 10000, anchorsElement=None, searchTop=False, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param searchDelay: [必选参数]超时时间(毫秒)。
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param searchTop: [可选参数]是否搜索顶级父元素。搜索临近一层的父元素(默认):False 搜索顶级的父元素:True
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: 目标元素对象的上一层父级元素 或 顶层父级元素
    """
def GetSibling(target: str | uia.Control, position: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> uia.Control | None:
    '''
    获取相邻元素

    WinElement.GetSibling(element, "next", 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param position: [必选参数]相邻位置。下一个："next"  上一个："previous"
    :param searchDelay: [必选参数]超时时间(毫秒)。
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: 目标元素对象的下一个相邻元素对象 或 上一个相邻元素对象，没有返回None
    '''
def Exists(target: str | uia.Control, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
    """
    判断元素是否存在

    WinElement.Exists(element, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: bool
    """
def GetCheck(target: str | uia.Control, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
    """
    获取元素勾选

    WinElement.GetCheck(element, 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: bool
    """
def SetCheck(target: str | uia.Control, searchDelay: int, isCheck: bool, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
    """
    设置元素勾选

    WinElement.SetCheck(element, 10000, True, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param isCheck: [必选参数]设置勾选:True 设置取消勾选:False
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    """
def GetSelect(target: str | uia.Control, searchDelay: int, mode: str, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> str | int:
    '''
    获取元素选择

    WinElement.GetSelect(element, 10000, \'text\', anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param mode: [必选参数]获取文本："text" 获取序号：“index” 获取值：“value”
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: 已选项的文本 或 序号 或 值，没有则返回None
    '''
def SetSelect(target: str | uia.Control, option: str | int, searchDelay: int, mode: str, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, simulateType: str = 'simulate') -> None:
    '''
    设置元素选择

    WinElement.SetSelect(element, \'\', 10000, \'text\', anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, simulateType=\'simulate\')

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param option: [必选参数]选择选项
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param mode: [必选参数]选择文本："text" 选择序号：“index” 选择值：“value”
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :param setForeground: [可选参数]激活窗口。默认True
    :param cursorPosition: [可选参数]光标位置。中心(默认):"center"  左上角:"topLeft"  右上角:"topRight"  左下角:"bottomLeft"  右下角:"bottomRight"
    :param cursorOffsetX: [可选参数]横坐标偏移。默认0
    :param cursorOffsetY: [可选参数]纵坐标偏移。默认0
    :param simulateType: [可选参数]鼠标点击选中项时的模式。模拟操作(默认):"simulate"   消息操作:"message"
    :return: None
    '''
def GetValue(target: str | uia.Control, getMethod: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> str:
    '''
    获取元素文本

    WinElement.GetValue(element, "auto", 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param getMethod: [必选参数]获取方式。自动方式："auto"  搜元素Name方式："name"  搜元素Value方式："value"。建议使用自动方式
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: 元素文本
    '''
def SetValue(target: str | uia.Control, value: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
    '''
    设置元素文本

    WinElement.SetValue(element, "", 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param value: [必选参数]待写入UI界面元素的文本内容
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    '''
def GetRect(target: str | uia.Control, relativeType: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> dict:
    '''
    获取元素区域

    WinElement.GetRect(element, "parent", 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param relativeType: [必选参数]返回元素位置是相对于哪一个坐标而言的。  相对父元素:"parent"  相对窗口客户区:"root"  相对屏幕坐标:"screen"
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: {"height" : int, "width" : int, "x" : int, "y" : int}
    '''
def ScreenCapture(target: str | uia.Control, filePath: str, rect: dict, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
    '''
    元素截图

    WinElement.ScreenCapture(element, \'D:/1.jpg\', {"x":0, "y":0, "width":0, "height":0}, 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param filePath: [必选参数]图片存储的绝对路径。如 \'D:/1.png\'(支持图片保存格式：bmp、jpg、jpeg、png、gif、tif、tiff)
    :param rect: [必选参数]对指定界面元素截图的范围，如果范围传递为 {"x":0,"y":0,"width":0,"height":0}，则截取该元素的全区域，否则以该元素的左上角为坐标原点，根据高宽进行截图
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: bool(截图成功返回True，否则返回假)
    '''
def Wait(target: str | uia.Control, waitType: str, searchDelay: int, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
    '''
    等待元素（等待元素显示或消失）

    WinElement.Wait(element, \'show\', 10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

    :param target: [必选参数]拾取器获取的目标元素特征字符串或目标元素对象
    :param waitType: [必选参数]等待方式。 等待显示："show"  等待消失:"hide"
    :param searchDelay: [必选参数]超时时间(毫秒)
    :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）默认None
    :param continueOnError: [可选参数]错误继续执行。默认False
    :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
    :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
    :return: None
    '''
