
import requests
import os
from dotenv import load_dotenv
import argparse
import sys

load_dotenv()

cwd = os.getcwd()   
scripPath = os.path.dirname(os.path.abspath(__file__))
token = os.getenv('TOKEN')

parser = argparse.ArgumentParser()
parser.add_argument("--name" , "-n" , type=str,dest="name" ,help='for file and repo name  "required"' )
parser.add_argument("--private" , "-p" ,dest="private",action="store_true" , help="to make repo private")
parser.add_argument("--flutter" , "-f" ,dest="flutter",action="store_true",help=" to create flutter project under same repo name")
parser.add_argument("--angular" , "-a" ,dest="angular",action="store_true",help="to create angular project under same repo name")
parser.add_argument("--vscode" , "-vc" ,dest="vscode",action="store_true",help="to lunch project in vscode")
parser.add_argument("--youtube" , "-yt" ,dest="youtube",action="store_true",help="to lunch youtube on chrome")

args = parser.parse_args()
# hhelp = args.hhelp

if not args.name:
    print("--name , -n  for file and repo name 'required' ")
    print("--private , -p  to make repo private" )
    print("--flutter , -f to create flutter project under same repo name")
    print("--angular , -a to create angular project under same repo name")
    print("--vscode , -vc to lunch project in vscode")
    print("--youtube , -yt to lunch project in vscode")
    sys.exit()
if args.name:
    repo_name = args.name
    private = args.private
    flutter = args.flutter
    angular = args.angular
    vscode = args.vscode
    youtube = args.youtube
    if private:
        payload = '{"name":"' + repo_name  +'", "private":true}'
    else:
        payload = '{"name":"' + repo_name  +'", "private":false}'


    done = False
    while not done:
        if token:
            headers = {
                "Authorization" : f"token {token}" ,
                "Accept": "application/vnd.github.v3+json"
            }

            try:
                r = requests.post("https://api.github.com/user/repos" , data=payload,headers=headers)
                if r.status_code == 201:
                    s = r.json()
                    repo_path = s['html_url']
                    done = True
                else:
                    print(r.content)
                    sys.exit()
            except Exception as e:
                print(e)
        else:
            print("Token is requred please enter token")
            print("to genereate one go to github -> settings -> Developer settings -> Personal access tokens")
            print("or follow the link https://github.com/settings/tokens")
            print("repo scope needed to create private repo")
            token = input("github token: ")
            with open (f"{scripPath}/.env" , "w") as f:
                f.write(f'TOKEN="{token}"')
    try:
        os.chdir(cwd)
        os.system("mkdir "  +repo_name)
        os.chdir(cwd + "/" + repo_name)
        os.system("git init")
        createGit  = f"git remote add origin {repo_path}.git"
        os.system(createGit)
        os.system("echo '#" + repo_name+"' >> README.md")
        if flutter:

            os.system(f"flutter create {repo_name}")
        elif angular:
            print("ANGLUR")
            os.system(f"ng new {repo_name}")
        gitComand = 'git add . && git commit -m "initial commit" && git push origin master'
        os.system(gitComand)
    except FileNotFoundError as err:
        print(err)    

    if vscode:
        os.system("code .")
    if youtube:
        os.system("start chrome www.youtube.com")
else:
    print("--name , -n  for file and repo name 'required'")
    print("--private , -p  to make repo private" )
    print("--flutter , -f to create flutter project under same repo name")
    print("--angular , -a to create angular project under same repo name")
    print("--vscode , -vc to lunch project in vscode")
    print("--youtube , -yt to lunch project in vscode")
    print("--help , -h for help")