import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#these are all the points of the body. 49 points. UD = UP down, FB = Face Back
COLS = [
        #up postion
        'headLR1', 'headFB1',
        'backLR1', 'backFB1',
        'lShoulderFB1', 'lShoulderUD1',
        'lHipLR1', 'lHipFB1',
        'rShoulderFB1', 'rShoulderUD1',
        'rHipLR1', 'rHipFB1',
        'lElb1', 'rElb1',
        'lKnee1', 'rKnee1',
        
        #down position
        'headLR2', 'headFB2',
        'backLR2', 'backFB2',
        'lShoulderFB2', 'lShoulderUD2',
        'lHipLR2', 'lHipFB2',
        'rShoulderFB2', 'rShoulderUD2',
        'rHipLR2', 'rHipFB2',
        'lElb2', 'rElb2',
        'lKnee2', 'rKnee2',
        
        #up position
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
        
    return df #df.sample(frac=1).reset_index(drop=True) # shuffle dataframe and return

def dataframeforeval(totalreps, totalAngs):
    repsList=[] # is a list of reps. reps is a list of [top, bottom, top] angles
    print(f"\ntotal reps: {len(totalreps)}")
    for i in range(len(totalreps)):
        rowList = []
        for j in range(3):
            # concat angles of top, bottom, top into one list radiens
            if j == 0:
                rowList = totalAngs[j].tolist()
            else:
                rowList = rowList + totalAngs[j].tolist()
        repsList.append(rowList) #appends the list of (top, bottom, top) angles in raidens
    return repsList
                

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
    labels = df.pop('GoodForm').values.tolist()
    print(f"y(df.pop): {labels}. \nLen is :{len(labels)}\n")
    x = df.values.tolist()
    print(f"x(df.values.tolist): {x}.")
    X_train, X_test, y_train, y_test = train_test_split(x, labels, test_size=0.2, random_state=0)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    tf.random.set_seed(42)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(48, activation='relu'),
        #tf.keras.layers.Dense(48, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.binary_crossentropy,
        metrics=['accuracy',tf.keras.metrics.Precision(), 
                  tf.keras.metrics.TruePositives(),
                 tf.keras.metrics.FalseNegatives()]
    )  
    
    model.fit(X_train, y_train, epochs)
    return model, X_test, y_test

#
#
#
#
#
#
#
#
def do_ml(df):
    
    print(f"df.head: {df.head}")
    
    train, test = split(df)
    
    model, x_test, y_test = train_model(df)
    
    testy = test.pop('GoodForm').values.tolist()
    testx = test.values.tolist()
    
    test_loss, test_acc, test_prec, true_pos, false_neg = model.evaluate(x_test, y_test)
    print("MODEL ACCURACY: ", test_acc)#accuracy = how often the model predicted correctly
    #this is determined by #of correct predictions # of total predictions.
    # whereas accuracy deals with how close they are to the actual value of the measurement
    
    print("MODEL PRECISION: ",test_prec)#prescion = how often the model predicted the event to be positive and it turned out to be true
    #this is determined by # of true positives/ (# of true positives + # of false positives).
    # precision measures how near the calculated results are to one another
    
    print("MODEL LOSS(CROSS-ENTROPY LOSS): ", test_loss) #measures the performance of a classification model 
    #whose output is a probability value between 0 and 1. Cross-entropy loss increases as the 
    # predicted probability diverges from the actual label
    
    recall = true_pos/(true_pos + false_neg)
    print("Recall: ", recall) #measures how good the model is at correctly predicting positive classes
    #this is determined by # of true positives/(# of true positives + # of false negatives)
    if (test_prec + recall) > 0:
        f1 = 2*((test_prec * recall)/(test_prec + recall))
        print("F1-Score: ", f1)# is the harmonic mean of precision and recall
    # harmonic mean is an alternative metric for the more common arithmetic mean. It is often useful when computing an average rate.
    # F1 score = 2 * ((precision * recall)/ (precision + recall))
    
    #the F1 score gives equal weight to Precision and Recall
    #   A model will obtain a high F1 score if both Precision and Recall are high
    #   A model will obtain a low F1 score if both Precision and Recall are low
    #   A model will obtain a medium F1 score if one of Precision and Recall is low and the other is high
    return model


#this evaluate a user inputted cideo from key frame extraction
#it takes the already built model to evaluate the reps of the
#users videos. it than gives prediction of how accurate for
#each rep and prints it
#y_pred is the probability of every single output described in the model. 
#In many classification models you have a threshold. The common threshold is 0.5, 
# if the result is above of this, then is more likely to be “true”. On the contrary 
# if the result is below is more likely to be false
#
#parameters:
#           trained_model = an already trained model
#           df = is the list of reps. the reps are list of top bottom top angle in raidens
def vid_ml_eval(trained_model,df):
    #print(f"\nthe is the dataframe going into eval {df}. \n\nlength is {len(df)}")
    print(f"len of df: {len(df)}")
    y_pred = trained_model.predict(df)
    print(f"\n\nthis is the prediction for eaxh rep: {y_pred}")
    return True

#correct testing vids reps
#squatorfiangle.mp4 = 5 reps
#squatV1angle.mp4 = 5 reps
#squatV1angleland.mp4 = 5 reps
#squatV2angleland.mp4 = 5 reps

#incorrect testing vid reps
#deepsquatorfiangle.mp4 = 6 reps
#highsquatJCangle.mp4 = 5 reps
#deepsquatJCangle.mp4 = 5 reps
#curvedbacksquatorfiangle.mp4 = 5 reps
#curvedbacksquatJCangle.mp4 = 5 reps

#total reps 46, key frame sxtraction getting 2 extra reps