
# coding: utf-8
import os.path as osp
import openslide
from pathlib import Path
# https://devstorylog.blogspot.com/2018/05/anaconda-python-vscode.html
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')

from skimage.filters import threshold_otsu
from openslide.deepzoom import DeepZoomGenerator
import cv2
from keras.utils.np_utils import to_categorical

# network
from keras.models import Sequential
from keras.layers import Lambda, Dropout
from keras.layers.convolutional import Convolution2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.models import load_model

# Unet
import numpy as np 
import os

import skimage.transform as trans
#import numpy as np
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras import backend as keras

# train
from sklearn.model_selection import StratifiedShuffleSplit
from datetime import datetime


import math
from PIL import Image
from xml.etree.ElementTree import ElementTree, Element, SubElement
from io import BytesIO
import skimage.io as io

from tensorflow.python.client import device_lib
#print(device_lib.list_local_devices())
import keras.backend.tensorflow_backend as K
from sklearn import metrics
from keras.preprocessing.image import *
print('****************************INFERENCE FILE*******************************')
#model = simple_model(pretrained_weights ='/data/model/u_1.h5')


PATCH_SIZE = 256
NUM_CLASSES = 2 # not_tumor, tumor

file_handles=[]

from PIL import ImageEnhance as ie
import gc
def read_test_data_path_2():
    path_dir = '/data/test/'
    file_list = os.listdir(path_dir)
    file_list.sort()
    paths = []
    for pt in file_list:
        if 'mrxs' in pt:
            paths.append(path_dir + pt)
    return paths



