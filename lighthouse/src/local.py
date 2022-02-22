from asyncio import subprocess
import os
import shutil
from socket import timeout
import stat
import time
from git import Repo
import mysql.connector
import js2py
from numpy import sign
from temp import *
import subprocess
import json
import psutil
import signal

local_repo_directory_fork = os.path.join("C:\\Users\\pedri\\Documents\\tcc", 'fork')
local_repo_directory = os.path.join("C:\\Users\\pedri\\Documents\\tcc", 'projetos')
local_repo_directory_vue = os.path.join("C:\\Users\\pedri\\Documents\\tcc", 'vue')
destination = 'main'
repoOrigin = "git@github.com:pedro-werik/projeto.git"

repoFork = []
#repoFork = []



#BANCO DE DADOS
def connect_with_db():
    print("--------- OPEN CONNECTION ---------")
    config = {
    'user': 'pedro_werik',
    'password': 'tcc2022puc',
    'host': 'tccbase.cuotubehzepx.us-east-1.rds.amazonaws.com',
    'database': 'tccbase',
    'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    return cnx

def select_db(cnx):
    print("PEGANDO REPOSITORIOS")
    cursor = cnx.cursor()
    query = ("SELECT * FROM REPOSITORIO WHERE TIPOREPOSITORIO = 'VUE'")
    cursor.execute(query)
    result = cursor.fetchall()
    
    for x in result:
        repoFork.append({'ssh': x[1], 'id': x[0], 'tipo': x[3], 'nome': x[2]})
    
    cursor.close()
    cnx.close()

def insert_into_med(cnx, value, id):
    print("--------- INSERT DATA ---------")

    cursor = cnx.cursor()
    #query = """INSERT INTO MEDICAO (IDREPOSITORIO, SPEEDINDEX1, SPEEDINDEX2, SPEEDINDEX3) VALUES (%s, %s, %s, %s)"""
    query = """INSERT INTO TESTESCRIPT (firstname, lastname, email) VALUES (%s, %s, %s)"""
    cursor.execute(query, (value[0], value[0], value[0]))
    cnx.commit()
    print(cursor.rowcount, "record inserted.")
    
    cursor.close()
    cnx.close()

def delete_fork_directory():
    print("Deletando diretorio Fork")
    for root, dirs, files in os.walk(local_repo_directory_fork):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    shutil.rmtree(local_repo_directory_fork)

def copy_files_fork_to_projeto(type):
    print("------- COPY FILES -------")
    for file in os.listdir(local_repo_directory_fork):
        if file != '.git':
            if(type == "REACT"):
                shutil.move(local_repo_directory_fork + '/' + file, local_repo_directory)
            else:
                shutil.move(local_repo_directory_fork + '/' + file, local_repo_directory_vue)

def remove_files_projeto(type):
    if(type == "REACT"):
        local = local_repo_directory
    else:
        local = local_repo_directory_vue
    if os.path.isdir(local):
        print("Removendo arquivos anteriores")
        chdirectory(local)
        for file in os.listdir(local):
            path = os.path.join(local, file)
            if file != '.git':
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)
    else:
        print('nao existe a pasta')

def remove_yarn():
    if os.path.isdir(local_repo_directory):
        print("Removendo yarn")
        chdirectory(local_repo_directory)
        for file in os.listdir(local_repo_directory):
            path = os.path.join(local_repo_directory, file)
            if file == 'yarn.lock':
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)

def clone_repo():
    if os.path.exists(local_repo_directory):
        print("Dir Existe")
     #   print("Diretorio existe, Pulling mudanças da main branch")
      #  repo = Repo(local_repo_directory)
       # origin = repo.remotes.origin
       # origin.pull(destination)
    else:
        print("Diretorio não existe, Clonando repo")    
        Repo.clone_from(repoOrigin, 
            local_repo_directory, branch=destination) #ssh link git, local destino, branch

def clone_repo_fork(repo, dest):
    if os.path.exists(local_repo_directory_fork):
        print("DirFork Existe")
        delete_fork_directory()
        print("Diretorio não existe, Clonando repo fork") 
        Repo.clone_from(repo, 
            local_repo_directory_fork, branch=dest)
    else:
        print("Diretorio não existe, Clonando repo fork")    
        Repo.clone_from(repo, 
            local_repo_directory_fork, branch=dest) 

def chdirectory(path):
    os.chdir(path)

def chdirectory_lighthouse():
    os.chdir("C:\\Users\\pedri\\Documents\\tcc\\tcc-script\\lighthouse\\src")

def update_file():
    chdirectory(local_repo_directory)
    opened_file = open("README.md", 'a')
    opened_file.write("{0} added at {1}".format("I am a new String", str(time.time())))

def add_commit_changes(repo):
    print("Comitando mudancas")
    repo.git.add('--all')
    repo.git.commit("-m", "Teste Repositorios")

def push_changes(repo):
    print("push changes")
    repo.git.push('origin', "master")

def call_lighthouse():
    print("------------ RUN LIGHTHOUSE ------------")
    subprocess.run(["node", "lh.js"])

    time.sleep(2)

    res = read_report_lighthouse()
    return res

def read_report_lighthouse():
    print("------------ GET SPEED-INDEX ------------")
    file = open('lhreport.json', encoding="utf8")
    data = json.load(file)
    
    if data["audits"]["speed-index"]["score"] == None:
        file.close()
        return None
    else:
        speed_index_data = data["audits"]["speed-index"]
        speed_index_seconds = speed_index_data["displayValue"]
        speed_index_seconds = speed_index_seconds.replace("Â", "")
        file.close()
        return speed_index_seconds
    
def npm_command():
    os.chdir(local_repo_directory_fork)
    subprocess.check_call('npm install', shell=True)
    file = open('package.json', encoding="utf8")
    data = json.load(file)
    next_command = data['scripts']
    if 'serve' in next_command:
        next_command = 'npm run serve'
    elif 'start' in next_command:
        next_command = 'npm start'
    else:
        next_command = 'npm run dev'
    
    file.close()
    os.system('start cmd /c ' + next_command)
    

        
def main():
    cnx = connect_with_db()
    select_db(cnx)
    print(repoFork)

    for r in repoFork:
        print('######## CLONANDO: ' + r['nome'] + ' ########')
        try:
            #clonar repositorio
            clone_repo_fork(r['ssh'], 'master')
            print("----------OK---------")
        except:
            time.sleep(5)
            #clonar repositorio
            clone_repo_fork(r['ssh'], 'main')
            print("----------OK---------")

        npm_command()

        time.sleep(15)

        chdirectory_lighthouse()
        print(os.getcwd())
        
        time.sleep(5)

        speed_index = []
        for i in range(1):
            res = call_lighthouse()
            speed_index.append(res)
        
        print("----------OK---------")

        os.system('taskkill /IM node.exe /F')
        
    
        cnx = connect_with_db()
        insert_into_med(cnx, speed_index, r['id'])
        print("----- OK -----")

        
    '''
        #deleta diretorio fork
        delete_fork_directory()
        print("----------OK---------")
    '''
main()