"""本模块提供一些关于文件系统路径处理的帮助函数"""
import os
import shutil


def is_ignore(path, *patterns):
    """判断path是否被忽略

    目前能只能处理文件,无法处理目录通配符

    Args:
        path: 被匹配的路径,确保该路径是合法路径,末尾可以有/或者\
        patterns: 模式,可使用下面的通配符

            | Pattern | Meaning                           |
            | ------- | --------------------------------- |
            | *       | matches everything                |
            | ?       | matches any single character      |
            | [seq]   | matches any character in*seq*     |
            | [!seq]  | matches any character not in*seq* |
    """

    path = os.path.normcase(path)
    patterns = (os.path.normcase(pattern) for pattern in patterns)

    a = shutil.ignore_patterns(*patterns)
    c = a(None, (path,))
    return True if c else False


def abspath(real_path, suffix=None):
    """根据一个相对路径和前缀得到绝对路径

    如果没有前缀,则前缀为当前目录(os.path.abspath的默认行为),否则
    就前缀添加在前面在去求解,这里要求前缀是一个绝对路径

    eg:
        oslib.abspath(r'../hello',r'E:\MyComputer\Workspace\项目\')
        # E:\MyComputer\Workspace\hello
    """
    if suffix is None:
        return os.path.abspath(real_path)
    else:
        if os.path.isabs(suffix):
            path = os.path.join(suffix, real_path)
            return os.path.abspath(path)
        else:
            raise OSError('{}不是绝对路径'.format(suffix))
