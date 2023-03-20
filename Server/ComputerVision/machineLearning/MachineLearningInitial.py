import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from keras.preprocessing.text import Tokenizer
from keras.utils.vis_utils import plot_model
from pathlib import Path
from keras_visualizer import visualizer
import os
import pickle
#refrence between
# 1   head angle = [0,1]
# 2   body angle = [2,3]
# 3   left shoulder = [4,5]
# 4   left hip = [6,7]
# 5   right shoulder = [8,9]
# 6   right hip = [10,11]
# 7   left elbow = [12]
# 8   left knee = [13]
# 9   right elbow = [14]
# 10  right knee = [15]
#these are all the points of the body. 49 points for 1 rep and form. UD = UP down, FB = Face Back
#can onnly exclude a max of 6 joints. each elbow and knee is counted as one. Everything else is 
# counted as 2 

# use scaler or not
USE_SCALER = False

DEBUG = True

COLS = [
        #up postion
        'headLR1', 'headFB1',#[0,1]
        'backLR1', 'backFB1',#[2,3]
        'lShoulderFB1', 'lShoulderUD1',#[4,5]
        'lHipLR1', 'lHipFB1',#[6,7]
        'rShoulderFB1', 'rShoulderUD1',#[8,9]
        'rHipLR1', 'rHipFB1', #[10,11]
        'lElb1',  'lKnee1', #[12],[13]
        'rElb1', 'rKnee1', #[14],[15]
        
        #down position
        'headLR2', 'headFB2',#
        'backLR2', 'backFB2',#
        'lShoulderFB2', 'lShoulderUD2',#
        'lHipLR2', 'lHipFB2',#
        'rShoulderFB2', 'rShoulderUD2',#
        'rHipLR2', 'rHipFB2',#
        'lElb2', 'lKnee2',#
        'rElb2', 'rKnee2',#
        
        #up position
        'headLR3', 'headFB3',#
        'backLR3', 'backFB3',#
        'lShoulderFB3', 'lShoulderUD3',#
        'lHipLR3', 'lHipFB3',#
        'rShoulderFB3', 'rShoulderUD3',#
        'rHipLR3', 'rHipFB3',#
        'lElb3', 'lKnee3',#
        'rElb3', 'rKnee3',#
        'GoodForm'
    ]
#
def repsToDataframe(totalReps, totalAngs, goodOrBad, rmCols=[]):
    
    repsList=[]
    colsList = COLS.copy() # copy list of all possible cols names
    colNamesRemoved = False
    for i in range(len(totalReps)): # for each video
        print(f"rep i in totalreps[i]: {totalReps[i]}")
        for rep in totalReps[i]: # for each rep in video
            if None in rep:
                continue
            else:
                rowList = []
                for j in range(3): # for keyframes in rep
                    # concat angles of top, bottom, top into one list
                    
                    currList = totalAngs[i][rep[j]].tolist() # all angles for keyframe
                    if rmCols: # if there are cols to delete
                        rmCols.sort(reverse=True) # desceneding
                        for num in rmCols: 
                            if not colNamesRemoved:
                                colIndex = num + (2-j) * 16
                                del colsList[colIndex] # delete exclude column name
                            del currList[num] # delete col index
                            
                    if j == 0: # first 16
                        rowList = currList
                    else: # next 32
                        rowList = rowList + currList
                        
                colNamesRemoved = True
                # add if is a good rep (for training)
                
                rowList.append(goodOrBad)
                    
                # append rep angles to reps list
                repsList.append(rowList) 
    #convert to dataframe
    df = pd.DataFrame(repsList, columns=colsList)
        
    return df #df.sample(frac=1).reset_index(drop=True) # shuffle dataframe and return

#
def dataframeforeval(totalReps, totalAngs, rmCols=[]):
    repsList=[] # is a list of reps. reps is a list of [top, bottom, top] angles
    print(f"\ntotal reps: {len(totalReps)}")
    print(f"\ntotal ang lengths: {len(totalAngs)}")
    for rep in totalReps: # for each rep in video
        if None in rep or len(rep) <5:
            continue
        else:
            rowList = []
            for j in range(3): # for keyframes in rep
                # concat angles of top, bottom, top into one list
                
                currList = totalAngs[rep[j]].tolist() # all angles for keyframe
                if rmCols: # if there are cols to delete
                    rmCols.sort(reverse=True) # desceneding
                    for num in rmCols: 
                        # colIndex = num + (2-j) * 16
                        # del colsList[colIndex] # delete exclude column name
                        del currList[num] # delete col index
                        
                if j == 0: # first 16
                    rowList = currList
                else: # next 32
                    rowList = rowList + currList
        repsList.append(rowList) #appends the list of (top, bottom, top) angles in raidens
    return repsList
                
#
def split(df, ratio=0.2):
    train = pd.DataFrame(columns=COLS) 
    test = pd.DataFrame(columns=COLS)
    split = int(df.shape[0]*ratio)
    
    test = df.iloc[0:split]
    train = df.iloc[split:df.shape[0]]

    return train, test


