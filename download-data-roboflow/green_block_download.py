!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="Obqe7hCGLLSt4bfyaMVR")
project = rf.workspace("bittle").project("object-detection-bcc7j")
dataset = project.version(1).download("yolov5")



