import glob
from pathlib import Path
import shutil

import pkg_resources


def getPackagedFilePathStrict(pkgName: str, fileName: str = None) -> str:
    """
        pkgName : str format package style :- com.fol1.fol2.fol3....
        fileName : str :- any file name with extension.
        it will raise :- ModuleNotFoundError if entire package name does not exist.
        it will raise :- FileNotFoundError if given fileName does not exists in the given package.
        if fileName ="" or fileName==None, then it simply returns absolute path of the package.
    """
    fileName = pkg_resources.resource_filename(pkgName, fileName)
    if exists(fileName):
        return fileName
    else:
        raise FileNotFoundError(fileName)


def getPackagedFilePath(pkgName: str, fileName: str) -> str:
    """
        pkgName : str format package style :- com.fol1.fol2.fol3....
        fileName : str :- any file name with extension.
        It will raise :- ModuleNotFoundError if first packaged directory is not found.
        It will not check entire package existance or file existance. it simply
        returns absolute file path wrt first packaged directory.
    """
    resultPath = []
    pkgs = pkgName.split(".")
    v = pkg_resources.resource_filename(pkgs[0], "")
    resultPath.append(v)
    resultPath.append("/".join(pkgs[1:]))
    resultPath.append(fileName)
    return "/".join(resultPath)


def toPath(path: str) -> Path:
    """
    """
    if not isinstance(path, str):
        raise TypeError(
            "TypeError : path must be of type str (path like) , Provided '{}' type.".format(path.__class__.__name__))
    if path.strip() == "":
        raise ValueError("ValueError : path can't blank")
    try:
        result = Path(path)
    except TypeError:
        raise TypeError(
            "TypeError : path must be of type str (path like) , Provided '{}' type.".format(path.__class__.__name__))
    return result


def exists(path: str, ifPathNotExistsRaiseError: bool = False) -> bool:
    """
        path : str (path like)
        returns : bool
            true if fileName/FolderName/Any path provided exists, otherwise returns false
    """
    path = toPath(path)
    pathExists = path.exists()

    if pathExists:
        return pathExists
    else:
        if ifPathNotExistsRaiseError:
            raise FileNotFoundError("FileNotFoundError : File/Folder '{}' not exists.".format(path))
        return pathExists


def getPath(fileNamePattern: str) -> str:
    """
        fileNamePattern :- regexed pattern path for a unique existing file/path name.
        if givenPattern is does not exists for any unique file/Path then -> FileNotFoundError
        if givenPattern returns multiple file/Paths then ->AttributeError
        if pattern returns only one matching file/path name :- Then it returns complete matched path/file name.
    """
    try:
        fileNamesList = glob.glob(fileNamePattern)
        if len(fileNamesList) > 1:
            raise AttributeError(
                "MultipleFileNamesFoundError : Multiple File Names found with fileNamePattern : '{}'".format(
                    fileNamePattern))
        return fileNamesList[0]
    except IndexError:
        raise FileNotFoundError("FileNotFoundError : file '{}' not found".format(fileNamePattern))


def toExcel(fileName: str) -> str:
    """
        fileName :- str
        fileName -> File name without extension . fileName must exists.
        It appends the proper excel extension to file name.
    """
    if isinstance(fileName, str):
        pattern = fileName + ".xls*"
    else:
        raise TypeError("TypeError : file name must be str, provided '{}' type".format(fileName.__class__.__name__))
    result = getPath(pattern)
    return result


def createPath(path: str) -> None:
    """
        It creates the path if not exists and pass if exists.
    """
    existsPath = exists(path)
    if not existsPath:
        pathToCreate = Path(path)
        pathToCreate.mkdir(parents=True)


def deletePath(path: str) -> None:
    """
        if Path not existing then ->Pass
        If Path is existing file Name :- raise NotADirectoryError
        if Path is opened or is in used :- raise PermissionError
    """
    if exists(path):
        try:
            shutil.rmtree(path)
        except PermissionError:
            raise PermissionError("FileIsOpened : File/Folder : '{}' is in used by another application".format(path))


def deleteFile(filePath: str):
    """
        If filePath not exists -> pass
        If filePath is not file ->ValueError
        if filePath is file but file is in used -> PermissionError
    """

    if exists(filePath):
        filePath = toPath(filePath)
        if not filePath.is_file():
            raise ValueError(
                "NotAFileError : Path given : '{path}' is not file path, can't delete it".format(path=filePath))
        try:
            filePath.unlink()
        except PermissionError:
            raise PermissionError(
                "FileIsOpened : File : '{filePath}' is in used by another application, can't delete it.".format(
                    filePath=filePath))