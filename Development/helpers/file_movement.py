import os
import shutil

def move_error_folder(fileRoot, fileSub, filePath_network, timeStamp, fileName):
    dirExists = os.path.exists(fileRoot + "/Error/" + fileSub + "/")
    if not dirExists:
        os.makedirs(fileRoot + "/Error/" + fileSub + "/")
    shutil.move(filePath_network, fileRoot + "/Error/" + fileSub + "/" + timeStamp + '_' + fileName)


def move_partial_folder(fileRoot, fileSub, filePath_network, timeStamp, fileName):
    dirExists = os.path.exists(fileRoot + "/Partial/" + fileSub + "/")
    if not dirExists:
        os.makedirs(fileRoot + "/Partial/" + fileSub + "/")
    shutil.move(filePath_network, fileRoot + "/Partial/" + fileSub + "/" + timeStamp + '_' + fileName)

def move_archive_folder(fileRoot, fileSub, filePath_network, timeStamp, fileName):
    dirExists = os.path.exists(fileRoot + "/Archive/" + fileSub + "/")
    if not dirExists:
        os.makedirs(fileRoot + "/Archive/" + fileSub + "/")
    shutil.move(filePath_network, fileRoot + "/Archive/" + fileSub + "/" + timeStamp + '_' + fileName)
