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
import copy
from  lifting.prob_model  import  Prob3dPose

import socket
import time
TCP_IP = '192.168.1.212'
TCP_PORT = 5007


logger = logging.getLogger('TfPoseEstimator')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# def Estimate_3Ddata(image,e,scales):

#     humans = e.inference(image, scales=scales)

#     if (len(humans) == 0):
#         human_appear = False
#         return 0, image

#     image = TfPoseEstimator.draw_humans(image, humans)

#     logger.info('3d lifting initialization.')

#     poseLifting = Prob3dPose('lifting/models/prob_model_params.mat')

#     pose_2d_mpiis = []
#     visibilities = []
#     for human in humans:
#         pose_2d_mpii, visibility = common.MPIIPart.from_coco(human)
#         pose_2d_mpiis.append([(int(x * 432 + 0.5), int(y * 368 + 0.5)) for x, y in pose_2d_mpii])
#         visibilities.append(visibility)

#     pose_2d_mpiis = np.array(pose_2d_mpiis)
#     visibilities = np.array(visibilities)
#     if(pose_2d_mpiis.ndim != 3):
#         return 0
#     transformed_pose2d, weights = poseLifting.transform_joints(pose_2d_mpiis, visibilities)
#     pose_3d = poseLifting.compute_3d(transformed_pose2d, weights)

