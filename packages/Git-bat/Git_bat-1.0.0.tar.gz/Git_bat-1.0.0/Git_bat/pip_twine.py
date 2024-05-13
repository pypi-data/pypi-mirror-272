import sys,os
def pip_twine( file_path = os.path.join(os.path.expanduser("~"), ".pypirc") ):
    # if os.name == "nt":
    #     file_path = os.path.join(os.getcwd(), ".pypirc")
    # else:

    # if  passs:passs=sys.argv[0] if len(sys.argv)==1 else "" ,
        import os
        os.system("python setup.py sdist")
        # print( f"twine upload --skip-existing  dist/*  --config-file {file_path}" )
        print(os.popen(f"twine upload --skip-existing  dist/*  --config-file {file_path}").read())
        print("pause            ")
        input("pause")
    # else:
    #     print("不建立檔案. ")


