import sys
from workoutRecognition import evaluate_video

# This is to compare an uploaded video to the trained model from the command 
# line. Run as:
#   python3 DatabaseEval.py [workout_name] [path_to_video]

# E
def main():
    args = sys.argv[1:]
    
    if len(args) != 3:
        print("Must enter a user ID, exercise name/ID, and path to video")
        sys.exit(1)
        
    else:
        if args[0] == '' or args[1] == '':
            print("Workout name and video path must not be empty")
            sys.exit(2)
        
        else:
            # should give info to DB and return ID inserted into workout
            workoutID = evaluate_video(args[0], args[1], args[2])
            
            # should be able to get in PHP with:
            # $command = escapeshellcmd('/usr/custom/test.py');
            # $output = shell_exec($command);
            sys.stderr.write(str(workoutID))
            sys.exit(0)
            

if __name__ == "__main__":
    main()