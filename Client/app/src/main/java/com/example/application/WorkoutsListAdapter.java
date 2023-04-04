package com.example.application;

import android.content.Context;
import android.database.DataSetObserver;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.TextView;

import java.util.ArrayList;

public class WorkoutsListAdapter implements ListAdapter {
    ArrayList<Workout> workoutsList;
    Context context;

    public WorkoutsListAdapter(Context context, ArrayList<Workout> workoutsList) {
        this.workoutsList=workoutsList;
        this.context=context;
    }

    public boolean areAllItemsEnabled() {
        return false;
    }

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
            TextView workoutName=convertView.findViewById(R.id.txt_workoutName);

            workoutName.setText(currWorkout.);

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
