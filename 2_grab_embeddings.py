import dlib
import os
import numpy as np
from skimage import io

_, _, filenames = next(os.walk('jpg'))
jpg_ids = sorted([int(x[:-4]) for x in filenames])

_, _, filenames = next(os.walk('npy'))
npy_ids = sorted([int(x[:-6]) for x in filenames])

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()


def get_face_descriptor(x):
    try:
        img = io.imread('jpg/{}.jpg'.format(x))
    except:
        return
    detected_faces = detector(img, 1)
    q = 0
    for k, d in enumerate(detected_faces):
        shape = sp(img, d)
        try:
            q += 1
            f = face_rec.compute_face_descriptor(img, shape)
            mas = np.array(f)
            np.save('npy/{}_{}'.format(x, q), mas)
        except Exception as ex:
            print(ex)


for i in range(0, len(jpg_ids)):
    x = jpg_ids[i]
    if x not in npy_ids:
        print(i + 1, end=' - ')
        get_face_descriptor(x)
