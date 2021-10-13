#Nome: Antonio Vinicius de Moura Rodrigues
#Fontes: https://www.vitoshacademy.com/python-algorithms-stable-matching-problem/ , https://towardsdatascience.com/gale-shapley-algorithm-simply-explained-caa344e643c2

import os #Importando o biblioteca "os" para ler o arquivo .txt
import re #Importando a biblioteca "re" para utilizar o regex quando montar os dados

def assemble_data(file_content):
    student_list = []; project_list = []

    for x in range(len(file_content)):
        
        if file_content[x] != "" and "//" not in file_content[x]: #Verificando se a linha nao e vazia ou se nao e um comentario
            if "A" in file_content[x]: #Verificando se a linha pertence a um aluno
                m = re.search("\((\w+)\):\((\w+), (\w+), (\w+)\)(|\ )\((\w+)\)", file_content[x]) #Aplicando o regex para separar as informacoes em grupos
                student_id = m.group(1); prefs_project = [m.group(2), m.group(3), m.group(4)]; note = m.group(6)
                
                student = {"student_id": student_id, "prefs_project": prefs_project, "note": note, "have_a_project": False, "belongs_to": "", "tried_to":[]} #montando o dicionario com as informacoes dos alunos separados
                student_list.append(student)                
            else:
                m = re.search("(\w+), (\w), (\w)", file_content[x]) #Aplicando o regex para separar as informacoes em grupos
                project_id = m.group(1); vacancies_num = m.group(2); requirements = m.group(3)

                project = {"project_id": project_id, "vacancies_num": vacancies_num, "requirements": requirements, "belongs_to": []} #montando o dicionario com as informacoes dos projetos separados
                project_list.append(project)
        
    # print(f"Lista de alunos: {student_list}\n")
    # print(f"Lista de projetos: {project_list}\n")
        
    return student_list, project_list

def gale_sharpley(students, projects):
    print("Substituições:\n")

    while (True):
        flag = 0
        for student in students:
            
            if (student["have_a_project"] == True or len(student["tried_to"]) == 3): #Verifica se o aluno nao tem nenhum projeto e se ja tentou toda a suas listas de preferencias
                flag += 1
                if flag == len(students): #Se a flag for do tamanho do tamanho de estudantes que nao repetem preferencias
                    print("\nAlgoritmo concluído com sucesso!\n")
                    return students, projects

            for prefs in student["prefs_project"]: #Para cada projeto na list de preferencias do aluno
                if student["belongs_to"] == "": #Verificando se o aluno nao pertence a nenhum projeto

                    if prefs not in student["tried_to"]: 
                        for x in range(student["prefs_project"].count(prefs)):
                            student["tried_to"].append(prefs)

                    for project in projects: #Encontra o proejeto desejado pelo aluno
                        if project["project_id"] == prefs: 
                            selected_project = project

                    if student["note"] >= selected_project["requirements"]: #Verifica se o aluno tem nota o suficiente para participar do projeto 
                        if len(selected_project["belongs_to"]) == int(selected_project["vacancies_num"]): #Verifica se todas as vagas do projeto ja foram ocupadas
                            
                            students_in_project_list = selected_project["belongs_to"] #Pega a lista de alunos que estao participando do projeto

                            replaced_student_id = None
                            for x in range(len(students_in_project_list)): #[{student_id: "", note: ""}]

                                if student["note"] > students_in_project_list[x]["note"]: #Verifica se a nota do aluno e melhor do que os alunos que ja estao participando
                                    replaced_student_id = students_in_project_list[x]["student_id"]; student_position = x
                                  
                            if replaced_student_id: #Verifica se existe algum aluno com a nota menor
                                new_student = student["student_id"]
                                students_in_project_list[student_position] = {"student_id": new_student, "note": student["note"]} #Substitui o aluno

                                student["belongs_to"] = selected_project["project_id"]; student["have_a_project"] = True
                                selected_project["belongs_to"] = students_in_project_list

                                for student in students:
                                    if student["student_id"] == replaced_student_id:
                                        student["belongs_to"] = ""; student["have_a_project"] = False
                                        print(f"'{new_student}' substituiu '{replaced_student_id}' no projeto '{selected_project['project_id']}'")

                        else:
                            student["belongs_to"] = selected_project["project_id"]; student["have_a_project"] = True

                            aux_belongs_to = selected_project["belongs_to"]
                            aux_belongs_to.append({"student_id": student["student_id"], "note": student["note"]})

                            selected_project["belongs_to"] = aux_belongs_to

def main():

    with open(f"{os.getcwd()}/entradaProj2TAG.txt") as file:
        file_content = [line.rstrip('\n') for line in file] #Guardando cada linha do .txt em um elemento da lista

    student_list, project_list = assemble_data(file_content) #Funcao responsavel por montar os dados que serao lidos pelo algoritmo
    student_list, project_list = gale_sharpley(student_list, project_list)

    for project in project_list: #Printando os projetos e seus respectivos alunos
        project_id = project["project_id"]; belongs_to = project["belongs_to"]
        bt_list = [bt["student_id"] for bt in belongs_to]

        print(f"{project_id} <---> {bt_list}")

if __name__ == "__main__":
    main()