# Manual method to remove outliers
def removeOutliers(df, y_df=None, minStdDev=0.2, thresholdMult=1.5, multipleOut=False, multiOutThreshold=3):
    dataframe = df.copy()
    y_dataframe = None
    if y_df:
        y_dataframe = y_df.copy()
        
    boolArr = np.full(dataframe.shape, True)
    
    for i in range(dataframe.shape[1]): # columns
        if np.std(dataframe.iloc[:,i]) < minStdDev:
            # if variance in column data is small, skip column outlier removal
            # help prevent too many row being removed
            continue
        
        q75 = np.percentile(dataframe.iloc[:,i], 75)
        q25 = np.percentile(dataframe.iloc[:,i], 25)
        cutOff = thresholdMult * (q75-q25) # multiply interquartile range
        
        for j in range(dataframe.shape[0]-1, -1, -1): #rows in column *from the bottom*
            #iterate fom the bottom so removing doesn't mess up index
            currVal = dataframe.iloc[j,i]
            # less than bottom cut off or greater than top cutoff
            if currVal < q25 - cutOff or currVal > q75 + cutOff:
                if multipleOut:
                    boolArr[j][i] = False
                else:
                    # dump row with outlier
                    dataframe = dataframe.drop(j)
                    dataframe.reset_index(drop=True, inplace=True)
                    if y_dataframe:
                        del y_dataframe[i]
    
    # if data should require multiple outliers in one row
    if multipleOut:
        # rows starting from bottom
        for i in range(dataframe.shape[0]-1, -1, -1):
            count = 0
            for inlier in boolArr[i]:
                if not inlier: # outlier
                    count = count + 1
                if count >= multiOutThreshold:
                    # if count reaches threshold, drop row, and go to next
                    dataframe = dataframe.drop(i)
                    dataframe.reset_index(drop=True, inplace=True)
                    if y_dataframe:
                        del y_dataframe[i]
                    break
    
    if y_dataframe:
        return dataframe, y_dataframe
    else:
        return dataframe


# Use sklearn to automatically detect and remove outliers
def autoRemoveOutliers(x_train, y_train):
    '''
    https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html
    https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/
    '''
    lof = LocalOutlierFactor(leaf_size=40)
    inAndOutliers = lof.fit_predict(x_train)
    
    # inliers are 1, outliers are -1
    mask = inAndOutliers != -1 # grab only inliers
    outliers = inAndOutliers != 1
    
    print(f"outliers:\n{x_train[outliers,:]}")
    
    new_x_train = x_train[mask,:]
    new_y_train = y_train[mask]
    
    return new_x_train, new_y_train

