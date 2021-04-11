import dlib
import numpy as np
from skimage import io
import nmslib


sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_rec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()
index = nmslib.init(method='hnsw', space='l2', data_type=nmslib.DataType.DENSE_VECTOR)
index.loadIndex('embeddings.bin')
index.setQueryTimeParams({'efSearch': 400})


def get_face_descriptor(filename):
    img = io.imread(filename)
    win1 = dlib.image_window()
    win1.clear_overlay()
    win1.set_image(img)
    face_descriptor = None
    shape = None
    detected_faces = detector(img, 1)
    for k, d in enumerate(detected_faces):
        shape = sp(img, d)
        win1.clear_overlay()
        win1.add_overlay(d)
        win1.add_overlay(shape)
    try:
        face_descriptor = face_rec.compute_face_descriptor(img, shape)
        face_descriptor = np.asarray(face_descriptor)
    except Exception as ex:
        print(ex)

    return face_descriptor


def get_link():
    try:
        embedding = get_face_descriptor('1.jpg')
        ids, dists = index.knnQuery(embedding, k=1)
        best_dx = ids[0]
        s = ''
        with open('associations.txt', 'r') as file_:
            for line in file_:
                w = str(best_dx) + '|'
                if line.find(w) == 0:
                    s = line.split('|')[1]
        s = 'https://vk.com/id' + s.split('_')[0]
        for bad_symbols in ['.txt', '.npy', '\n']:
            s = s.replace(bad_symbols, '')
        print(s, ids[0], dists[0])
        return s
    except:
        return 'NOT FOUND'


if __name__ == '__main__':
    get_link()
