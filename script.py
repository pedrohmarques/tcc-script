import os
import shutil
import stat
import time
from git import Repo
import mysql.connector

local_repo_directory_fork = os.path.join(os.getcwd(), 'fork')
local_repo_directory = os.path.join(os.getcwd(), 'projeto')
destination = 'main'
repoOrigin = "git@github.com:pedro-werik/projeto.git"
repoFork = ["git@github.com:mdn/todo-react.git", "git@github.com:mdn/todo-react.git"]

#BANCO DE DADOS
def connect_with_db():
    print("#ABRINDO CONEXAO")
    config = {
    'user': 'pedro_werik',
    'password': 'tcc2022puc',
    'host': '',
    'database': 'tccbase',
    'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    return cnx

def select_db(cnx):
    print("PEGANDO REPOSITORIOS")
    cursor = cnx.cursor()
    query = ("SELECT NOMEREPOSITORIO FROM REPOSITORIO")
    cursor.execute(query)
    result = cursor.fetchall()
    for x in result:
        print(x)

    cursor.close()
    cnx.close()

def insert_into_med(cnx):
    print("INSERINDO DADOS")
    cursor = cnx.cursor()
    query = ("INSERT INTO MEDICAO (speedindex1) VALUES (%s)")
    values = ("3")
    cursor.execute(query, values)
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

def copy_files_fork_to_projeto():
    for file in os.listdir(local_repo_directory_fork):
        if file != '.git':
            shutil.move(local_repo_directory_fork + '/' + file, local_repo_directory)

def remove_files_projeto():
    if os.path.isdir(local_repo_directory):
        print("Removendo arquivos anteriores")
        chdirectory(local_repo_directory)
        for file in os.listdir(local_repo_directory):
            path = os.path.join(local_repo_directory, file)
            if file != '.git':
                try:
                    shutil.rmtree(path)
                except OSError:
                    os.remove(path)
    else:
        print('nao existe a pasta')   

def clone_repo():
    #if os.path.exists(local_repo_directory):
     #   print("Diretorio existe, Pulling mudanças da main branch")
      #  repo = Repo(local_repo_directory)
       # origin = repo.remotes.origin
       # origin.pull(destination)
    #else:
        print("Diretorio não existe, Clonando repo")    
        Repo.clone_from(repoOrigin, 
            local_repo_directory, branch=destination) #ssh link git, local destino, branch

def clone_repo_fork(repo, dest):
    print("Diretorio não existe, Clonando repo")    
    Repo.clone_from(repo, 
        local_repo_directory_fork, branch=dest) 

def chdirectory(path):
    os.chdir(path)

def update_file():
    chdirectory(local_repo_directory)
    opened_file = open("README.md", 'a')
    opened_file.write("{0} added at {1}".format("I am a new String", str(time.time())))

def add_commit_changes(repo):
    print("Comitando mudancas")
    repo.git.add('--all')
    repo.git.commit("-m", "Teste Script 2")

def push_changes(repo):
    print("push changes")
    repo.git.push("--set-upstream", 'origin', destination)

def main():
    connect_with_db()
    """
    #clonar repositorio
    clone_repo()
    print("----------OK---------")

    #Remove arquivos
    remove_files_projeto()
    print("----------OK---------")
    

    for r in repoFork:
        dest = 'master' #temporario

        #clonar repositorio
        clone_repo_fork(r, dest)
        print("----------OK---------")

        #move os arquivos para o projeto
        copy_files_fork_to_projeto()
        print("----------OK---------")

        #deleta diretorio fork
        delete_fork_directory()
        print("----------OK---------")

        #Remove arquivos
        remove_files_projeto()
        print("----------OK---------")
        
    #repo = Repo(local_repo_directory)
    
    #add and commit changes
    #add_commit_changes(repo)
    #print("----------OK---------")

    #push changes
    #push_changes(repo)
    #print("----------OK---------")
    """
main()