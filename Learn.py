import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.externals import joblib

with open('Data_X.pickle', 'rb') as fx:
    x = pickle.load(fx)
    tf = TfidfVectorizer(strip_accents='unicode', max_df=0.7, min_df=44, max_features=4096,
                         norm='l2', sublinear_tf=True)
    x = tf.fit_transform(x).astype('float32').toarray()
with open('Data_Y.pickle', 'rb') as fy:
    y = pickle.load(fy)
    le = LabelEncoder()
    le.fit(y)
    y = le.transform(y)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
lb = LabelBinarizer()
lb.fit(y)
joblib.dump(tf, 'Data_T.pickle')
joblib.dump(lb, 'Data_LB.pickle')
del x, y
y_train = lb.transform(y_train)
y_test = lb.transform(y_test)
classifier = Sequential()
classifier.add(Dense(output_dim=1024, activation='relu', init='glorot_uniform', input_dim=4096))
classifier.add(Dropout(0.2))
classifier.add(Dense(output_dim=256, activation='relu', init='glorot_uniform'))
classifier.add(Dense(activation='softmax', output_dim=17))
classifier.add(Dropout(0.2))
classifier.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
classifier.fit(x_train, y_train, nb_epoch=10, batch_size=128, shuffle=True, validation_data=(x_test, y_test))
classifier.save('Data_Z.mdl')