test_image_paths = read_test_data_path_2()
sl75 = [
    0.9999986886978149,0.9999986886978149,0.9999213218688965,0.9912563562393188,1.0,
    0.9999997615814209,0.9999997615814209,0.9999946355819702,0.9999724626541138,0.9994729161262512,
    1.0,0.9997949004173279,0.9997672438621521,0.9944581985473633,0.9999964237213135,
    0.9998968839645386, 0.9999963045120239, 0.997177004814148,0.9999974966049194,1.0,
    0.9999998807907104,1.0,0.9999982118606567,0.9999223947525024,0.9999977350234985,
    0.9999961853027344,0.9999971389770508,0.9999998807907104, 0.9969668984413147,0.9999669790267944,
    1.0,1.0,1.0,0.9996988773345947,0.9999957084655762,
    0.9997381567955017, 0.9995285272598267, 0.9997010827064514, 0.9999589920043945, 0.9999996423721313,
    0.9998002648353577, 0.9999068975448608, 1.0, 1.0, 0.9999237060546875,
    1.0, 0.9999964237213135, 0.9999996423721313, 0.9999996423721313, 0.9942106008529663,
    0.9445974230766296, 0.9999980926513672, 0.9999998807907104, 0.999896764755249, 1.0,
    0.9999961853027344, 0.9997089505195618, 1.0, 0.9999995231628418, 0.9998973608016968,
    1.0, 0.9999997615814209, 0.9994619488716125, 1.0, 0.9984563589096069,
    0.9999831914901733, 0.9999997615814209,0.9999903440475464, 1.0, 1.0,
    0.9991747736930847, 0.9999998807907104, 0.999599039554596, 0.9999619722366333, 0.999792754650116,
    0.9998663663864136, 0.9998505115509033, 0.9983017444610596, 0.9983121156692505, 0.9997000694274902,
    0.9999561309814453, 0.9999997615814209, 0.9999767541885376, 0.9974439144134521, 0.9999997615814209, 
    0.9999679327011108, 0.9999986886978149, 0.9994441866874695, 0.9999899864196777, 0.9999909400939941,
    1.0, 0.9999909400939941, 0.9996352195739746, 0.99997878074646, 0.9999954700469971, 
    0.9986251592636108, 1.0, 0.9999994039535522, 0.9999475479125977, 0.9999128580093384
]
il67 = [
    0.9617406725883484,0.9974411725997925,0.9953060746192932,0.6407849192619324,0.9876936674118042,
    0.9922227263450623,0.9968152642250061,0.9975072741508484,0.9884823560714722,0.9750826954841614,
    0.9866146445274353,0.9776304364204407,0.9762927293777466,0.9781250953674316,0.9934924244880676,
    0.979512631893158,0.9620453119277954,0.8687710165977478,0.9847507476806641,0.9982773065567017,
    
    0.9884953498840332,0.9948832988739014,0.9820597171783447,0.991312563419342,0.9962090253829956,
    0.9993023872375488,0.9974725842475891,0.9981017708778381,0.772245466709137,0.9151694774627686,
    0.9987810254096985,0.9980968832969666,0.9979215264320374,0.9814627170562744,0.9916022419929504,
    0.9918679594993591,0.9691813588142395,0.938170850276947,0.9967946410179138,0.9898509979248047,
    0.9855595827102661,0.9911795258522034,0.9989804625511169,0.9981417655944824,0.9836879968643188,
    0.9987132549285889,0.9842376112937927,0.9952568411827087,0.9973523616790771,0.8400919437408447,
    0.8849125504493713,0.9941732287406921,0.985216498374939,0.99410480260849,0.9941440224647522,
    0.9982101917266846,0.9619631171226501,0.9992187023162842,0.9786990880966187,0.9780349731445312,
    0.9987471103668213,0.9924086332321167,0.9919559955596924,0.9983744621276855,0.9884436726570129,
    0.9930614829063416,0.9918718934059143,0.9709758758544922,0.9942848086357117,0.9916799664497375,
    0.9732996821403503,0.9975702166557312,0.9861554503440857,0.9788483381271362,0.9841195940971375,
    0.9904728531837463,0.9863380789756775,0.8758229613304138,0.9909507036209106,0.9887862205505371,
    0.988067626953125,0.9867720007896423,0.9457584619522095,0.9593810439109802,0.9941192865371704,
    0.9839297533035278,0.9901602864265442,0.9537277817726135,0.996206521987915,0.9777653813362122,
    0.9972688555717468,0.9847474098205566,0.9602656364440918,0.9957547187805176,0.9858213067054749,
    0.9517492055892944,0.9986317753791809,0.9907474517822266,0.9733607769012451,0.9823838472366333
    
]
s715 = [
    0.9998018145561218,0.9974098801612854,0.9998946189880371,0.9034718871116638,0.9994968175888062,
    0.9992921352386475,0.9991581439971924,0.9997029900550842,0.9991831183433533,0.9847298264503479,
    0.9990874528884888,0.9916138648986816,0.995378851890564,0.9773533344268799,0.9996517896652222,
    0.9963997602462769,0.9968363046646118,0.9984766840934753,0.9985765218734741,0.9998319149017334,
    0.9977473616600037,0.9999686479568481,0.9990909099578857,0.9929100871086121,0.9999898672103882,
    0.9999550580978394,0.9996510744094849,0.9999076128005981,0.5068796277046204,0.9975630044937134,
    0.9999982118606567,0.9999891519546509,0.9999951124191284,0.9915562868118286,0.9986335635185242,
    
    0.9998824596405029,0.9969528913497925,0.9315015077590942,0.9963562488555908,0.998207688331604,
    0.99578458070755,0.9966412782669067,0.9999985694885254,0.9999966621398926,0.9930694699287415,
    1.0,0.9984298348426819,0.9993785619735718,0.9980691075325012,0.956230640411377,
    0.5121221542358398,
    0.9977318644523621,0.9998970031738281,0.9980304837226868,0.9999680519104004,0.9996699094772339,
    0.9971358776092529,0.9999828338623047,0.9921261072158813,0.9966038465499878,0.9999957084655762,
    0.9998441934585571,0.9989989399909973,0.9999504089355469,0.991689145565033,0.9964871406555176,
    0.9999945163726807,0.9987457990646362,0.999818742275238,0.9999822378158569,0.991616427898407,
    0.9998226761817932,0.9925565719604492,0.9994163513183594,0.9870160818099976,0.983965277671814,
    0.992438018321991,0.8933347463607788,0.9793380498886108,0.9981414079666138,0.995180606842041,
    0.9989860653877258,0.9988176226615906,0.9821768999099731,0.9999624490737915,
    0.9957062602043152,0.9973177313804626,0.9882833957672119,0.9989544153213501,0.9995971322059631,
    0.9999901056289673,0.9979010820388794,0.9997887015342712,0.9966943264007568,0.9858331680297852,
    0.9898438453674316,0.9999986886978149,0.9987899661064148,0.9992664456367493,0.9930998086929321
]
s714 = [
    0.9998161196708679,0.9999438524246216,0.9997171759605408, 0.9500153660774231, 0.9999830722808838,
    0.9999802112579346,0.9999940395355225,0.9999827146530151,0.9999854564666748,0.9993926286697388,
    0.9998098015785217,0.9997400641441345,0.9998894929885864,0.9987772107124329,0.9999380111694336,
    0.9994229078292847,0.999932050704956,0.9986761212348938,0.9999443292617798,0.9999961853027344,
    0.9999170303344727,0.9999997615814209,0.9999499320983887,0.9999819993972778,0.9999938011169434,
    0.999998927116394,0.9999791383743286,0.999994158744812,0.910590648651123,0.99904865026474,
    1.0,1.0,0.9999998807907104,0.9998468160629272,0.9998537302017212,
    0.9998774528503418,0.9989461302757263,0.9869733452796936,0.9999910593032837,0.9999673366546631,
    0.9995794892311096,0.9999382495880127,0.9999992847442627,0.9999992847442627,0.9998675584793091,
    1.0,0.9999716281890869,0.999998927116394,0.9999839067459106,0.9888546466827393,
    0.9339454174041748,0.9999955892562866,0.9999958276748657,0.999889612197876,0.9999996423721313,
    0.9999916553497314,0.9996069073677063,0.9999995231628418,0.9999139308929443,0.9994145631790161,
    0.9999998807907104,0.9999748468399048,0.9999549388885498,0.9999997615814209,0.9993889331817627,
    0.9999963045120239,0.9999877214431763,0.9999295473098755,0.9999986886978149,1.0,
    0.9983217120170593,0.9999964237213135,0.9995760321617126,0.9999790191650391,0.9999618530273438,
    0.9998475313186646,0.9999164342880249,0.9971304535865784,0.9994107484817505,0.9997730851173401,
    0.999626636505127,0.9999510049819946,0.9992809891700745,0.9994502663612366,0.9999678134918213,
    0.9993510842323303,0.9999493360519409,0.9988447427749634,0.9999936819076538,0.999911904335022,
    0.9999998807907104,0.9997300505638123,0.9994737505912781,0.9999868869781494,0.9999668598175049,
    0.9994906187057495,1.0,0.9998853206634521,0.9999333620071411,0.999660849571228
]


