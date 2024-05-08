import os
from ultralytics import YOLO
import paramiko

class ModelNotFound(Exception):
     def __init__(self, error= "Cannot Load Model"):
          self.error = error
          super().___init__(self.error)

class EurBaseSDK():
    
    def getModel(self, filepath) ->str:
        extension = filepath.split(".")
        if extension[1] != "pt":
            print("Not supported file path")
            return ""
        
        if os.path.exists(filepath):
                print("Model file exist and ready to load")
                return filepath        
        else: 
            print("Model file is not available in the given path")
            return ""
        
    def loadModel(self, modelPath) -> YOLO:
        modelFile = self.getModel(modelPath)
        if modelFile != "":
            model = YOLO(modelPath)
            return model 
        else:
            raise ModelNotFound()

class ModelYolo(EurBaseSDK):
     
     def vaidateModel(self, pathArg):
        # try to loadModel for yolo
        try: 
            model = self.loadModel(pathArg)
            metrics = model.val(data='coco8.yaml')
            print("The Validated Metrics", metrics)
        except ModelNotFound as err:
             print("Error :", err)
    
     def predictModel(self, pathArg, dataSet):
        # try to loadModel for yolo
          data = []
          data.append(dataSet)
          try:
            model = self.loadModel(pathArg)
            results = model(data, save=True)
            for result in results:
                result.save(filename="./result.jpg")
                print("resuts saved in resuts.jpg")
          except ModelNotFound as err:
              print("Error :", err)

     def connect_ssh_client(self ,hostname , username, password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        return ssh 

     def uploadModel(self, local_path, remote_path, hostname, username, password):
        # Establish SSH connection
        ssh_client = self.connect_ssh_client(hostname, username, password)

        # SCP a file from local to remote
        sftp = ssh_client.open_sftp()
        sftp.put(local_path, remote_path)
        print("Model upload successful")
        sftp.close()
        # Close SSH connection
        ssh_client.close()

     def execute_script(self, hostname, username, password , script_path , modelFile):
        ssh_client = self.connect_ssh_client(hostname, username, password)
        
        stdin, stdout, stderr = ssh_client.exec_command('python3 -m venv mlsdk-venv && source ./mlsdk-venv/bin/activate && pip install eurmlsdk --upgrade && python3 {} {}'.format(script_path , modelFile))
        #python3 {}'.format(script_path)
        op = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        if op:
                print(op)
        if err:
                print("Error:")
                print(err)
        
        ssh_client.close()
        
     def deployModel(self, local_path, remote_path, hostname, username, password , script_path , modelFile):
        self.uploadModel(local_path, remote_path, hostname,username,password)
        self.execute_script(hostname, username, password , script_path , modelFile)