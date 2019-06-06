# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:47:50 2018

@author: KEEL
"""
import argparse
import cv2
import logging
import time
import ast
import common
import numpy as np
from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh

from  lifting.prob_model  import  Prob3dPose

import socket
import time
TCP_IP = '192.168.1.212'
TCP_PORT = 5005



logger = logging.getLogger('TfPoseEstimator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



out_dir  =  './movie/data_Doit/'

def Estimate_3Ddata(image,e,scales):
    # t0 = time.time()
    # # estimate human poses from a single image !
    # t = time.time()
    humans = e.inference(image, scales=scales)
    #elapsed = time.time() - t
    image = TfPoseEstimator.draw_humans(image, humans)
    #logger.info('inference image:%.4f seconds.' % (elapsed))
    logger.info('3d lifting initialization.')

    poseLifting = Prob3dPose('lifting/models/prob_model_params.mat')

    standard_w = 320
    standard_h = 240

    pose_2d_mpiis = []
    visibilities = []
    for human in humans:
        pose_2d_mpii, visibility = common.MPIIPart.from_coco(human)
        pose_2d_mpiis.append([(int(x * standard_w + 0.5), int(y * standard_h + 0.5)) for x, y in pose_2d_mpii])
        visibilities.append(visibility)

    pose_2d_mpiis = np.array(pose_2d_mpiis)
    visibilities = np.array(visibilities)
    if(pose_2d_mpiis.ndim != 3):
        return 0
    transformed_pose2d, weights = poseLifting.transform_joints(pose_2d_mpiis, visibilities)
    pose_3d = poseLifting.compute_3d(transformed_pose2d, weights)

    #alltime= time.time() - t0
    #logger.info('estimate all time:%.4f seconds.' % (alltime))
    return pose_3d, image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--movie', type=str, default='../cai.mp4')
    parser.add_argument('--dataname',type=str,default='')
    parser.add_argument('--datas', type=str, default='data/')
    args = parser.parse_args()
    movie = cv2.VideoCapture(args.movie)

    #w, h = model_wh('432x368')
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(656,368))
    ast_l = ast.literal_eval('[None]')
    frame_count = int(movie.get(7))
    
    for i in range(frame_count):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        
        array = []
        _, frame = movie.read()
        data, image = Estimate_3Ddata(frame,e,ast_l)
        

        x = data[0][0]
        y = data[0][1]
        z = data[0][2]
        
        for j in range(17): 
            array.extend([x[j], y[j], z[j]])
        array = " ".join(str(x) for x in array)

        image = cv2.resize(image, (656,368))
        cv2.imshow('tf-pose-estimation result', image)
        if cv2.waitKey(1) == 27:
            break

        s.sendall(bytes(array,encoding = 'utf-8'))
        
        s.close()
        
        #cv2.imwrite("data/%s.png"%i, frame)
        #fw = open('data/3d_data' + str(i)+'.txt','w')
        #fw.write(str(data))
        #fw.close()
    cv2.destroyAllWindows()