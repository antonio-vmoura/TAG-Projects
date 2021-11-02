"""
name: Antonio Vinicius de Moura Rodrigues

sources:
- https://www.vitoshacademy.com/python-algorithms-stable-matching-problem/
- https://towardsdatascience.com/gale-shapley-algorithm-simply-explained-caa344e643c2

"""

import os
import re

class matchProjects():

    def assemble_data(file_content):
        student_list = []; project_list = []

        for x in range(len(file_content)):
            
            if file_content[x] != "" and "//" not in file_content[x]: #checking if the line is not empty or if it is not a comment
                if "A" in file_content[x]: #checking if the line belongs to a student
                    m = re.search("\((\w+)\):\((\w+), (\w+), (\w+)\)(|\ )\((\w+)\)", file_content[x]) #applying the regex to separate information into groups
                    student_id = m.group(1); prefs_project = [m.group(2), m.group(3), m.group(4)]; note = m.group(6)
                    
                    student = {"student_id": student_id, "prefs_project": prefs_project, "note": note, "have_a_project": False, "belongs_to": "", "tried_to":[]} #montando o dicionario com as informacoes dos alunos separados
                    student_list.append(student)                
                else:
                    m = re.search("(\w+), (\w), (\w)", file_content[x]) #applying the regex to separate information into groups
                    project_id = m.group(1); vacancies_num = m.group(2); requirements = m.group(3)

                    project = {"project_id": project_id, "vacancies_num": vacancies_num, "requirements": requirements, "belongs_to": []} #assembling the dictionary with information from the separate projects
                    project_list.append(project)
            
        # print(f"Lista de alunos: {student_list}\nLista de projetos: {project_list}\n")
            
        return student_list, project_list

    def gale_sharpley(students, projects):
        print("\nSubstitutions:\n")

        while (True):
            flag = 0
            for student in students:
                
                if (student["have_a_project"] == True or len(student["tried_to"]) == 3): #check if the student does not have any projects and if they have tried all their preference lists
                    flag += 1
                    if flag == len(students): #if the flag is the size of the size of students who do not repeat preferences
                        print("\nAlgorithm successfully completed!\n")
                        return students, projects

                for prefs in student["prefs_project"]: #for each project on the student's wish list
                    if student["belongs_to"] == "": #checking if the student does not belong to any project

                        if prefs not in student["tried_to"]: 
                            for x in range(student["prefs_project"].count(prefs)):
                                student["tried_to"].append(prefs)

                        for project in projects: #find the project desired by the student
                            if project["project_id"] == prefs: 
                                selected_project = project

                        if student["note"] >= selected_project["requirements"]: #check if the student has enough grade to participate in the project
                            if len(selected_project["belongs_to"]) == int(selected_project["vacancies_num"]): #check if all the project's vacancies have already been occupied
                                
                                students_in_project_list = selected_project["belongs_to"] #get the list of students who are participating in the project

                                replaced_student_id = None
                                for x in range(len(students_in_project_list)): #[{student_id: "", note: ""}]

                                    if student["note"] > students_in_project_list[x]["note"]: #check if the student's note is better than the students who are already participating
                                        replaced_student_id = students_in_project_list[x]["student_id"]; student_position = x
                                    
                                if replaced_student_id: #check if there is any student with the lowest grade
                                    new_student = student["student_id"]
                                    students_in_project_list[student_position] = {"student_id": new_student, "note": student["note"]} #replaces the student

                                    student["belongs_to"] = selected_project["project_id"]; student["have_a_project"] = True
                                    selected_project["belongs_to"] = students_in_project_list

                                    for student in students:
                                        if student["student_id"] == replaced_student_id:
                                            student["belongs_to"] = ""; student["have_a_project"] = False
                                            print(f"'{new_student}' replaced '{replaced_student_id}' In the project '{selected_project['project_id']}'")

                            else:
                                student["belongs_to"] = selected_project["project_id"]; student["have_a_project"] = True

                                aux_belongs_to = selected_project["belongs_to"]
                                aux_belongs_to.append({"student_id": student["student_id"], "note": student["note"]})

                                selected_project["belongs_to"] = aux_belongs_to

    def main():

        with open(f"{os.getcwd()}/data_input.txt") as file:
            file_content = [line.rstrip('\n') for line in file] #storing each line of the .txt in a list element

        student_list, project_list = matchProjects.assemble_data(file_content) #function responsible for assembling the data that will be read by the algorithm
        student_list, project_list = matchProjects.gale_sharpley(student_list, project_list)

        for project in project_list: #printing the projects and their respective students
            project_id = project["project_id"]; belongs_to = project["belongs_to"]
            bt_list = [bt["student_id"] for bt in belongs_to]

            print(f"{project_id} <---> {bt_list}")

if __name__ == "__main__":
    matchProjects.main()
