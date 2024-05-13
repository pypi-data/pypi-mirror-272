

def get_path():
    import os
    # 獲取系統的 PATH 環境變量
    path = os.environ.get('PATH')
    if path:
        # 將 PATH 列表打印出來
        print("System PATH:")
        for p in path.split(os.pathsep):
            print(p)
    return 123

def get_pathDD(AAA):
    # import os
    # # 獲取系統的 PATH 環境變量
    # path = os.environ.get('PATH')
    # if path:
    #     # 將 PATH 列表打印出來
    #     print("System PATH:")
    #     for p in path.split(os.pathsep):
    #         print(p)
    return 777+AAA

# if __name__ == "__main__":
#     get_path()