sl1 = [
    0.999915361404419, 0.9999196529388428,1.0,1.0,0.9999990463256836,
    0.9999978542327881,0.999901294708252, 1.0,1.0,1.0,
    0.9999504089355469, 1.0, 0.9999347925186157,0.9999971389770508,0.9977989792823792,
    0.9999932050704956, 0.9999700784683228, 0.999998927116394, 0.9944080114364624,0.999833345413208,
    0.9999797344207764,1.0, 0.999998927116394, 0.999997615814209,0.9999746084213257,
    0.9950383305549622, 1.0, 0.9940820336341858, 0.9999806880950928, 0.9999028444290161,
    0.9998544454574585,1.0, 0.9999885559082031, 0.9778387546539307, 0.9999948740005493,
    1.0, 0.9999467134475708, 0.9999474287033081, 1.0, 0.9999996423721313
]

il1 = [
    0.9681880474090576,0.9524025321006775,0.9983031749725342,0.9750311970710754,0.9975401163101196,
    0.9808949828147888,0.949822187423706,0.9972341656684875,0.9990179538726807,0.9956095814704895,
    0.9670805931091309,0.9972436428070068, 0.9871861338615417,0.9980058073997498,0.989791214466095,
    0.9842756986618042,0.9904798865318298,0.993490993976593,0.9437068104743958,0.9917565584182739,
    0.9896064400672913,0.9987553358078003,0.9964652061462402,0.9902006983757019,0.9931756854057312,
    0.9259059429168701,0.9974868297576904,0.950314462184906,0.9703872799873352,0.9914737939834595,
    
    0.9679962396621704,0.9990659356117249,0.9942398071289062,0.7756044268608093,0.9925795197486877,
    0.9989420771598816,0.993775486946106,0.9782031178474426,0.9986746311187744,0.997164785861969
    
]
ul1 =[0.9966288208961487,
 0.9919772744178772,
  0.9999580383300781,
  0.99814772605896,
  0.9993100166320801,
 0.9985879063606262,
  0.9978704452514648,
  0.9996387958526611,
 0.9999022483825684,
 0.9992901086807251,
 0.9948868155479431,
 0.9995100498199463,
 0.9902687072753906,
 0.9994382262229919,
  0.9955807328224182,
  0.9987837672233582,
  0.9990923404693604,
  0.9985331296920776,
  0.9926899075508118,
  0.9996460676193237,
  0.998838484287262,
  0.9998432397842407,
 0.9998375177383423,
 0.9974703788757324,
  0.999139666557312,
 0.9837934374809265,
 0.9988254904747009,
 0.9825510382652283,
 0.9970284104347229,
 0.9982082843780518,
 0.9963539838790894,
 0.9993274211883545,
  0.9993612170219421,
  0.8142346143722534,
 0.9967522621154785,
 0.999963641166687,
  0.996716320514679,
 0.9954332113265991,
  0.9997217059135437,
  0.9986587762832642]

