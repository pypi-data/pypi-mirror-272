from re import Pattern, compile

from .FileFly import GetAllDisks, GetAllFiles

# public symbols
__all__ = [
    "GetAllDisk", "GetAllFile"
]


def GetAllDisk(TypeRecord: int | list = True) -> list:
    """获取磁盘列表

    Parameters
    ----------
    TypeRecord : int | list, 可选参数
        磁盘类型,默认为True,返回所有磁盘
        * | 0 | 无法确定驱动器类型 |
        * | 1 | 根路径无效的驱动器 |
        * | 2 | 可移动媒体(如U盘等)|
        * | 3 | 固定驱动器         |
        * | 4 | 远程(网络)驱动器   |
        * | 5 | CD-ROM驱动器       |
        * | 6 | RAM 磁盘           |

    Returns
    -------
    list
        捕获到的磁盘列表

    Example
    _______
    >>> import FileFly
    >>> print(FileFly.GetAllDisk(3))
    ['C:\\\\', 'D:\\\\']

    """
    if TypeRecord is True:
        TypeRecord = list(range(7))
    elif isinstance(TypeRecord, int) and -1 < TypeRecord < 7:
        TypeRecord = [TypeRecord]
    elif isinstance(TypeRecord, list):
        TypeRecord = list(dict.fromkeys(TypeRecord))
        TypeRecord = [E for E in TypeRecord if -1 < E < 7]
    return GetAllDisks(TypeRecord)


def GetAllFile(Path: str,
               Privileges: bool = None,
               Regexp: str | Pattern = None,
               IfPath: bool = None,
               Exclude: bool = None) -> list:
    """获取给定目录的所有文件

    Parameters
    ----------
    Path : str
        给定的目录
    Privileges : bool, 可选参数
        是否使用[SeBackupPrivilege](https://learn.microsoft.com/zh-cn/windows-hardware/drivers/ifs/privileges)和[SeRestorePrivilege](https://learn.microsoft.com/zh-cn/windows-hardware/drivers/ifs/privileges)权限进行文件遍历\n
        使用权限进行文件查找可读取到正在被使用的文件(自动跳过系统HS元文件)\n
        默认为None, 即不使用权限查找文件
    Regexp : str | RegexFlag, 可选参数
        正则表达式, 默认为None, 即不进行正则表达式过滤\n
        可以是正则字符串或经 `re.compile(...)` 编译的正则表达式对象
    IfPath : bool, 可选参数
        当 `Regexp` 参数满足正则要求时, 是否用路径匹配\n
        当该参数为True时, 则使用路径匹配, 否则使用文件名匹配\n
        该参数为None时, 则根据 `Regexp` 参数是否为None来判断\n
        内部实现原理:\n
        ```rust
        let FilePath =
            &[PathBuf::from(Entry.file_name()), Entry.clone().into_path()][IfPath as usize];
        let Results = re.compile(...).search(FilePath).is_truthy()?;
        // let Results = Regexp.search(FilePath).is_truthy()?;
        ```
    Exclude : bool, 可选参数
        当 `Regexp` 参数满足正则要求时, 是否进行反过滤\n
        如果为True(开启反过滤), 则返回不满足正则表达式的文件\n
        如果为False(不开启), 则返回满足正则表达式的文件\n
        默认为None, 即不进行反过滤
        内部实现原理:\n
        ```rust
        if Results as usize + Exclude as usize == 1 {
            File.push(Entry.into_path())
        }
        ```

    Returns
    -------
    list
        根据给定参数捕获到的文件列表

    Example
    _______
    >>> import FileFly
    >>> from re import compile
    >>> print(GetAllFile("D:\\\\", True, compile(r".*\\.png"), False, False))
    ['D:\\\\Downloads\\\\4K壁纸', ...]

    """

    if not isinstance(Path, str):
        raise TypeError("参数 Path 类型错误: ", type(Path))

    if isinstance(Regexp, str):
        Regexp = compile(Regexp)
    elif not isinstance(Regexp, Pattern):
        return GetAllFiles(Path, bool(Privileges))

    return GetAllFiles(Path, bool(Privileges), Regexp, bool(IfPath), bool(Exclude))
