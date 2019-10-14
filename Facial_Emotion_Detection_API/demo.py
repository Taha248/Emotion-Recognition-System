# /usr/bin/python3
import cv2
import numpy as np
import sys
import tensorflow as tf
import copy

from model import predict, image_to_tensor, deepnn

CASC_PATH = './data/haarcascade_files/haarcascade_frontalface_default.xml'
cascade_classifier = cv2.CascadeClassifier(CASC_PATH)
EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
SAMPLE_IMAGE="images/sample1.jpg"


def format_image(image):
  if len(image.shape) > 2 and image.shape[2] == 3:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  faces = cascade_classifier.detectMultiScale(
    image,
    scaleFactor = 1.3,
    minNeighbors = 5
  )
  # None is no face found in image
  if not len(faces) > 0:
    return None, None
  max_are_face = faces[0]
  for face in faces:
    if face[2] * face[3] > max_are_face[2] * max_are_face[3]:
      max_are_face = face
  # face to image
  face_coor =  max_are_face
  image = image[face_coor[1]:(face_coor[1] + face_coor[2]), face_coor[0]:(face_coor[0] + face_coor[3])]
  # Resize image to network size
  try:
    image = cv2.resize(image, (48, 48), interpolation=cv2.INTER_CUBIC)
  except Exception:
    print("[+} Problem during resize")
    return None, None
  return  image, face_coor

def face_dect(image):
  """
  Detecting faces in image
  :param image: 
  :return:  the coordinate of max face
  """
  if len(image.shape) > 2 and image.shape[2] == 3:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  faces = cascade_classifier.detectMultiScale(
    image,
    scaleFactor = 1.3,
    minNeighbors = 5
  )
  if not len(faces) > 0:
    return None
  max_face = faces[0]
  for face in faces:
    if face[2] * face[3] > max_face[2] * max_face[3]:
      max_face = face
  face_image = image[max_face[1]:(max_face[1] + max_face[2]), max_face[0]:(max_face[0] + max_face[3])]
  try:
    image = cv2.resize(face_image, (48, 48), interpolation=cv2.INTER_CUBIC) / 255.
  except Exception:
    print("[+} Problem during resize")
    return None
  return face_image

def resize_image(image, size):
  try:
    image = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC) / 255.
  except Exception:
    print("+} Problem during resize")
    return None
  return image

def draw_emotion():
  pass

def demo(modelPath, showBox=False,SAMPLE_IMAGE_PATH=SAMPLE_IMAGE):
  face_x = tf.placeholder(tf.float32, [None, 2304])
  y_conv = deepnn(face_x)
  probs = tf.nn.softmax(y_conv)

  saver = tf.train.Saver()
  ckpt = tf.train.get_checkpoint_state(modelPath)
  sess = tf.Session()
  if ckpt and ckpt.model_checkpoint_path:
    saver.restore(sess, ckpt.model_checkpoint_path)
    
  result = None

  frame = SAMPLE_IMAGE_PATH
  detected_face, face_coor = format_image(frame) #face Coordinates
  
  if showBox:
      if face_coor is not None:
        [x,y,w,h] = face_coor
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

  if detected_face is not None:
        cv2.imwrite('temp.jpg', detected_face)
        tensor = image_to_tensor(detected_face)
        result = sess.run(probs, feed_dict={face_x: tensor})
        print(result)
  jsonString='{'
  maximum=0.00
  FINAL_EMOTION=''
  if result is not None:
      for index, emotion in enumerate(EMOTIONS):
        if(index!=0):
          jsonString+=','

        percentage= float("{0:.2f}".format(result[0][index]*100))
        if(percentage==0.0):
          percentage=0
  
        jsonString+='"'+str(emotion)+'":'+str(percentage)
        if(maximum<percentage):
            maximum=copy.copy(percentage)
            FINAL_EMOTION=emotion
        print('--------------------------------')
        print('                                ')
        
        print(str(emotion)+" : "+str(percentage)+"%")
        print('                                ')
        
  print('=========================================================')
  print('The Result for Input Image is : '+str(FINAL_EMOTION)+" ( "+str(maximum)+"% )")
  print('=========================================================')
  jsonString+='}'
  return jsonString

  
