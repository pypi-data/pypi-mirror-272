from sys import argv,exit
from .base_class import ModelBase
from dotenv import load_dotenv
import os
import logging
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow info and warning logs
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Suppress TensorFlow warning logs
logging.getLogger('tensorflow.compiler.tf2tensorrt').setLevel(logging.ERROR)  # Suppress TensorFlow-TRT warning logs

def list_commands():
    print("Available commands in mlsdk package are:")
    print("  help | --h                : Lists all commands available in mlsdk package")
    print("  get <model name/path>     : Gives model path name by fetching or downloading from S3")
    print("  profile <model name/path> : Gives model profiling info by running the profiler on a simulator")
    print("  compare <model name/path> <model name/path> : Gives comparison chart of model profiling info by running the profiler on a simulator")
    print("  deploy <local path> <hostname> <username> <password> : Uploads the model file in the Raspberry pi")
    print("     <local path> : path to the model file")
    print("     <hostname>   : hostname to connect to Raspberry pi")
    print("     <username>   : username to connect to Raspberry pi")
    print("     <password>   : password to connect to Raspberry pi")

def main():
    load_dotenv("config.env")
    s3_bucket = os.getenv("MLSDK_S3_BUCKET_NAME")
    model_key = os.getenv("MLSDK_S3_MODEL_KEY")
    model_ouput_path = os.getenv("MLSDK_MODEL_OUTPUT_PATH")
    # print("Bucket: %s" % s3_bucket)
    # print("Model key: %s" % model_key)
    
    if len(argv) == 1:
        print("Model Zoo SDK")
        print("Package name: eurmlsdk")
        print("Version: 0.0.1")
        print("Run 'eurmlsdk help' or eurmlsdk --h to find the list of commands.")
        exit(1)

    command = argv[1]
    if command == "help" or command == "--h":
        list_commands()
        exit(1)
    elif command == "get":
        if len(argv) < 3:
            print("Give the model file name or file path")
            exit(1)
        filePath = argv[2]
        modelBase = ModelBase(s3_bucket, model_key, model_ouput_path)
        model_file_path = modelBase.getModel(filePath)
        print("Model File Path: %s" %model_file_path)
        
    elif command == "profile":
        if len(argv) < 3:
            print("Give the model file name or file path")
        else:
            modelFile = argv[2]
            modelBase = ModelBase(s3_bucket, model_key, model_ouput_path)
            profiling_results = modelBase.getProfileInfo(modelFile)  
            print(profiling_results)
        exit(1)
 #compare metrics       
    elif command == "compare":
        if len(argv) < 3:
            print("Give the model file name or file path")
        elif len(argv) < 4:
            print("Provide 2 models for comparing")
        else:
            unQuantizedModel = argv[2]
            quantizedModel = argv[3]
            modelBase = ModelBase(s3_bucket, model_key, model_ouput_path)
            modelBase.compareMetrics(unQuantizedModel , quantizedModel)  
        
    elif command == "validate":
            print(argv)
            if len(argv) <3:
                print("Give the model file name or file file path")
                exit(1)
        
    elif command == "predict":
            print(argv)
            if len(argv) <3:
                print("Give the model file name or file file path")
                exit(1)
            elif len(argv) <4:
                print("Please provide atlest one data set of images")
                                                                                                                                             
            modelBase.compareMetrics(unQuantizedModel , quantizedModel)
            exit(1)
    
    elif command == "deploy":
        if len(argv) < 6:
            print("Missing required arguments")
            print("Usage: eurmlsdk deploy <local path> <hostname> <username> <password>")
        else:
            localPath = argv[2]
            remotePath = "/home/embeduradmin/" + localPath.split("/")[-1]
            hostname = argv[3]
            username = argv[4]
            password = argv[5]
            modelBase = ModelBase(s3_bucket, model_key, model_ouput_path ,None ,None)
            script_path = "/home/embeduradmin/hello.py"
            modelBase.deployModel(localPath, remotePath, hostname, username, password ,script_path)
        exit(1)
        
    else:
        print("Unknown command. Please find the list of commands")
        list_commands()

if __name__ == "__main__":
    main()