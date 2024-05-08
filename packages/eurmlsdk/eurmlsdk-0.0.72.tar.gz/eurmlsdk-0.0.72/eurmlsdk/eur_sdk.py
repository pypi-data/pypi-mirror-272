import os
from ultralytics import YOLO
from paramiko.ssh_exception import AuthenticationException
import paramiko

class ModelNotFound(Exception):
     def __init__(self, error= "Cannot Load Model"):
          self.error = error
          super().___init__(self.error)

class EurBaseSDK():  
    def getModel(self, filepath) ->str:
        extension = filepath.split(".")
        if extension[1] != "pt" or extension[1] != "tflite":
            print("Not supported file path")
            return ""
        
        if os.path.exists(filepath):
            print("Model file exist and ready to load")
            return filepath        
        else: 
            print("Model file is not available in the given path")
            return ""
    
    def connect_ssh_client(self, hostname, username, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, username=username, password=password)
            return ssh
        except AuthenticationException as err:
            print("Authentication to %s SSH failed - Invalid username or password" % hostname)
            # print("Authentication Error: %s" % err)
            exit(1)
        except TimeoutError as err:
            print("Connection Timeout Error: ", err)
            exit(1)
        except Exception as err:
            print("Error: %s" % err)
            exit(1)

    def uploadModel(self, ssh_client, local_path, remote_path):
        # Establish SSH connection
        # ssh_client = self.connect_ssh_client(hostname, username, password)
        # SCP a file from local to remote
        try:
            sftp = ssh_client.open_sftp()
            sftp.put(local_path, remote_path)
            print("Model upload successful")
            sftp.close()
        except Exception as err:
            print("Error uploading the model file: ", err)

        # Close SSH connection
        # ssh_client.close()

    def execute_script(self, ssh_client, script_path, modelFile):
        # ssh_client = self.connect_ssh_client(hostname, username, password)
        stdin, stdout, stderr = ssh_client.exec_command('python3 -m venv mlsdk-venv && source ./mlsdk-venv/bin/activate && pip install eurmlsdk --upgrade && python3 {} {}'.format(script_path , modelFile))
        #python3 {}'.format(script_path)
        op = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        if op:
            print(op)
        if err:
            print("Error:")
            print(err)
        # ssh_client.close()
        
    def deployModel(self, local_path, remote_path, hostname, username, password, script_path, modelFile):
        # Establish SSH connection
        ssh_client = self.connect_ssh_client(hostname, username, password)
        self.uploadModel(ssh_client, local_path, remote_path)
        self.execute_script(ssh_client, script_path , modelFile)
        # Close SSH connection
        ssh_client.close()

class ModelYolo(EurBaseSDK):
    def loadModel(self, modelPath) -> YOLO:
        modelFile = self.getModel(modelPath)
        if modelFile != "":
            model = YOLO(modelPath)
            return model 
        else:
            raise ModelNotFound()

    def validateModel(self, pathArg):
        try: 
            model = self.loadModel(pathArg)
            metrics = model.val(data='coco8.yaml')
            print("The Validated Metrics", metrics)
        except ModelNotFound as err:
            print("Error :", err)
    
    def predictModel(self, pathArg, dataSet):
        data = []
        data.append(dataSet)
        try:
            model = self.loadModel(pathArg)
            results = model(data, save=True)
            for result in results:
                result.save(filename="./result.jpg")
                print("resuts saved in result.jpg")
        except ModelNotFound as err:
            print("Error :", err)