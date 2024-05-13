import sys
def pip_MD(passs=sys.argv[1] if len(sys.argv)==2 else "" ,name= "__token__"):
    # if os.name == "nt":
    #     file_path = os.path.join(os.getcwd(), ".pypirc")
    # else:

    if  passs:
        passs=passs.strip()
        os = __import__('os')
        if os.name != "nt":
            # file_path = "/root/.pypirc"
            # with open(file_path, "w") as f:
            #     f.write("[pypi]\n")
            #     f.write("repository: https://upload.pypi.org/legacy/\n")
            #     f.write(f"username: {name}\n")
            #     f.write(f"password: {passs}\n")
            pass
        else:
            file_path = os.path.join(os.path.expanduser("~"), ".pypirc")
            with open(file_path, "w") as f:
                f.write("[pypi]\n")
                f.write("repository: https://upload.pypi.org/legacy/\n")
                f.write(f"username: {name}\n")
                f.write(f"password: {passs}\n")

            # print(file_path  , os.path.expanduser("~") ,os.path)
    else:
        print("不建立檔案. ")


# pip_MD( "__token__",sys.argv[2].strip() )
        

# twine upload --repository pypi test_package.tar.gz
# twine upload --repository pypi dist/*
