import tensorflow as tf
import numpy as np
import pandas as pd

#these are all the points of the body
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

#
#
#
#
#
#
#
#
def repsToDataframe(totalReps, totalAngs, lengths):
    goodNum = lengths[0]
    repsList=[]
    for i in range(len(totalReps)): # for each video
        for rep in totalReps[i]: # for each rep in video
            if None in rep:
                continue
            else:
                rowList = []
                for j in range(3): # for keyuframes in rep
                    # concat angles of top, bottom, top into one list
                    if j == 0:
                        rowList = totalAngs[i][j].tolist()
                    else:
                        rowList = rowList + totalAngs[i][j].tolist()
                
                # add if is a good rep (for training)
                if i < goodNum:
                    rowList.append(1)
                else: 
                    rowList.append(0)
                    
                # append rep angles to reps list
                repsList.append(rowList) 
    #convert to dataframe
    df = pd.DataFrame(repsList, columns=COLS)
        
    return df.sample(frac=1).reset_index(drop=True) # shuffle dataframe and return

#
#
#
#
#
#
#
#
def split(df, ratio=0.2):
    train = pd.DataFrame(columns=COLS) 
    test = pd.DataFrame(columns=COLS)
    split = int(df.shape[0]*ratio)
    
    test = df.iloc[0:split]
    train = df.iloc[split:df.shape[0]]

    return train, test

#
#
#
#
#
#
#
#
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

#
#
#
#
#
#
#
#
def do_ml(df):
    
    print(df.head)
    
    train, test = split(df)
    
    model = train_model(train)
    
    testy = test.pop('GoodForm').values.tolist()
    testx = test.values.tolist()
    
    test_loss, test_acc = model.evaluate(testx, testy)
    print("MODEL ACCURACY: ", test_acc)