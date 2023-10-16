# Number Recognition App

## Table of Contents
1. [General Information](#general-information)
2. [Installation](#installation)

## General Information:
In this application you can write a number on the canvas at the top left.
When writing, the image you write is redrawn (image in the middle), compressed and then fed into a neural network.
This neural network is trained with the MNIST handwritten numbers dataset 
and predicts the number which is written on the canvas.
At the top right the image fed into the neural network is shown in higher resolution (original: 28x28).
The probablities for every number are displayed at the bottom right.
You can use the drawing options under the canvas.
Dont write too fast because making a copy of the drawn image creates a small delay!

## Installation
Follow these steps to install the number recognition app.
1. Make sure Python and Pip are installed.
2. Clone this repository.
```
git clone https://github.com/soosmann/number_recognition.git
```
3. Install project dependencies.
```
pip install -r requirements.txt
```
4. Start app.
```
python frontend.py
```