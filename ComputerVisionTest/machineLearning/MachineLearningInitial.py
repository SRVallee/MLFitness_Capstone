import tensorflow as tf
import numpy as np
import pandas as pd

COLS = [
        'headLR1', 'headFB1',
        'backLR1', 'backFB1',
        'lShoulderFB1', 'lShoulderUD1',
        'lHipLR1', 'lHipFB1',
        'rShoulderFB1', 'rShoulderUD1',
        'rHipLR1', 'rHipFB1',
        'lElb1', 'rElb1',
        'lKnee1', 'rKnee1',
        'headLR2', 'headFB2',
        'backLR2', 'backFB2',
        'lShoulderFB2', 'lShoulderUD2',
        'lHipLR2', 'lHipFB2',
        'rShoulderFB2', 'rShoulderUD2',
        'rHipLR2', 'rHipFB2',
        'lElb2', 'rElb2',
        'lKnee2', 'rKnee2',
        'headLR3', 'headFB3',
        'backLR3', 'backFB3',
        'lShoulderFB3', 'lShoulderUD3',
        'lHipLR3', 'lHipFB3',
        'rShoulderFB3', 'rShoulderUD3',
        'rHipLR3', 'rHipFB3',
        'lElb3', 'rElb3',
        'lKnee3', 'rKnee3',
        'GoodForm'
    ]

def repsToDataframe(totalReps, totalAngs):
    df = pd.DataFrame(columns=COLS)
    for i in range(2):
        for reps in totalReps:
            break    


def split(df, ratio=0.2):
    test = pd.DataFrame(columns=COLS)
    for i in range(df.shape[0]-1, -1, int(1/ratio) * -1):
        if test.size == 0:
            test = df.iloc[[i]]
        else:
            pd.concat([test, df.iloc[[i]]], ignore_index=True)
        df.drop(index=i)
    
    return df, test

def train_model(df, epochs=10):
    tf.random.set_seed(42)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(48, activation='relu'),
        tf.keras.layers.Dense(48, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.binary_crossentropy,
        metrics=['accuracy']
    )
    
    y = df.pop('GoodForm').values.tolist()
    print(y)
    x = df.values.tolist()
    print(x)
    
    model.fit(x, y, epochs)
    
    return model

def do_ml(data):
    df = pd.DataFrame(data, columns=COLS)
    
    print(df.head)
    
    train, test = split(df)
    
    model = train_model(train)
    
    testy = test.pop('GoodForm').values.tolist()
    testx = test.values.tolist()
    
    test_loss, test_acc = model.evaluate(testx, testy)
    print("MODEL ACCURACY: ", test_acc)