import sys,subprocess
# print("@ sys @",sys.argv)
class Var:
    # nameA = 'pip'
    # nameB = '0.2.0'
    ### 修改參數 ###
    @classmethod
    def update_names(cls, name=None, vvv=None):
        """
        更新
        """
        if name is not None and vvv is not None:
            cls.nameA = name
            cls.nameB = vvv
          
            print(f"已更新 nameA={cls.nameA}, nameB={cls.nameB}")
            print("-"*50)

            # 修改文件内容
            # filename = __file__   # 替换成你的脚本文件名
            with open( "setup.py" , 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if "### 修改參數 ###" in line:
                        lines[i-2] = f"    nameA = '{name}'\n"
                        lines[i-1] = f"    nameB = '{vvv}'\n"
                        break  # 找到后就退出循环
                f.seek(0)
                f.writelines(lines)
                f.truncate()
                # 刷新檔案緩衝區
                f.flush()
                f.close()
              
               ##  這邊會導致跑二次..............關掉一個
       
             
        else:
            print("未提供足够的参数")
    
    @classmethod
    def gitNAME(cls,name="name"):
        import subprocess
        # 讀取 Git 使用者名稱
        result = subprocess.run(['git', 'config', f'user.{name}'], capture_output=True, text=True)

        # 如果命令成功執行，則輸出使用者名稱
        if result.returncode == 0:
            git_user_name = result.stdout.strip()
            # print(f"Git 使用者名稱: {git_user_name}")
            return git_user_name
        else:
            # print("無法讀取 Git 使用者名稱")
            return False
    # name=gitNAME()
    # pypi=gitNAME('pypi')
    @classmethod
    def pip_MD(cls,name, passs):
        # if os.name == "nt":
        #     file_path = os.path.join(os.getcwd(), ".pypirc")
        # else:
        if os.name != "nt":
            file_path = "/root/.pypirc"
            with open(file_path, "w") as f:
                f.write("[pypi]\n")
                f.write("repository: https://upload.pypi.org/legacy/\n")
                f.write(f"username: {name}\n")
                f.write(f"password: {passs}\n")
    @classmethod
    def pip_exists(cls,package_name):
        import os,importlib
        if  os.name=="nt":
            print("條件必須[linux]環境")
        else:
            try:
                importlib.import_module(package_name)
            except ImportError:
                NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
                os.system(f"pip install {package_name} {NU}")
    @classmethod
    def pip_twine( cls,URL="https://gitlab.com/moon-0516/cmd.pop@0.11.0" ):
        import os
        if  os.name=="nt":
            print("條件必須[linux]環境")
        elif URL.count("@")==1:
            os.chdir("/content")
            A,B=URL.split("@")
            NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
            print(f"git clone -b {B} {A} {NU}")  
            
            name=os.path.basename(A)
            print("")
            if  os.system(f"git clone -b {B} {A}")==0:
                os.chdir(name)
                os.system(f"rm -rf /content/.git")
                os.system("python setup.py sdist")
                print(os.popen("twine upload --skip-existing  dist/*  --config-file /root/.pypirc").read())
                print("pause            ")
                input("pause")
                
            os.chdir("../")
            os.system(f"rm -rf /content/{name}")
        else:
            print("格式不對")
    @classmethod
    def  clear(cls):
            ###############################################################################
            import os
            if os.name!="nt":
                os.system("rm -rf ~/.cache/pip/*")
            else:
                os.system(f"rmdir /q /s %LOCALAPPDATA%\pip\cache")
            ################################################################################
    ############
    ############
    # pypi.Var.run(self,Var.nameA) ## del[cmd_pop]
    @classmethod
    def run(cls,  this=None , install=None ,nameA="cmd.pop" ):
        #####

        ###################################
        def del_file(directory = "/path/to/your/directory"):
            import os
            # 如果目錄存在，則刪除其中的所有檔案
            if os.path.exists(directory):
                [os.remove(os.path.join(directory, file)) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
                print("所有檔案已刪除。")
            else:
                print(f"目錄 '{directory}' 不存在。")
        ###################################
        ###################################
        # from setuptools.command.install import install
        import os
        data = {}    
        PWD=os.getcwd()
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            print( os.path.basename(root) in [i for i in os.listdir( PWD )if i[0]!="."] )
            if  root.find(os.path.sep+".git")==-1:
                ######################################## 
                ######################################## 
                print(root , dirs , files)
                ################################################################### 
                ######################################## def 刪除路徑下的 所有檔案
                BB=nameA.split(".")               ### [nameA] ###
                if "_".join(BB)==os.path.basename(root):         
                    print( "@@## ",root )         
                    del_file( root )
                    # os.system(f"rmdir /q /s %LOCALAPPDATA%\pip\cache")
                print( "@@ ## "*10 )
        return install.run( this )
    
    
    @classmethod
    def cmds(cls,command = "pip install cmd.pop==9999999999"):
        import subprocess
        # 定義你的命令
        # command = "pip install cmd.pop==9999999999"
        # 使用 subprocess.run() 執行命令
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 獲取標準輸出和標準錯誤
        output = result.stdout.decode("utf-8")
        error = result.stderr.decode("utf-8")

        # 判斷命令是否執行成功
        return output if result.returncode == 0 else error

    @classmethod
    def pipIF(cls,name="cmd.pop"):
        #####################################
 
        # SS = cls.cmds(command = f"pip install {name}==9999999999")
        # import re 
        # R= re.findall(".*[,](.*)[)].*",SS,re.S)
        # return R.pop() if len(R)==1 else "0.0.1"
        ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # git ls-remote --tags gitlab2
        import subprocess,os
        os.system("git init")
        # 定義命令
        NU = ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        NU2 = "2> nul" if os.name == "nt" else "2> >/dev/null" ## 排除--錯誤訊息
        command = f"git log --oneline --tags --no-walk -n 1 {NU2}"
        # print(os.system(command)==0)
        # print("@",os.popen(command).read())
        # 使用 subprocess.run() 運行命令

        RB = os.popen(command).readline()
        print("@@",len(RB) ,RB)
        if  len(RB)==0:
            return "0.0.1"
        else:
            return RB[1]   
        
        
    @classmethod
    def create_init_files(cls,directory):
        import os
        for root, dirs, files in os.walk(directory):
            # 在当前目录中创建 __init__.py 文件
            init_file_path = os.path.join(root, '__init__.py')
            with open(init_file_path, 'w') as init_file:
                pass  # 可以留空，也可以添加一些内容


    @classmethod
    def clone_commit(cls,url="https://gitlab.com/moon-0516/cmd.pop"):
        import os
        print(os.popen(f"git fetch {url}").read())
        print(os.popen(f"git pull -X theirs {url}").read())


    #########
    ## end ##
    #########

    

#########################################
def remove_contents(directory_path):
    import os,shutil
    try:
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        # del  /f /s /q  E:\moon-0516\cmd.pop
        os.system(f'del  /f /s /q  {directory_path}') ### 刪除此目錄底下--所有檔案 
        print(f"成功刪除目錄內容: {directory_path}")
    except Exception as e:
        print(f"刪除目錄內容時發生錯誤: {e}")
        pass
#########################################
    
    
def pip_api(moon="moon-start",name=""):

    token=gitNAME('api').split(":")
    token=False if len(token)==1 else token[1]
    if not token:
        return token
    ###################################
    if  not token :
        print(f"@ token {token} 不存在 @")
        os._exit(0)
    # !curl --header "PRIVATE-TOKEN: KEY" "https://gitlab.com/api/v4/projects/moon-start%2FBAT."
    import requests
    url = f"https://gitlab.com/api/v4/projects/{moon}%2F{name}"
    headers = {"PRIVATE-TOKEN": token }
    # headers = {"PRIVATE-TOKEN": "KEY"}
    response = requests.get(url, headers=headers)
    # print(response.status_code==200)
    # print(response.json())
    return response.status_code==200

def pip_tag(moon="moon-start",name=""):
    token=gitNAME('api').split(":")
    token=False if len(token)==1 else token[1]
    if not token:
        return token
    # namespace = "moon-start"
    ###################################
    if  not token :
        print(f"@ token {token} 不存在 @")
        os._exit(0)
    # !curl --header "PRIVATE-TOKEN: KEY" "https://gitlab.com/api/v4/projects/moon-start%2FBAT."
    import requests
    # url = f"https://gitlab.com/api/v4/projects/moon-start%2F{name}"
    url_tag = f"https://gitlab.com/api/v4/projects/{moon}%2F{name}/repository/tags"
    headers = {"PRIVATE-TOKEN": token }
    # headers = {"PRIVATE-TOKEN": "KEY"}
    response = requests.get(url_tag, headers=headers)
    # print(response.status_code==200)
    # print(response.json())
    # return response.status_code==200
    RR=[]
    if response.status_code == 200:
        tags_info = response.json()
        # print("Project Versions:")
        for tag in tags_info:
            # print("pip_tag",tag.get("name"))
            RR.append(tag.get("name"))
    else:
        print("!=200")
        # print(f"Error getting tags: {response.status_code}")
    ## 排序
    keyIF = lambda x: tuple(map(int, x.split('.')))
    TG=sorted(RR,key=keyIF)
    print("pip_tag():",TG)
    return TG

def gitNAME(name="name"):
    import subprocess
    # 讀取 Git 使用者名稱
    result = subprocess.run(['git', 'config', f'user.{name}'], capture_output=True, text=True)


    # 如果命令成功執行，則輸出使用者名稱
    if result.returncode == 0:
        git_user_name = result.stdout.strip()
        # print(f"Git 使用者名稱: {git_user_name}")
        return git_user_name
    else:
        # print("無法讀取 Git 使用者名稱")
        # returninput("@ [pip api] : ")
        return False
    

# home = os.path.basename(os.getcwd())
# pwd  = 
##################### git config user.{name}
##################### 專案 讀取 
# moon=gitNAME("moon")
import os
moon=os.path.basename(os.path.dirname(os.getcwd()))
# moon="moon-start"
name=gitNAME()
pypi=gitNAME('api')
##########################################################
import sys,os   
if len(sys.argv)==4:
    if   sys.argv[1]=="moon"  and sys.argv[3]=="ok":
        import os
        name=str(sys.argv[2])
        os.system(f"git config --global user.moon {name}")
        os._exit(0)
    if  sys.argv[1]=="del"  and sys.argv[2]=="ok":
        import os
        def remove_contents(directory_path):
            try:
                for item in os.listdir(directory_path):
                    item_path = os.path.join(directory_path, item)
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                # print(f"成功刪除目錄內容: {directory_path}")
            except Exception as e:
                # print(f"刪除目錄內容時發生錯誤: {e}")
                pass
        #########################################
        import shutil
        def rmdirDIR(path):
            try:
                shutil.rmtree(path)
                # print(f"成功刪除目錄: {directory_path}")
            except Exception as e:
                # print(f"刪除目錄時發生錯誤: {e}")
                pass
        #########################################
        import os
        def gitD():
            if os.name == "nt":  # Windows
                os.system(f'rmdir /s /q .git')
            else:  # Unix/Linux
                os.system(f'rm -rf .git')
        #########################################
        home = os.getcwd()
        ########################################
        # 呼叫函數以刪除目錄
        # rmdirDIR(f"{home}{os.path.sep}.git")
        gitD()
        # remove_contents( f"{home}{os.path.sep}.git" )
        # print("[刪除] .git 目錄 ")

        import os
        if  sys.argv[3]=="ok":
            # try:
            #     input("[pause] 全部 Del ?? ")
            # except KeyboardInterrupt:
            #     print("\n操作被中斷。")  ## Ctrl+C
            #     os._exit(0)
          
            # 使用範例
            remove_contents( home )
            print(f"已確認移除。[OK]")
        else:
            try:
                # print("123", end=' ')## 只可以用在print
                input(f"[pause] {sys.argv[3]} Del ?? ")
            except KeyboardInterrupt:
                print("\n操作被中斷。") ## Ctrl+C
                os._exit(0)
            rmdirDIR(f"{home}{os.path.sep}{sys.argv[3]}")
            print(f"已確認移除。[OK]")
        os._exit(0)



import os,sys
if len(sys.argv)==4 or len(sys.argv)==3:
    ########################################################################
    if  sys.argv[1]=="-D" and sys.argv[2]=="init":
        print(f"缺少。[all]")
        os._exit(0)
    elif  sys.argv[1]=="-D" and sys.argv[2]=="init" and sys.argv[3]=="all":
        home = os.getcwd()
        remove_contents( home ) 
        print(f"已確認移除。[OK]")
        os._exit(0)
    ##########################################################################
    if  sys.argv[1]=="-D" and sys.argv[2]=="tag"  and  len(sys.argv)==3:    
        print(f"缺少。[all]")
        os._exit(0)
    
    elif  sys.argv[1]=="-D" and sys.argv[2]=="tag":    
        # git push origin --delete <tagname>
        # os.system(f'git push origin --delete {sys.argv[3]}')
        os.system(f'git tag -d {sys.argv[3]}')
        os.system(f'git push gitlab --delete {sys.argv[3]}')
        os._exit(0)
   
        
if len(sys.argv)==2:
    if sys.argv[1]=="-H":
        print(r"@ [1] pip -IN {版本號} @ ..........安裝")
        print(r"@ [1] pip -UP {版本號} @ ..........上傳")
        # print("#"*100)
        os._exit(0)
   #########################################################
    if   sys.argv[1]=="-R":
        print(os.popen("git remote -v").read())
        print("#"*100)
        os._exit(0)
    ##########################################################
    if   sys.argv[1]=="-UN":
        import os
        home = os.path.basename(os.getcwd())
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        os.system(f"pip cls {NU}") ## 缺一不可
        print(f"@ [使用] pip uninstall { home } -y  @")
        print(os.popen(f"pip uninstall { home } -y ").read())
        os._exit(0)
    if sys.argv[1]=="save":
        import os,sys
        home = os.path.basename(os.getcwd())
        pwd  = os.path.basename(os.path.dirname(os.getcwd()))
        # NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        ### 只有排除.....錯誤的部分輸出
        NU2 = "2> nul" if os.name == "nt" else "2> >/dev/null"
        R=[ i.lstrip("Version:").strip() for i in os.popen(f"pip show {home} {NU2}").readlines()if str(i).startswith("Version:")]
        HR=[ i.lstrip("Home-page:").strip() for i in os.popen(f"pip show {home} {NU2}").readlines()if str(i).startswith("Home-page:")]
        home = os.path.basename(os.getcwd())
        # print(len(HR) , len(R),HR,pwd)
        if len(HR)!=0 and len(R)!=0:
            if HR[0]==pwd:
                # print(R[0])
                # sys.argv = [sys.argv[0],"-UN",home,"&&",sys.argv[0],"-UP",R[0]]
                sys.argv = [sys.argv[0],"-UP",R[0]]
                # print("!!!")
            else:
                print(f"# [模型-已存在] :")
                print(f"@ Home-page: {HR[0]}  @\n")
                os._exit(0)
        else:
            print(f"@ 電腦中 此[{pwd}]-模組 尚未安裝 @")   
            print("")
            print(r"@ [功能]:  ---自動 pip -UP {版本} @")
            print(r"@ [條件]:  ---自動 pip -IN {版本} @")
            os._exit(0)

    if sys.argv[1]=="-init":
        import os
        home = os.path.basename(os.getcwd())
        NN   = home.split(".")      
        if  os.path.isdir( "_".join(NN) ):
            Var.create_init_files( "_".join(NN) )
        else:
            print(f"@ [條件] pip -G init @")
            os._exit(0)

    
    if sys.argv[1]=="-log":
        import os
        # print(os.popen("git log --oneline").read())
        # os._exit(0)

        import  shutil
        # 查找 pip 的完整路径
        pip_path = shutil.which('pip') #### 他只接受 pip........... argv.[0]
 
        ### -log ###
        import subprocess,os, shutil
        os.system("git fetch gitlab --tags")
        git_path = str(shutil.which('git'))
        # git_command = 'log --oneline --graph'
        git_command = 'log --oneline --tags --no-walk'
        # 在新的 cmd 窗口中执行 Git 命令
        subprocess.Popen(['cmd', '/c', f'start cmd /k {git_path} {git_command}'], shell=True) # 新終端::顯示
        # subprocess.Popen(['cmd', '/c', f'{git_path} {git_command}'], shell=True)  ############# 本終端::顯示  ............不使用::會清除掉紀錄
        os._exit(0)
        ### -log ###
     
    if sys.argv[1]=="-CP":
        import os
        Var.clone_commit("https://gitlab.com/moon-0516/cmd.pop")
        os._exit(0)
        ######



  
# git config --list
if len(sys.argv)==3:
    if sys.argv[1]=="-IN":
        os.system("git fetch gitlab --tags")
        home = os.path.basename(os.getcwd())
        sys.argv = [sys.argv[0],"-install",f"{home}=={sys.argv[2]}"]
    if sys.argv[1]=="-UP":
        if  sys.argv[2].count(".")!=2:
            print(f"@ [請修正版本] XX.XX.XX @")
            os._exit(0)
        ########################################################
        # print(os.popen(f"pip -G --moon").read().strip()) #XX
        value = os.popen(f"git config user.moon").read().strip()
        home = os.path.basename(os.getcwd())
        if  len(value)==0:
            print(f"@ [缺少環境] user.moon @")
            os._exit(0)
        
        ########################################################        
        # import os
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        # os.system(f"pip cls {NU}") ## 缺一不可
        print(f"pip setup.py { home } {sys.argv[2]}")
        # print(os.popen(f"pip setup.py cmd.pop {sys.argv[2]}").read())
        # os._exit(0)
        sys.argv = [sys.argv[0],"setup.py",  home ,sys.argv[2]]
        print("- "*25)
    
    if sys.argv[1]=="-UN":
        import os
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        os.system(f"pip cls {NU}") ## 缺一不可
        print(f"@ [使用] pip uninstall {sys.argv[2]} -y  @")
        print(os.popen(f"pip uninstall {sys.argv[2]} -y ").read())
        os._exit(0)
    ##########################################################
    if   sys.argv[1]=="-L" and sys.argv[2]=="file":
        print(os.popen("git diff main gitlab/main").read())
        os._exit(0)
    ##########################################################
    if   sys.argv[1]=="-G" and sys.argv[2]=="url":
        print(os.popen("git remote -v").read())
        os._exit(0)
    elif sys.argv[1]=="-G" and  sys.argv[2][0:2]=="--":
        import os
      
        # if os.name=="nt": #### 在 win 11 使用
        ##########################################
        name = sys.argv[2][2::]
        # print(f"git config user.{name}")
        value = os.popen(f"git config user.{name}").read().strip()
        ##########################################
        print(f"## [user.{name}] {value}  ") 
        os._exit(0)
    elif sys.argv[1]=="-G" and sys.argv[2]=="del":
        home = os.getcwd()
        remove_contents( home ) 
        # print(f"已確認移除。[OK]") ###########################
        os.system("pip del ok ok")
        os._exit(0)
    elif sys.argv[1]=="-G" and sys.argv[2]=="init":


        import os
        home = os.path.basename(os.getcwd())
        NN   = home.split(".")
        if len(NN)==2:
            ###############################################################################
            if ".git" in os.listdir():
                print("# [提示] (git init) 已建立")
                print("# [提示] 停止 pip init 後面動作")
            else:
                # 创建目录
                os.makedirs( "_".join(NN) , exist_ok=True)
                # 在目录中创建 __init__.py 文件
                open( "."+os.path.sep+"_".join(NN)+os.path.sep+"__init__.py" , 'w').write(" ")
                #######################################################
                os.system("git init ")
                pwd=os.path.basename(os.path.dirname(os.getcwd()))
                moon=os.path.basename(os.path.dirname(os.getcwd())) ## 避免::不同步
                # os.system(f"git config user.moon {pwd}")
                os.system(f"git config user.home {home}") ## nameA 名稱
                #########################################################
                ## [建檔]
                ######################################################## 拷貝 ##
                sys.argv.pop(1)
                sys.argv.pop(1)
                sys.argv.append("-V")
                #####################
                nameA = os.popen("git config user.home").read().strip()
                NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
                if os.system(f'git remote get-url gitlab {NU}')!=0:
                    os.system(f"git init")
                    os.system(f"git remote add gitlab https://{ pypi }@gitlab.com/{moon}/{nameA}")
                    print(f"@ [位置] @ git remote add gitlab https://pypi:{ pypi }@gitlab.com/{moon}/{nameA} @")
                ######################
                TTAG = Var.pipIF( nameA ).strip()
                print("@TTAG:",TTAG,TTAG=="0.0.1")
                if TTAG=="0.0.1":
                    try:
                        from cmd_html import setupPIP
                        text=open( setupPIP.__file__ ,"r",encoding='utf8').read()
                        open( "setup.py"  ,"w",encoding='utf8').write(text)
                        nameA = os.popen("git config user.home").read().strip()
                        os.system(f"pip setup.py {nameA} 0.0.1")
                        del text,nameA
                    except Exception as e:
                        # 在這裡處理提醒的邏輯
                        # print(f"提醒: {e}") ###### 如果尚未安裝的話
                        # import re 
                        # R= re.findall(".*[,](.*)[)].*",Var.cmds(),re.S)
                        # TTAG = str(R.pop()).strip() if len(R)==1 else "0.0.1"
                        print(r"@ [條件]:  ---自動 pip -IN {版本} @")
                        print(r"@ [問題]:  ---缺少模組 安裝setup.py @")
                        TTAG = pip_tag("moon-0516",nameA).pop()
                        print("@TTAG:",TTAG,TTAG=="0.0.1")  
                        print(f"提醒: pip -install cmd.pop=={TTAG} [需要在 moon-0516目錄]")
                        print(f"提醒: pip -IN {TTAG}               [需要在 moon-0516目錄]")
                        # print(f"提醒: gitlab 專案尚未存在")
              
                ############
                else:

                    # os.system(f"pip del ok ok {NU}")
                    os.system("pip del ok ok")
                    ####################################
                    # # os.system(f"git fetch gitlab ")
                    # os.system("git branch --set-upstream-to=gitlab/main main")
                    os.system("git pull gitlab main  --rebase")
                    print(f"\n[提醒]: 已存在專案 正在下載ing..") ###### 如果尚未安裝的話
                    # url =  f"https://{ pypi }@gitlab.com/{moon}/{TTAG}"
                    # print(f"git clone {url} . -o gitlab")
                    # os.system(f"git clone {url} . -o gitlab")
                    # del url
                    ###############
                    # try:
                    #     from cmd_html import setupPIP
                    #     text=open( setupPIP.__file__ ,"r",encoding='utf8').read()
                    #     open( "setup.py"  ,"w",encoding='utf8').write(text)
                    #     nameA = os.popen("git config user.home").read().strip()
                    #     os.system(f"pip setup.py {nameA} {TTAG}")
                    #     del text,nameA
                    # except Exception as e:
                    #     # 在這裡處理提醒的邏輯
                    #     # print(f"提醒: {e}") ###### 如果尚未安裝的話
                    #     import re 
                    #     R= re.findall(".*[,](.*)[)].*",cmds(),re.S)
                    #     TTAG = R.pop() if len(R)==1 else "0.0.1"
                    #     print(f"提醒: pip -install cmd.pop=={TTAG}")
                    # git config user.moon
                        
            os._exit(0)
        else:
            print("# [提示] 專案名稱沒有[.] ")
            print("# [提示] 無法 (git init)")
            os._exit(0)

    ###########################################################
    if  sys.argv[1]=="clone-MD":
        Var.pip_MD( "__token__",sys.argv[2].strip() )
        os._exit(0)
    if  sys.argv[1]=="clone-UP":
        Var.pip_exists("twine")
        Var.pip_twine( sys.argv[2].strip()  )
        os._exit(0)

    if   sys.argv[1]=="name":
        import os
        name=str(sys.argv[2])
        os.system(f"git config --global user.name {name}")
        os.system(f"git config --global init.defaultBranch main")
        os._exit(0)
    elif sys.argv[1]=="api":
        import os
        KEY=str(sys.argv[2])
        ###################################################
        # if os.name=="nt":
        #     os.system("rmdir /s /q .git")
        # else:
        #     os.system("rm -rf .git")
        ###################################################
     
            # if not BBL:
            #     print("@ 重新執行 @")
            #     os._exit(0)
        if ".git"  in os.listdir(os.getcwd()):
            pypi = os.popen("git config --global user.api").read().strip()
            SA =  os.path.basename(os.popen("git remote get-url gitlab").read().strip())
            os.system(f"git remote  set-url gitlab https://{ pypi }@gitlab.com/{moon}/{SA}")
            print(f"@ [位置] @ git remote  set-url   https://{ pypi }@gitlab.com/{moon}/{SA} @")
   

        ###################################################
        os.system(f"git config --global  user.api {KEY}")
        os._exit(0)
 

        
    elif sys.argv[2]=="get":
        import os
        if os.name=="nt": #### 在 win 11 使用
            ##########################################
            name = sys.argv[1]
            value = os.popen(f"git config user.{name}").read().strip()
            ##########################################
            print(f"## [user.{name}] {value}  ") 
            os._exit(0)




    elif sys.argv[1]=="load" and sys.argv[2]=="pip":
        import os
        if os.name!="nt":
            ##########################################
            # from IPython import get_ipython
            # # 取得 IPython 實例
            # ip = get_ipython()
            # # 使用 os.system() 來執行 %load_ext pip
            # import os
            # os.system("jupyter nbextension enable --py widgetsnbextension")
            # # 或者使用 IPython 的 run_line_magic 方法
            # ip.run_line_magic("load_ext", "pip")
            # # ip.run_line_magic("load_ext", "PY檔名")
            ##########################################
            print(f"@ [使用] %load_ext  pip  @") 
            os._exit(0)


 
if len(sys.argv)==2:
    # print("!!")
    if  sys.argv[1]=="api":
        import os
        os.system("git config --global --unset user.api")
        print("@ git config --global --unset user.api 移除 @") 
        os._exit(0)
    elif  sys.argv[1]=="moon":
        import os
        os.system("git config --global --unset user.moon")
        print("@ git config --global --unset user.moon 移除 @") 
        os._exit(0)
    ########################
    ########################
    elif sys.argv[1]=="pop":
        import os
        dictQ={i.split("=")[0][5::] : i.split("=")[1] for i in os.popen("git config --global --list").read().split("\n")if i[0:4]=="user"}
        # if "name" in dictQ.keys():
        #   S=dictQ["name"]
        #   print(S)
        
        print(f"@ user: {dictQ} @")
        os._exit(0)
    
    elif sys.argv[1]=="cls":
        Var.clear()
        os._exit(0)
    elif sys.argv[1]=="MD":
        print("")
        print("https://colab.research.google.com/drive/1jl5xJiOqFz5Bcj7SdPsF1VmBVR_dCWb0")
        os._exit(0)
    if len(sys.argv)==2:
        # if  sys.argv[1][0]==r"%" and  len(sys.argv[1])!=1  :
        if  sys.argv[1]==r"%pip" and  len(sys.argv[1])!=1  :
            print(f"@ [使用] %load_ext  pip  @") 
            os._exit(0)


# pip setup.py cmd.pop 0.1.0
if len(sys.argv)==4:
    if  sys.argv[1]=="setup.py" and moon and pypi:
        SA,SB = sys.argv[2],sys.argv[3]
        ########################################################
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        if os.system(f'git remote get-url gitlab {NU}')!=0:
            os.system(f"git init")
            os.system(f"git remote add gitlab https://{ pypi }@gitlab.com/{moon}/{SA}")
            print(f"@ [位置] @ git remote add gitlab https://pypi:{ pypi }@gitlab.com/{moon}/{SA} @")
        else:
            import re
            URL = os.popen("git remote get-url gitlab").read().strip()
            KEY=re.findall(r'https://([^/^@]+)@gitlab\.com/[^/^@]+/[^/^@]+$',URL)
            if len(KEY)!=0:
               KEY=KEY[0]
               URL = re.sub( f"//{KEY}@", f"//{pypi}@" ,URL )
            else:
                os.system(f"git remote  set-url gitlab {URL}")
                print(f"@ [位置] @ git remote  set-url  {URL} @")
                print("-"*50)
                os._exit(0)

            # print("@!! URL ",KEY,pypi,URL)
            # print("@ URL ",URL)

     
        #####################################################
        Var.update_names( SA,SB )

        
        if  not pip_api(moon,SA):
            print(f"@ 專案不存在 @")
            os._exit(0)


        # # print("@ SA :",pip_tag(moon,SA),SB)
        # if  pip_tag(moon,SA)==[]:
        #     print("# ",os.popen(f"git add . ").read())
        #     print("# ",os.popen(f"git commit -m \"{ SB }\" ").read())
        #     print("# ",os.popen(f"git tag { SB } ").read())
        #     #########################################################
        #     print("# ",os.popen(f"git push -u gitlab main").read())
        #     print("# ",os.popen(f"git push --tags").read())
        # else:
        #     # print( "@ SB :" ,SB in pip_tag(moon,SA)  )
        #     if  SB in pip_tag(moon,SA):
        #         # 刪除本地標籤
        #         os.popen(f"git tag -d { SB }")
        #         # 推送新標籤到遠端
        #         os.popen(f"git push gitlab :refs/tags/{ SB }")
        #         ###################################################
        #         ###################################################
        #     #######################################################
        #     print("# ",os.popen(f"git add . ").read())
        #     print("# ",os.popen(f"git commit -m \"{ SB }\" ").read())
        #     print("# ",os.popen(f"git tag { SB } ").read())
        #     #########################################################
        #     print("# ",os.popen(f"git push -u gitlab main").read())
        #     print("# ",os.popen(f"git push --tags").read())


        if  SB in pip_tag(moon,SA):
            # 刪除本地標籤
            os.popen(f"git tag -d { SB }  {NU}")
            # 推送新標籤到遠端
            os.popen(f"git push gitlab :refs/tags/{ SB }  {NU}")
            ###################################################
            ###################################################
            import time
            time.sleep(1)
            print("del tag:",SB,SB in pip_tag(moon,SA))    
        #######################################################
        print("# ",os.popen(f"git add .  {NU}").read())
        print("# ",os.popen(f"git commit -m \"{ SB }\"  {NU}").read())
        print("# ",os.popen(f"git tag { SB }  {NU}").read())
        print(f"# git tag { SB }  {NU}")
        #########################################################
        print("# ",os.popen(f"git push -u gitlab main  {NU}").read())
        # print("# ",os.popen(f"git push --tags").read())
        print("# ",os.popen(f"git push --tags").read())
        ############
        ###########
        NU = "2> nul" if os.name == "nt" else "2> >/dev/null"
        HR=[ i.lstrip("Home-page:").strip() for i in os.popen(f"pip show {SA} {NU}").readlines()if str(i).startswith("Home-page:")]
        if len(HR)!=0:
            # import os
            # pwd  = os.path.basename(os.path.dirname(os.getcwd()))
            # print("@@!!",moon,pwd,HR[0])
            if moon==HR[0]:
               ## [reload安裝]
               NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
               os.system(f"pip uninstall {SA} -y {NU}")
               os.system(f"pip -install {SA}=={SB} {NU}")
               print("# [reload] :")
               print("@ pip -UN && pip -IN 更新完成 @")
        ############
        ###########
        os._exit(0)
    else:
        if (not moon)  or (not pypi):
            print("@ [缺少環境] api 或 moon @")
            #os._exit(0)
        



#####
##################################################################
if len(sys.argv)>=2 and moon and pypi and  "uninstall"  not  in sys.argv and  "del"  not  in sys.argv  and  "setup.py" not  in sys.argv  and r"-install" in sys.argv:
# if len(sys.argv)>=2 and moon and pypi and  "uninstall"  not  in sys.argv and  "del"  not  in sys.argv  and  "setup.py" not  in sys.argv :
    print("@ [使用] user.api 認證 @")
    NAA=sys.argv.index('-install')
    sys.argv.pop(NAA) ## [抽出][-u] pop即刪除
    sys.argv.insert(NAA,"install") ## [插入]

    # print(f"@ {sys.argv} @",os.environ["username"])
    args = sys.argv[1:]
    # if args is None:
    #     args = sys.argv[1:]
    if  "install" in sys.argv:
        NN = args.index("install")+1
        # KEY= os.environ["KEY"]
        if  args[NN].find(r"==")!=-1:
            SA,SB=args[NN].split(r"==")
            # print(f"@1 {SA} {SB}")
            args[NN]=f"git+https://{pypi}@gitlab.com/{moon}/{SA}@{SB}"
            # print(f"@1 {args} {pypi}")
        else:
            SA=args[NN]
            # print(f"@2 {SA}")
            args[NN]=f"git+https://{pypi}@gitlab.com/{moon}/{SA}"
            # print(f"@2 {args} {pypi}")
        ################################################################
        
        # print("@!! ",not pip_api( moon ,SA)  ) 
        if not pip_api( moon ,SA):
            import re
            # 定義正規表達式模式
            pattern = re.compile(r'^git\+https://[^/^@]+@gitlab\.com/[^/^@]+/[^/^@]+[@]?[^/^@]?$')
            args = sys.argv[1:]              ## 條件需要::不要移動 
            if  not pattern.match( args[NN] ):
                print(f"@ [{moon}]中 ---{SA}專案---不存在 @")
                os._exit(0)
        else:
            # print("@ SB ",  'SB' in globals() )
            if 'SB' in globals():
                # print("存在名为 SB 的变量")
                if  SB not in pip_tag( moon ,SA):
                    print(f"@ 目前沒有 {SB} 版本 @")
                    os._exit(0)
        ##############################
        # print(f"@ 專案 {SA} 存在 @")
        sys.argv=[sys.argv[0]]
        sys.argv.extend( args )
        # print("@ argv @",sys.argv)
        ##############################
 