#
def train_model(df, importantAngles, modelName, rounds=50, outlierAggresive=True):
    
    labels = df.pop('GoodForm').values.tolist()
    print(f"y(df.pop): {labels}. \nLen is :{len(labels)}\n")
    #print(f"COLS at index 13: {COLS[13]}, COLS at index {13+16}: {COLS[13+16]}COLS at index {13+32}: {COLS[13+32]}")

    shape = df.shape
    print(f"this is the shape: {shape}")
    features_amnt = shape[1]
    print(f"features_amnt: {features_amnt}")
    input_list = []
    for repper in range(3):
        for ang in importantAngles:
            input_list.append(ang+(16*repper))
            
    # x = df.values.tolist()
    # new_df = [[x for i, x in enumerate(n) if i in input_list] for n in x]
    # for df_list in x:
    #     rep_imp_angles = []
    #     for rep_angles in input_list:
    #         rep_imp_angles.append(df_list[rep_angles])
    #     new_df.append(rep_imp_angles)
    #new_df is inclusion of specific points df is for the whole thing
    X_train, X_test, y_train, y_test = train_test_split(df, labels, test_size=0.2, random_state=0)
    
    if DEBUG:
        indecies = pd.Series(range(X_train.shape[0], X_test.shape[0] + X_train.shape[0], 1))
        X_test_newindex = X_test.set_index(indecies)
        merged_df = pd.concat([X_train, X_test_newindex])
        
        currFile = os.path.dirname(__file__)
        parent = os.path.dirname(currFile)
        
        filename = str(parent) + "\\dataframes\\" + modelName + "_tt.csv"
        merged_df.to_csv(filename, index=False)
    
    print(f"Shape of training set before outlier removal:{X_train.shape}")
    
    X_train.reset_index(drop=True, inplace=True)
    X_test.reset_index(drop=True, inplace=True)
    
    # Scale data
    scaler = StandardScaler()
    if USE_SCALER:
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
    # manual, aggressive outlier removal
    if outlierAggresive:
        new_x_train, new_y_train = removeOutliers(X_train, y_train, 
                                                  thresholdMult=2, 
                                                  multipleOut=True, 
                                                  multiOutThreshold=3)
        # for debugging, can just assign directly instead
        # X_train = new_x_train
        # y_train = new_y_train
    
    # Convert datasets to numpy
    X_train_np = X_train.to_numpy()
    # X_train_np = np.array(X_train)
    y_train_np = np.array(y_train)
    X_test_np  = X_test.to_numpy()
    # X_test_np  = np.array(X_test)
    y_test_np  = np.array(y_test)
    
    # auto, soft outlier removal
    if not outlierAggresive:
        new_x_train, new_y_train = autoRemoveOutliers(X_train_np, y_train_np)
        # for debugging, can just assign directly instead
        X_train_np = new_x_train
        y_train_np = new_y_train
        

    print(f"Shape of training set after outlier removal:{X_train_np.shape}")
    
    if DEBUG:
        indecies = pd.Series(range(X_train.shape[0], X_test.shape[0] + X_train.shape[0], 1))
        X_test_newindex = X_test.set_index(indecies)
        merged_df = pd.concat([X_train, X_test_newindex])
        
        currFile = os.path.dirname(__file__)
        parent = os.path.dirname(currFile)
        
        filename = str(parent) + "\\dataframes\\" + modelName + "_tt_Rem.csv"
        merged_df.to_csv(filename, index=False)
    
    #tf.random.set_seed(42)

    # Set model
    model = tf.keras.Sequential([
        #tf.keras.Input(shape=(None,features_amnt)),
        tf.keras.layers.Dense(48, activation='relu'),
        tf.keras.layers.Dense(48, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.binary_crossentropy,
        metrics=['accuracy',tf.keras.metrics.Precision(), 
                  tf.keras.metrics.TruePositives(),
                  tf.keras.metrics.FalsePositives(),
                  tf.keras.metrics.FalseNegatives()]
    )
    
    model.fit(x=X_train_np, y=y_train_np, epochs = rounds)
    print(model.summary())
    #tf.keras.utils.plot_model(model, to_file='model_1.png',show_shapes=True)
    currDir = str(os.path.dirname(__file__))
    model_path = str(currDir) + "\\ML_Trained_Models\\"+ str(modelName)+"_trained"
    print(model_path)
    model.save(model_path)
    
    # dump scaler
    if USE_SCALER:
        scaler_path = str(currDir) +"\\scalers\\"+ str(modelName)+"_scaler.pkl"
        pickle.dump(scaler, open(scaler_path, 'wb'))
    
    return model, X_test_np, y_test_np

#
def do_ml(df, importantAngles,modelName):
    
    # print(f"df.head: {df.head}")
    
    model, x_test, y_test = train_model(df,importantAngles,modelName, outlierAggresive=True)
    
    test_loss, test_acc, test_prec, true_pos, true_neg, false_neg = model.evaluate(x_test, y_test)
    print("MODEL ACCURACY: ", test_acc)#accuracy = how often the model predicted correctly
    #this is determined by #of correct predictions # of total predictions.
    # whereas accuracy deals with how close they are to the actual value of the measurement
    
    print("MODEL PRECISION: ",test_prec)#prescion = how often the model predicted the event to be positive and it turned out to be true
    #this is determined by # of true positives/ (# of true positives + # of false positives).
    # precision measures how near the calculated results are to one another
    
    print("MODEL LOSS(CROSS-ENTROPY LOSS): ", test_loss) #measures the performance of a classification model 
    #whose output is a probability value between 0 and 1. Cross-entropy loss increases as the 
    # predicted probability diverges from the actual label
    if ((true_pos + false_neg) > 0):
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



#this evaluate a user inputted video from key frame extraction
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
#
#Return:
#           y_pred_list, acutal_frame_num
def vid_ml_eval(modelName, trained_model, df, extracted, reps,imp_angles):
    #print(f"\nthe is the dataframe going into eval {df}. \n\nlength is {len(df)}")
    print(f"len of df: {len(df)}")
    currDir = str(os.path.dirname(__file__))
    
    new_df = np.array(df)
    y_pred_list =[]
    acutal_frame_num = []
    #scaler
    if USE_SCALER:
        scaler_path = str(currDir) +"\\scalers\\"+ str(modelName)+"_scaler.pkl"
        acutal_frame_num = [] # this was for the scalar but scalar causes the points to be inaccurrate
        scaler = pickle.load(open(scaler_path,'rb'))
        new_df = scaler.transform(new_df)
    
    print(trained_model.summary())
    print(currDir)
    # TODO: uncomment \/
    # tf.keras.utils.plot_model(trained_model, to_file= str(vidsDir)+"\\" + str(modelName)+"_diagram.png",show_shapes=True)
    visualizer(trained_model, filename= str(currDir) + str(modelName)+"_neural_network.png", view= False)
    y_pred = trained_model.predict(x = new_df)
    print(f"\n\nthis is the prediction for each rep: {y_pred}")
    print(f"this is the actual frame numbers [up, down, up, degree]: {reps}")
    # for confidence in range(reps):
    #     y_pred_list.append(confidence[1])
    return reps, acutal_frame_num

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