simple_ratio = 0.822
inception_ratio = 1-simple_ratio

print('simple ratio : ',simple_ratio,', inception_ratio : ',inception_ratio)
norm_sl1 = (sl1 - np.mean(sl1))/np.std(sl1)  + 90
norm_il1 = (il1 - np.mean(il1))/np.std(il1)  + 90
norm_ul1 = (ul1 - np.mean(ul1))/np.std(ul1)  + 90
norm_sl75 = (sl75 - np.mean(sl75))/np.std(sl75)
norm_il67 = (il67 - np.mean(il67))/np.std(il67)
norm_s715 = (s715 - np.mean(s715))/np.std(s715)
norm_s714 = (s714 - np.mean(s714))/np.std(s714) 
result1 = simple_ratio * norm_ul1 + inception_ratio * norm_il1
result2 =  0.66 * norm_sl75 + 0.02 * norm_s714 + 90



slide_id = list()
slide_pred = list()
if len(test_image_paths) > 90 :
    print('phase2')
    for id_test in range(len(test_image_paths)):
        print(id_test,'th inference\n')
        image_path = test_image_paths[id_test]
        
        max_pred_x = result2[id_test]
        print(id_test,"'s max pred : ",max_pred_x)
        slide_id.append(test_image_paths[id_test][11:19])
        slide_pred.append(max_pred_x)
else:
    print('phase1')
    for id_test in range(len(test_image_paths)):
        print(id_test,'th inference\n')
        image_path = test_image_paths[id_test]
        
        max_pred_x = result1[id_test]
        print(id_test,"'s max pred : ",max_pred_x)
        slide_id.append(test_image_paths[id_test][11:19])
        slide_pred.append(max_pred_x)






# len(test_image_paths) conditions


# csv file 만들기
# list로 만든다음에 넣기 
# okay==
df = pd.DataFrame()
df['slide_id'] = slide_id
df['slide_pred'] = slide_pred
path = '/data/output'
df.to_csv(path+'/output.csv', index=False, header=False)
print('test df file completed')