#     return pose_3d, image

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation run')
    parser.add_argument('--movie', type=str, default='../demo2.mp4')
    parser.add_argument('--dataname',type=str,default='')
    parser.add_argument('--datas', type=str, default='data/')
    args = parser.parse_args()
    #movie = cv2.VideoCapture(args.movie)
    #movie = cv2.VideoCapture("rtsp://admin:admin@192.168.1.137:30012")
    movie = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    e = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432,368))
    ast_l = ast.literal_eval('[None]')
    
    
    array = []
    previous_frame = 0
    previous_frame2 = 0
    
    # _, frame = movie.read()
    # data, frame = Estimate_3Ddata(frame,e,ast_l)
    # # if(data == 0):
    # #     previous_frame[0] = 0
    # previous_frame[0] = data
    
    # _, frame = movie.read()
    # data, frame = Estimate_3Ddata(frame,e,ast_l)
    # # if(data == 0):
    # #     previous_frame[1] = 0
    # previous_frame[1] = data
    #frame_count = int(movie.get(7))  
    #for i in range(frame_count):
    while(True):    

        
        
        _, frame = movie.read()

        #***************************************************************
        #data, image = Estimate_3Ddata(frame,e,ast_l)

        humans = e.inference(frame, scales=ast_l)

        if(len(humans)==0):
            array = []
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            
            image = cv2.resize(frame, (432,368))
            cv2.imshow('tf-pose-estimation result', image)
            
            array = [-7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936, -7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936]
            array = " ".join(str(x) for x in array)
            s.sendall(bytes(array,encoding = 'utf-8'))
            s.close()
            #print(array)
            print("No human appear...")
                       
            if cv2.waitKey(1) == 27:
                break

            continue


        elif len(humans) > 0:

            array = []

            image = cv2.resize(frame, (432,368))
            cv2.imshow('tf-pose-estimation result', image)
            if cv2.waitKey(1) == 27:
                break

            pop_array = []
            for j in range(len(humans)):
                
                #for i in range(17):
                    #print(humans[j].body_parts[i].x)
                if len(humans[j].body_parts)<13:
                    # array = []
                    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # s.connect((TCP_IP, TCP_PORT))
                    pop_array.append(j)
                    # print("no complete person appears")
                    # array = [-7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936, -7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936]
                    # array = " ".join(str(x) for x in array)
                    # s.sendall(bytes(array,encoding = 'utf-8'))
                    # s.close()
                    # print(array)

            #humans.pop(pop_array)
            humans = [e for e in humans if humans.index(e) not in pop_array]

            if len(humans) == 0:
                array = []
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                print("no complete person appears")
                array = [-7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936, -7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936]
                array = " ".join(str(x) for x in array)
                s.sendall(bytes(array,encoding = 'utf-8'))
                s.close()
                #print(array)
                

            if len(humans) >= 1:
                # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # s.connect((TCP_IP, TCP_PORT))
            
                human_min = min(len(humans), 2)
                humans = humans[:human_min]
                print("complete human appears")
                frame = TfPoseEstimator.draw_humans(frame, humans)

                #logger.info('3d lifting initialization.')

                poseLifting = Prob3dPose('lifting/models/prob_model_params.mat')

                
                
                #***************************************************************
                if len(humans) == 1:

                    pose_2d_mpiis = []
                    visibilities = []
                                            
                    human = humans[0]
                    if (not 9 in human.body_parts) and (not 12 in human.body_parts) and (8 in human.body_parts) and (11 in human.body_parts):
                        human.body_parts[9] = copy.copy(human.body_parts[8])
                        human.body_parts[12] = copy.copy(human.body_parts[11])
                        
                        human.body_parts[9].y = human.body_parts[8].y + 0.8*(human.body_parts[8].y-human.body_parts[1].y)
                        human.body_parts[12].y = human.body_parts[11].y + 0.8*(human.body_parts[11].y-human.body_parts[1].y)

                        human.body_parts[10] = copy.copy(human.body_parts[8])
                        human.body_parts[13] = copy.copy(human.body_parts[11])
                        
                        human.body_parts[10].y = human.body_parts[8].y + 1.6*(human.body_parts[8].y-human.body_parts[1].y)
                        human.body_parts[13].y = human.body_parts[11].y + 1.6*(human.body_parts[11].y-human.body_parts[1].y)

                    pose_2d_mpii, visibility = common.MPIIPart.from_coco(human)
                    pose_2d_mpiis.append([(int(x * 432 + 0.5), int(y * 368 + 0.5)) for x, y in pose_2d_mpii])
                    visibilities.append(visibility)

                    pose_2d_mpiis = np.array(pose_2d_mpiis)
                    visibilities = np.array(visibilities)
                    # if(pose_2d_mpiis.ndim != 3):
                    #     return 0
                    transformed_pose2d, weights = poseLifting.transform_joints(pose_2d_mpiis, visibilities)
                    data = poseLifting.compute_3d(transformed_pose2d, weights)
                    print(data)

                    array = []
                    data_mean = (np.array(np.array(data[0]) + previous_frame))/2
                    previous_frame = data[0]

                    x = data_mean[0]
                    y = data_mean[1]
                    z = data_mean[2]

                    for j in range(17): 
                        array.extend([x[j], y[j], z[j]])

                    array.extend([-7.6688656386986205, 13.011893068270316, -76.44649495830629, -96.04607485096246, -92.81828865032355, -66.12264213078763, -71.17861721812547, -141.7884342909674, -513.2769495552633, -93.24026034432053, -49.908593729408864, -859.9538382379666, 93.9853006386473, 118.84215202672682, -65.02325740984881, 109.97191521670692, 49.68661022821461, -500.2815729013937, 43.949669089576304, 113.42515121422467, -826.8247952726662, -30.178936716325808, 32.71730632233089, 199.99237952146646, 1.3300306085416633, 4.264303940397121, 518.4445448043695, 68.23552287179022, -59.627185316857094, 579.1492439958412, 16.227613839804388, -26.9316905346605, 762.9746341871173, 120.34132128722644, 125.661445590322, 493.24154801020865, 142.98984394558525, 237.95051301631239, 192.7825133883671, 194.12002009602188, 169.61851447575899, -20.96114030070511, -98.459444321648, -96.3385622492707, 492.55167674182735, -193.9636006266926, -160.35763166809497, 189.06132786524188, -170.02771737499376, -227.0821354762086, -72.1787662704936])
                    array = " ".join(str(x) for x in array)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    image = cv2.resize(frame, (432,368))
                    cv2.imshow('tf-pose-estimation result', image)
                    if cv2.waitKey(1) == 27:
                        break

                    #print(array)
                    s.sendall(bytes(array,encoding = 'utf-8'))
                    s.close() 
                       

                if len(humans) == 2:
                    array = []

                    data = []
                    pose_2d_mpiis = []
                    visibilities = []
                    # for k in range(len(humans)):
                    human1_hip = humans[0].body_parts[1].x 
                    human2_hip = humans[1].body_parts[1].x

                    if(human1_hip > human2_hip):
                        humans[0], humans[1] = humans[1], humans[0]

                    for human in humans:
                        if (not 9 in human.body_parts) and (not 12 in human.body_parts) and (8 in human.body_parts) and (11 in human.body_parts):
                            human.body_parts[9] = copy.copy(human.body_parts[8])
                            human.body_parts[12] = copy.copy(human.body_parts[11])
                            
                            human.body_parts[9].y = human.body_parts[8].y + 0.8*(human.body_parts[8].y-human.body_parts[1].y)
                            human.body_parts[12].y = human.body_parts[11].y + 0.8*(human.body_parts[11].y-human.body_parts[1].y)

                            human.body_parts[10] = copy.copy(human.body_parts[8])
                            human.body_parts[13] = copy.copy(human.body_parts[11])
                            
                            human.body_parts[10].y = human.body_parts[8].y + 1.6*(human.body_parts[8].y-human.body_parts[1].y)
                            human.body_parts[13].y = human.body_parts[11].y + 1.6*(human.body_parts[11].y-human.body_parts[1].y)


                    pose_2d_mpii, visibility = common.MPIIPart.from_coco(humans[0])
                    pose_2d_mpiis.append([(int(x * 432 + 0.5), int(y * 368 + 0.5)) for x, y in pose_2d_mpii])
                    visibilities.append(visibility)

                    pose_2d_mpiis = np.array(pose_2d_mpiis)
                    visibilities = np.array(visibilities)
                    transformed_pose2d, weights = poseLifting.transform_joints(pose_2d_mpiis, visibilities)
                    data.append(poseLifting.compute_3d(transformed_pose2d, weights))

                    pose_2d_mpiis = []
                    visibilities = []

                    
                    pose_2d_mpii, visibility = common.MPIIPart.from_coco(humans[1])
                    pose_2d_mpiis.append([(int(x * 432 + 0.5), int(y * 368 + 0.5)) for x, y in pose_2d_mpii])
                    visibilities.append(visibility)

                    pose_2d_mpiis = np.array(pose_2d_mpiis)
                    visibilities = np.array(visibilities)
                    transformed_pose2d, weights = poseLifting.transform_joints(pose_2d_mpiis, visibilities)
                    data.append(poseLifting.compute_3d(transformed_pose2d, weights))
                    #print(data)
                    # data_mean2 = (np.array(np.array(data[0]) + previous_frame2[0] + previous_frame2[1]))/3
                    # previous_frame2[0] = previous_frame2[1]
                    # previous_frame2[1] = np.array(data[0])

                    # x = data_mean2[0]
                    # y = data_mean2[1]
                    # z = data_mean2[2]

                    x = data[0][0][0]
                    y = data[0][0][1]
                    z = data[0][0][2]

                    for j in range(17): 
                        array.extend([x[j], y[j], z[j]])

                    # data_mean3 = (np.array(np.array(data[1]) + previous_frame3[0] + previous_frame3[1]))/3
                    # previous_frame3[0] = previous_frame3[1]
                    # previous_frame3[1] = np.array(data[1])

                    # x2 = data_mean3[0]
                    # y2 = data_mean3[1]
                    # z2 = data_mean3[2]
                    x2 = data[1][0][0]
                    y2 = data[1][0][1]
                    z2 = data[1][0][2]

                    for j in range(17): 
                        array.extend([x2[j], y2[j], z2[j]])

                    array = " ".join(str(x) for x in array)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    image = cv2.resize(frame, (432,368))
                    cv2.imshow('tf-pose-estimation result', image)
                    if cv2.waitKey(1) == 27:
                        break

                    print(array)
                    s.sendall(bytes(array,encoding = 'utf-8'))
                    
                    s.close() 
                    #array = []   
                
                # pose_2d_mpiis = np.array(pose_2d_mpiis)
                # visibilities = np.array(visibilities)
                # # if(pose_2d_mpiis.ndim != 3):
                # #     return 0
                # transformed_pose2d, weights = poseLifting.transform_joints(pose_2d_mpiis, visibilities)
                # data = poseLifting.compute_3d(transformed_pose2d, weights)
                # #***************************************************************

            
                # data_mean = (np.array(data + previous_frame[0] + previous_frame[1]))/3
                # previous_frame[0] = previous_frame[1]
                # previous_frame[1] = data

                # x = data_mean[0][0]
                # y = data_mean[0][1]
                # z = data_mean[0][2]
                
                # for j in range(17): 
                #     array.extend([x[j], y[j], z[j]])
                # array = " ".join(str(x) for x in array)

                # image = cv2.resize(frame, (432,368))
                # cv2.imshow('tf-pose-estimation result', image)
                # if cv2.waitKey(1) == 27:
                #     break

                # s.sendall(bytes(array,encoding = 'utf-8'))
                
                # s.close()
 