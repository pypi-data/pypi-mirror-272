def load():
    num = int(input())
    if (num == 1):
        print('''
import numpy as np
class Perceptron:
  def __init__(self,input_size,learning_rate = 0.1,epochs = 10):
    self.weights=np.random.rand(input_size)
    self.bias = np.random.rand()
    self.learning_rate = learning_rate
    self.epochs = epochs

  def activate(self,x):
    return 1 if x > 0 else 0

  def predict(self,inputs):
    summation = np.dot(inputs,self.weights) + self.bias
    return self.activate(summation)

  def train(self,inputs,target):
    print("Epochs | Input x1 | Input x2  | Desired Output  | Net Input + Bias     | Error | Weights | Change in Weights")
    for epoch in range(self.epochs):
      for i in range(len(inputs)):
        prediction = self.predict(inputs[i])
        error = target[i] - prediction
        delta_weights = self.learning_rate*error*inputs[i]
        self.weights += delta_weights
        self.bias += self.learning_rate * error
        print(f"{epoch+1:7}|{inputs[i][0]:9} | {inputs[i][1]:9} | {target[i]:15} | {np.dot(inputs[i],self.weights) + self.bias : 20} | {target[i] - prediction:5} | {self.weights} | {delta_weights}")

# And_gate
print("AND_GATE")
and_gate_inputs = np.array([[0,0],[0,1],[1,0],[1,1]])
and_gate_targets = np.array([0,0,0,1])
and_gate_perceptron = Perceptron(input_size=2)
and_gate_perceptron.train(and_gate_inputs,and_gate_targets)
# Or_gate
print("OR_GATE")
or_gate_inputs = np.array([[0,0],[0,1],[1,0],[1,1]])
or_gate_targets = np.array([0,1,1,1])
or_gate_perceptron = Perceptron(input_size=2)
or_gate_perceptron.train(or_gate_inputs,or_gate_targets)
# xOR_GATE
print("XOR_GATE")
Xor_gate_inputs = np.array([[0,0],[0,1],[1,0],[1,1]])
Xor_gate_targets = np.array([0,1,1,0])
Xor_gate_perceptron = Perceptron(input_size=2)
Xor_gate_perceptron.train(Xor_gate_inputs,Xor_gate_targets)
''')
    elif(num == 2):
        print('''
import numpy as np
import random as rd
 
def signum(type, no):
    if type == "unipolar":
        if no >= 0:
            return 1
        else:
            return 0
    elif type == "bipolar":
        if no < 0:
            return -1
        elif no == 0:
            return 0
        else:
            return 1
def network_of_preceptron(x, w, b, c, d):
    xi = np.asarray(x).astype(float)
    weights = np.asarray(w).astype(float)
    it, max_epochs = 1, 1000
    error = -1
    while it < max_epochs and error != 0:
        print(f"\nIteration {it}-")
        it += 1
        net = np.dot(weights, xi) + b
        oi = signum(type="unipolar",no=net)
        r = d - oi
        delta_w = c * r * xi
        weights += delta_w
        b += r
        error = r
        print(f"Net: {net}\nObserved Output: {oi}\nError: {r}\n\u0394 W: {delta_w}\nUpdated Weights: {weights}\nUpdated Bias: {b}")
input = [1, 1]
hidden = [[0, 0], [0, 1], [1, 0], [1, 1]]
weights = [rd.randint(-2,2) for i in range(4)]# [2, 2, 2, -5]
out_xor = {(-1, -1) : 0, (-1,1) : 1, (1, -1) : 1, (1, 1) : 0}
out_and = {(0, 0) : 0, (0, 1) : 0, (1, 0) : 0, (1, 1) : 1}
bias = -2
new_inputs = []
for i in hidden:
    new_inputs.append(signum(no=np.dot(i, input) + bias, type="unipolar"))
print(f"Hidden Layer Input: {new_inputs}\nInitial Weights: {weights}\nInitial Bias: {bias}\nLearning Rate: {1}")
network_of_preceptron(new_inputs, weights, bias, 1, out_and[tuple(input)])
''')
    elif(num == 3):
        print('''
import numpy as np
input = [0.05, 0.1]
weights_in = [[0.15, 0.2], [0.25, 0.3]]
weights_hddn = [[0.4, 0,45], [0.5, 0.55]]
bias = 0.35
 
def sigmoid(no, type='unipolar', lam=1):
    if type == "unipolar":
        return 1 / (1 + np.exp(-no * lam))
    elif type == "bipolar":
        return (2 / (1 + np.exp(-no * lam))) - 1
 
def der_sigmoid(oi, type='unipolar'):
    if type == "unipolar":
        return oi * (1 - oi)
    elif type == "bipolar":
        return (1 - oi**2) / 2
 
def forward_pass(b1,b2):
    net_h1 = np.dot(w_x1, x) + b1
    out_h1 = sigmoid(net_h1)
    net_h2 = np.dot(w_x2, x) + b1
    out_h2 = sigmoid(net_h2)
    global h
    h = [out_h1, out_h2]
 
    net_o1 = np.dot(w_h1, h) + b2
    out_o1 = sigmoid(net_o1)
    net_o2 = np.dot(w_h2, h) + b2
    out_o2 = sigmoid(net_o2)
    global o
    o = [out_o1, out_o2]
    global e
    e = []
    for oi, di in zip(o, d):
        e.append(((oi - di)**2) / 2)
    print("Forward Pass:")
    print(f"Net_h1: {net_h1:.4f}, Out_h1: {out_h1:.4f}\nNet_h2: {net_h2:.4f}, Out_h2: {out_h2:.4f}")
    print(f"Net_o1: {net_o1:.4f}, Out_o1: {out_o1:.4f}\nNet_o2: {net_o2:.4f}, Out_o2: {out_o2:.4f}")
    print(f"E_o1: {e[0]:.4f}, E_o2: {e[1]:.4f}\nTotal Error: {sum(e):.4f}\n")
 
def backward_pass(eta):
    w_h1[0] -= eta * ((o[0]- d[0]) * der_sigmoid(o[0]) * h[0])
    w_h1[1] -= eta * ((o[0]- d[0]) * der_sigmoid(o[0]) * h[1])
    w_h2[0] -= eta * ((o[1]- d[1]) * der_sigmoid(o[1]) * h[0])
    w_h2[1] -= eta * ((o[1]- d[1]) * der_sigmoid(o[1]) * h[1])
    w_x1[0] -= eta * (((o[0]- d[0]) * der_sigmoid(o[0]) * w_h1[0] * der_sigmoid(h[0]) * x[0]) + ((o[1]- d[1]) * der_sigmoid(o[1]) * w_h2[0] * der_sigmoid(h[0]) * x[0]))
    w_x1[1] -= eta * (((o[0]- d[0]) * der_sigmoid(o[0]) * w_h1[0] * der_sigmoid(h[0]) * x[1]) + ((o[1]- d[1]) * der_sigmoid(o[1]) * w_h2[0] * der_sigmoid(h[0]) * x[1]))
    w_x2[0] -= eta * (((o[0]- d[0]) * der_sigmoid(o[0]) * w_h1[1] * der_sigmoid(h[1]) * x[0]) + ((o[1]- d[1]) * der_sigmoid(o[1]) * w_h2[1] * der_sigmoid(h[1]) * x[0]))
    w_x2[1] -= eta * (((o[0]- d[0]) * der_sigmoid(o[0]) * w_h1[0] * der_sigmoid(h[1]) * x[1]) + ((o[1]- d[1]) * der_sigmoid(o[1]) * w_h2[1] * der_sigmoid(h[1]) * x[1]))
    print("Backward Pass:")
    print(f"Updated_w5: {w_h1[0]:.4f}, Updated_w6: {w_h1[1]:.4f}\nUpdated_w7: {w_h2[0]:.4f}, Updated_w8: {w_h2[1]:.4f}")
    print(f"Updated_w1: {w_x1[0]:.4f}, Updated_w2: {w_x2[0]:.4f}\nUpdated_w3: {w_x1[1]:.4f}, Updated_w4: {w_x2[1]:.4f}\n\n")
 
global x, w_x1, w_x2, w_h1, w_h2, d
x = [0.10, 0.50]      
w_x1 = [0.10, 0.30]   #[w1, w2]
w_x2 = [0.20, 0.40]   #[w3, w4]
b1 = 0.25             
w_h1 = [0.50, 0.60]   #[w5, w6]
w_h2 = [0.70, 0.80]   #[w7, w8]
b2 = 0.35             
d = [0.05, 0.95]      
eta = 0.6       
 
# x = [0.05, 0.10]
# w_x1 = [0.15, 0.20]
# w_x2 = [0.25, 0.30]
# b1 = 0.35
# w_h1 = [0.40, 0.45]
# w_h2 = [0.50, 0.55]
# b2 = 0.60
# d = [0.01, 0.99]
# eta = 0.25
 
def backpropogation():
    forward_pass(b1, b2)
    backward_pass(eta)
it, max_epochs = 1, 10
e = [float('inf')]
while it <= max_epochs and sum(e) != 0:
    print(f"Iteration {it}-")
    backpropogation()
    it += 1
''')
    elif(num == 4):
        print('''

import tensorflow as tf
from tensorflow.keras import datasets, layers, models


(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0


model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10)
])


model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


history = model.fit(train_images, train_labels, epochs=1,
                    validation_data=(test_images, test_labels))


test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(f'Test accuracy: {test_acc}')

model.predict(train_images)

''')
    elif(num == 5):
        print('''

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.preprocessing.sequence import pad_sequences

max_features = 1000
(train_data, train_labels), (test_data, test_labels) = datasets.imdb.load_data(num_words=max_features)

maxlen = 100  
train_data = pad_sequences(train_data, maxlen=maxlen)
test_data = pad_sequences(test_data, maxlen=maxlen)

model = models.Sequential([
    layers.Embedding(max_features, 32),
    layers.SimpleRNN(32),
    layers.Dense(1, activation='sigmoid'),
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_data, train_labels, validation_data=(test_data, test_labels), epochs=10)

loss, acc = model.evaluate(test_data, test_labels)
print(f'Test loss: {loss}, Test accuracy: {acc}')


''')
    elif(num == 6):
        print('''
import numpy as np
from math import sqrt
 
def dist_finder(w, x):
    distance = 0
    for i in range(len(x)):
        distance += pow(w[i] - x[i], 2)
    return round(sqrt(distance), 8)
 
def update_wgts(w, x, learning_rate):
    return w + learning_rate * (x - w)
 
def Kohonens_SOM(x1, x2, w1, w2, epochs=20, learning_rate=0.5):
    for j in range(epochs):
        print("Epoch ", j + 1)
        d1 = dist_finder(w1, x1)
        d2 = dist_finder(w2, x1)
        print(f"For X1-: \nd1: {d1:.4f} d2: {d2:.4f}")
        min_distance = min(d1, d2)
        print("Minimum Weight:", min_distance)
        if d1 < d2:
            w1 = update_wgts(w1, x1, learning_rate)
            print("Updated W1", w1)
        else:
            w2 = update_wgts(w2, x1, learning_rate)
            print("Updated W2", w2)
        d3 = dist_finder(w1, x2)
        d4 = dist_finder(w2, x2)
        print(f"\nFor X2-: \nd3: {d3:.4f} d4: {d4:.4f}")
        min_distance = min(d3, d4)
        print("Minimum Weight:", min_distance)
        if d3 < d4:
            w1 = update_wgts(w1, x2, learning_rate)
            print("Updated W1", w1)
        else:
            w2 = update_wgts(w2, x2, learning_rate)
            print("Updated W2", w2)
 
x1 = np.array([1, 0, 0, 0])
x2 = np.array([0, 1, 0, 0])
w1 = np.array([0.2, 0.5, 0.6, 0.8])
w2 = np.array([0.1, 0.3, 0.6, 0.7])
Kohonens_SOM(x1, x2, w1, w2)
''')
    elif(num == 7):
        print('''
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model
from sklearn.model_selection import train_test_split
 
# %%
data = pd.read_csv('yourcsv.csv')
# data = pd.read_csv('/Iris.csv')
print(data.shape)
print(data.columns)
data.info()
 
# %%
features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
            'BMI', 'DiabetesPedigreeFunction', 'Age']
label = ['Outcome']
X = data[features]
y = data[label]
 
# %%
def generate_latent_points(latent_dim, n_samples):
	x_input = np.random.randn(latent_dim * n_samples)
	x_input = x_input.reshape(n_samples, latent_dim)
	return x_input
 
# %%
def generate_fake_samples(generator, latent_dim, n_samples):
	x_input = generate_latent_points(latent_dim, n_samples)
	X = generator.predict(x_input)
	y = np.zeros((n_samples, 1))
	return X, y
 
# %%
def generate_real_samples(n):
  X = data.sample(n)
 
  #generate class labels
  y = np.ones((n, 1))
  return X, y
 
# %%
def define_generator(latent_dim, n_outputs=9):
    model = Sequential()
    model.add(Dense(15, activation='relu', kernel_initializer='he_uniform', input_dim=latent_dim))
    model.add(Dense(30, activation='relu'))
    model.add(Dense(n_outputs, activation='linear'))
    return model
 
gen = define_generator(10)
gen.summary()
 
# %%
def define_discriminator(n_inputs=9):
    model = Sequential()
    model.add(Dense(25, activation='relu', kernel_initializer='he_uniform', input_dim=n_inputs))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
 
discriminator1 = define_discriminator()
discriminator1.summary()
 
# %%
def define_gan(generator, discriminator):
	discriminator.trainable = False
	model = Sequential()
	model.add(generator)
	model.add(discriminator)
	model.compile(loss='binary_crossentropy', optimizer='adam')
	return model
 
# %%
def plot_history(d_hist, g_hist):
	plt.subplot(1, 1, 1)
	plt.plot(d_hist, label='d')
	plt.plot(g_hist, label='gen')
	# plt.legend()
	# plot discriminator accuracy
	# pyplot.subplot(2, 1, 2)
	# pyplot.plot(a1_hist, label='acc-real')
	# pyplot.plot(a2_hist, label='acc-fake')
	plt.show()
 
# %%
def train(g_model, d_model, gan_model, latent_dim, n_epochs=250, n_batch=128):
    half_batch = int(n_batch / 2)
 
    d_history = []
    g_history = []
 
    for epoch in range(n_epochs):
        x_real, y_real = generate_real_samples(half_batch)
        x_fake, y_fake = generate_fake_samples(g_model, latent_dim, half_batch)
        d_loss_real, d_real_acc = d_model.train_on_batch(x_real, y_real)
        d_loss_fake, d_fake_acc = d_model.train_on_batch(x_fake, y_fake)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
 
        # prepare points in latent space as input for the generator
        x_gan = generate_latent_points(latent_dim, n_batch)
 
        # create inverted labels for the fake samples
        y_gan = np.ones((n_batch, 1))
 
        # update the generator via the discriminator's error
        g_loss_fake = gan_model.train_on_batch(x_gan, y_gan)
 
        print(f'>Epoch {epoch+1}, Real_Loss_Disc: {d_loss_real:.4f} Fake_Loss_Disc=: {d_loss_fake:.3f} Disc_Loss: {d_loss:.3f} Gen_Loss: {g_loss_fake:.3f}')
        d_history.append(d_loss)
        g_history.append(g_loss_fake)
    plot_history(d_history, g_history)
    g_model.save('Generator.h5')
 
# %%
def summarize_performance(epoch, generator, discriminator, latent_dim, n=100):
	x_real, y_real = generate_real_samples(n)
	_, acc_real = discriminator.evaluate(x_real, y_real, verbose=0)
	x_fake, y_fake = generate_fake_samples(generator, latent_dim, n)
	_, acc_fake = discriminator.evaluate(x_fake, y_fake, verbose=0)
	print(epoch, acc_real, acc_fake)
	plt.scatter(x_real[:, 0], color='red')
	plt.scatter(x_fake[:, 0], color='blue')
	plt.show()
 
# %%
latent_dim = 10
discriminator = define_discriminator()
generator = define_generator(latent_dim)
gan_model = define_gan(generator, discriminator)
train(generator, discriminator, gan_model, latent_dim)
 
# %%
model = load_model('Generator.h5')
latent_points = generate_latent_points(10, 750)
X = model.predict(latent_points)
data_fake = pd.DataFrame(data=X,  columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
                            'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'])
data_fake.head(20)
''')
    elif(num == 8):
        print('''
import tensorflow as tf
from sklearn.datasets import load_iris
from tensorflow.keras import models,layers
from sklearn.decomposition import PCA

iris = load_iris()
X = iris.data
y = iris.target

# print(X.shape,y.shape) (150,4) & (150)
pca = PCA(n_components=4)
X_pca = pca.fit_transform(X)

autoencoder = models.Sequential([
    layers.Dense(6,activation='relu',input_shape=(4,)),
    layers.Dense(2,activation='relu'),
    layers.Dense(4,activation='sigmoid')
])

autoencoder.compile(optimizer='adam',loss='mse')
autoencoder.fit(X,y,epochs=2,batch_size=10)
X_autoencoded = autoencoder.predict(X)

pca_mse = mean_squared_error(X,pca.inverse_transform(X_pca))
autoencoder_mse = mean_squared_error(X,X_autoencoded)

print("PCA MSE:",pca_mse)
print("Autoencoder_MSE:",autoencoder_mse)

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.scatter(X_pca[:,0],X_pca[:,1],c=y,cmap='viridis')
plt.title('PCA')

plt.subplot(1,2,2)
plt.scatter(X_autoencoded[:,0],X_autoencoded[:,1],c=y,cmap='viridis')
plt.title('Autoencoder')

plt.show()

''')