package com.example.application;

import android.content.Context;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.TextView;

import java.text.DecimalFormat;
import java.util.ArrayList;

public class WorkoutsListAdapter implements ListAdapter {
    ArrayList<Workout> workoutsList;
    int user_id;
    Context context;

    public WorkoutsListAdapter(Context context, ArrayList<Workout> workoutsList, int user_id) {
        this.workoutsList=workoutsList;
        this.context=context;
        this.user_id = user_id;
    }

    public boolean areAllItemsEnabled() {
        return false;
    }

    @Override
    public boolean isEnabled(int position) {
        return true;
    }
    @Override
    public void registerDataSetObserver(DataSetObserver observer) {
    }
    @Override
    public void unregisterDataSetObserver(DataSetObserver observer) {
    }
    @Override
    public int getCount() {
        return workoutsList.size();
    }
    @Override
    public Object getItem(int position) {
        return position;
    }
    @Override
    public long getItemId(int position) {
        return position;
    }
    @Override
    public boolean hasStableIds() {
        return false;
    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Workout currWorkout=workoutsList.get(position);
        if(convertView==null) {
            LayoutInflater layoutInflater = LayoutInflater.from(context);
            convertView=layoutInflater.inflate(R.layout.workout_item, null);
            convertView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                }
            });
            TextView workoutNum=convertView.findViewById(R.id.txt_workoutNum);
            TextView workoutName=convertView.findViewById(R.id.txt_workoutName);
            TextView workoutDate=convertView.findViewById(R.id.txt_workoutDate);
            TextView workoutScore=convertView.findViewById(R.id.txt_workoutScore);

            // if workout list was empty
            if (currWorkout.getUser_id() == -1){
                workoutNum.setText("");

                String workoutTitle;
                if (SocketFunctions.user.isTrainer() & SocketFunctions.user.getId() != user_id){
                    workoutTitle = "No trainee workouts yet!";
                } else {
                    workoutTitle = "No workouts yet!";
                }

                workoutName.setText(workoutTitle);
                workoutDate.setText("");
                workoutScore.setText("");

            } else { // workouts has elements in it
                workoutNum.setText(String.valueOf(position + 1));

                String workoutTitle;
                if (SocketFunctions.user.isTrainer() & SocketFunctions.user.getId() != user_id){
                    workoutTitle = currWorkout.getUser_id() + ": " + currWorkout.getExercise_name();
                } else {
                    workoutTitle = currWorkout.getExercise_name();
                }

                workoutName.setText(workoutTitle);
                workoutDate.setText(currWorkout.getDate());
                DecimalFormat df = new DecimalFormat("##.##");
                Double currScore = currWorkout.getScore() * 100;
                workoutScore.setText("Score: " + df.format(currScore) + "%");
            }


        }
        return convertView;
    }
    @Override
    public int getItemViewType(int position) {
        return position;
    }
    @Override
    public int getViewTypeCount() {
        return workoutsList.size();
    }
    @Override
    public boolean isEmpty() {
        return false;
    }
}
