from pickle import load
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input as preprocess_input_inceptionv3
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input as preprocess_input_vgg16
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
import numpy as np
import json

# import downloader as dwn
import azdownloader as dwn

path = './payload/'

file_tokenizer = path + 'tokenizer.pickle'
file_model = path + 'latest_model.h5'
file_config = path + 'config.json'

# dwn.download_if_required({
    # file_tokenizer: 'https://drive.google.com/u/0/uc?id=1IzlakJLwM7oGSJZ0seji5QgiQktl85v7',
    # file_model: 'https://drive.google.com/u/0/uc?id=1-21E36vkdJlKsxFI1dgApSDX6FYvQTMH',
    # file_config: 'https://drive.google.com/u/0/uc?id=1UVUbq_S3FRFKYm9wq973aeQobwiBTM2z'
# }, force=False)

dwn.download_if_required({
    file_tokenizer: 'tokenizer.pickle',
    file_model: 'latest_model.h5',
    file_config: 'config.json'
}, force=False)

tokenizer = None
config = None

with open(file_tokenizer, 'rb') as handle:
    tokenizer = load(handle)

model = load_model(file_model)

with open(file_config) as f:
    config = json.load(f)

def extract_feat(filename):
    # load the model
    model = None
    if config['model'] == 'vgg16':
      model = VGG16(weights='imagenet')
      img_size = 224
      preprocess_input = preprocess_input_vgg16
    elif config['model'] == 'inceptionV3':
      model = InceptionV3(weights='imagenet')
      img_size = 299
      preprocess_input = preprocess_input_inceptionv3
    else:
      raise AttributeError('model type not recognised')
    
    # re-structure the model
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    # load the photo
    image = load_img(filename, target_size=(img_size, img_size))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the model
    image = preprocess_input(image)
    # get features
    feature = model.predict(image, verbose=0)
    return feature

# map an integer to a word
def word_for_id(integer, tokenizr):
    for word, index in tokenizr.word_index.items():
        if index == integer:
            return word
    return None

def generate_desc(model, tokenizer, photo, max_length):
    # seed the generation process
    in_text = 'startseq'
    # iterate over the whole length of the sequence
    for i in range(max_length):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo,sequence], verbose=0)
        # convert probability to integer
        yhat = np.argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += ' ' + word
        # stop if we predict the end of the sequence
        if word == 'endseq':
            break
    return in_text

def beam_generate_desc(model, tokenizer, photo, max_length, beam_idx):
    in_text = 'startseq'
    k=beam_idx
    sequence = tokenizer.texts_to_sequences([in_text])[0]
    sequence = pad_sequences([sequence], maxlen=max_length)
    yhat = model.predict([photo,sequence], verbose=0)
    yhat = yhat[0].argsort()[::-1][:k]
    words=[]
    for i in range(k):
        words.append(word_for_id(yhat[i], tokenizer))
    in_text = list(list())
    in_text = [['startseq'] for i in range(k)]
    for i in range(k):
        in_text[i].append(words[i])
    for p in range(max_length-1):
        total_seq = []
        for i in range(k):
            if(in_text[i][-1]=='endseq'):
                continue
            sequence = tokenizer.texts_to_sequences([' '.join(in_text[i])])[0]
            sequence = pad_sequences([sequence], maxlen=max_length)
            yhat = model.predict([photo,sequence], verbose=0)
            yhat = np.argmax(yhat)
            word = word_for_id(yhat, tokenizer)
            in_text[i].append(word)
    return in_text
    
def predict(filepath, search_method):
    photo = extract_feat(filepath)
    max_len = config['max_len']
    is_beam = search_method == 'beam'
  
    if is_beam:
        pred = beam_generate_desc(model, tokenizer, photo, max_len, 3)
        return [' '.join(x[1:-1]) for x in pred][2]
    else:
        pred = generate_desc(model, tokenizer, photo, max_len)
        return ' '.join(pred.split()[1:-1])
  
