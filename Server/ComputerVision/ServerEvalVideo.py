import sys
from workoutRecognition import evaluate_video

# This is to compare an uploaded video to the trained model from the command 
# line. Run as:
#   python3 DatabaseEval.py [workout_name] [path_to_video]


def main():
    args = sys.argv[1:]
    
    if len(args) != 2:
        print("Must enter a workout name and path to video")
        sys.exit(1)
        
    else:
        if args[0] == '' or args[1] == '':
            print("Workout name and video path must not be empty")
            sys.exit(2)
        
        else:
            evaluate_video(args[0], args[1])
    

if __name__ == "__main__":
    main()