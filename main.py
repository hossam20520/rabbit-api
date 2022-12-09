from template import TEMPLATE 
from template_crud import TEMPLATE as template_crud
from template_models import  TEMPLATE as template_model
from template_schemas import TEMPLATE as template_schemas
from auth_role_temp.template_route import TEMPLATE as auth_role_route_temp
from auth_role_temp.template_model_user import TEMPLATE as auth_role_model_user_template
from auth_role_temp.template_models_permission import TEMPLATE as auth_role_model_permission
from auth_role_temp.template_models_permission_roles import TEMPLATE as auth_role_model_permission_role
import shutil
from template_main import TEMPLATE as template_main
from template_database import TEMPLATE as template_database
from template_global import TEMPLATE as gloabl_template
from auth_role_temp.template_main import TEMPLATE as template_auth_main
#from Utils.DirCreator import DirCreator
import os
from jinja2 import Template
  
  
#d = DirCreator()
#d.CreateDir("app/Http/Controllers")
# Directory
#directory = "app/Http/Controllers"
  
# Parent Directory path
parent_dir = os.getcwd() + "/build"
  
# Path
#path = os.path.join(parent


def getTemp(template, element):
        t = Template(template)
        return t.render( element=element)


filepath = os.getcwd()
def MakeFile(file_name,dir, element, temp):
    temp_path = parent_dir +"/" + file_name
    #print(temp_path)
    with open(temp_path, 'w') as f:
        f.write( getTemp(temp , element ))
    print('Execution completed.')


#users = {"Name":"User" , "names": "users" , "name":"user"}
#MakeFile("routes.py",parent_dir , users)




# permissions  = {"Name":"User" , "names": "users" , "name":"user"}

# os.makedirs(os.path.join(parent_dir, permissions['names']) , exist_ok=True)

# MakeFile("routes.py",parent_dir+permissions['names'] , permissions, auth_role_route_temp)
# MakeFile("crud.py",parent_dir , permissions, template_crud)
# MakeFile("models.py",parent_dir , permissions, template_model)
# MakeFile("schemas.py",parent_dir , permissions, template_schemas)

class ProjectMaker:
    parent_dir = os.getcwd()
    build_dir =  os.getcwd() + "/build/"
    aliseNames = []
    projectName = "project"
    def __init__(self , projectName = None ):
        if  projectName:
            self.projectName = projectName
            os.makedirs(os.path.join(self.build_dir, projectName) , exist_ok=True)
            self.build_dir = self.build_dir + projectName +"/"
    def AliseName(self , name):
         self.Alise  = {"Name":name.capitalize() , "names": name+"s" , "name":name}
         self.aliseNames.append(self.Alise['names'] )

    def TemplateFile(self, template):
        self.template = template
    def makeDir(self):
        os.makedirs(os.path.join(self.build_dir, self.Alise['names']) , exist_ok=True)
    
    def MakeFile(self , file_name  ):
        temp_path = self.build_dir +"/" +self.Alise['names']+"/"+ file_name
        self.MakeInitFIle(self.Alise['names'])
        with open(temp_path, 'w') as f:
            f.write( getTemp(self.template , self.Alise ))
        print(file_name+ 'Created.')

    def MakeInitFIle(self , aliseName = ""):
        temp_path = self.build_dir +"/" +aliseName+"/"+ "__init__.py"
        with open(temp_path, 'w') as file:
             pass 

    def create_routes(self):
        self.MakeFile("routes.py")
    def create_crud(self):
        self.MakeFile("crud.py")

    def create_models(self):
        self.MakeFile("models.py")
    
    def create_schemas(self):
        self.MakeFile("schemas.py")
    def create_databaseFile(self):
        temp_path = self.build_dir +"/"+ "sql_app.db"
        with open(temp_path, 'w') as f:
            pass
        print('Database created.')

    def create_database(self ):
        temp_path = self.build_dir +"/"+ "database.py"
        with open(temp_path, 'w') as f:
            f.write( getTemp(template_database , "" ))
        print('database.py created.')
    
    def create_global_schemas(self):
        temp_path = self.build_dir +"/"+ "global_schemas.py"
        with open(temp_path, 'w') as f:
            f.write( getTemp(gloabl_template , "" ))
        print('global_schemas.py created.')


    def create_project(self , auth = False):
        temp_path = self.build_dir +"/"+ "main.py"
        self.create_global_schemas()
        self.create_databaseFile()
        self.create_database()
        self.MakeInitFIle()
        if auth:
            temp = template_auth_main
        else:
            temp = template_main
        with open(temp_path, 'w') as f:
            f.write( getTemp(temp , self.aliseNames ))
        print('Main.py created.')
        # self.MakeFile("main.py")

    def makeSimpleProject(self , names):
        for i in names:
            self.AliseName(i)
            self.makeDir()
            self.TemplateFile(TEMPLATE)
            self.create_routes()
            self.TemplateFile(template_crud)
            self.create_crud()
            self.TemplateFile(template_model)
            self.create_models()
            self.TemplateFile(template_schemas)
            self.create_schemas()

    def MakeAuthRoleProject(self , names):
    
                source_dir =  os.getcwd() + "/auth_role_temp/temps"
                destination_dir = os.getcwd() + "/build/"+ self.projectName+"/"
                shutil.copytree(source_dir, destination_dir , dirs_exist_ok=True)
                for i in names:
                    self.AliseName(i)
                    self.makeDir()
                    self.TemplateFile(auth_role_route_temp)
                    self.create_routes()
                    self.TemplateFile(template_crud)
                    self.create_crud()
                    self.TemplateFile(template_model)
                    self.create_models()
                    self.TemplateFile(template_schemas)
                    self.create_schemas()


print("""  
 ######                                     #    ######  ### 
 #     #   ##   #####  #####  # #####      # #   #     #  #  
 #     #  #  #  #    # #    # #   #       #   #  #     #  #  
 ######  #    # #####  #####  #   #      #     # ######   #  
 #   #   ###### #    # #    # #   #      ####### #        #  
 #    #  #    # #    # #    # #   #      #     # #        #  
 #     # #    # #####  #####  #   #      #     # #       ### 
                                                             """)


router  = ProjectMaker("labianoo")
router.MakeAuthRoleProject([ "product"])
router.create_project(True)

# router.makeSimpleProject([ "product"])
# router.create_project()



