package com.example.application;

import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.VideoView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;

import java.util.ArrayList;

public class TrainerFeedback extends AppCompatActivity {

    private EditText feetBack;

    private TextView workoutTitle, reviewerName, feedback;

    private VideoView videoFeedback;

    private int workoutID;
    private ArrayList<Workout> workouts = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainer_feetback);

        Intent intent = getIntent();
        Bundle bundle = intent.getExtras();
        if (bundle!=null){
            workoutID = (int) bundle.get("workout_id");
        }

        workoutTitle = findViewById(R.id.feetBackTitle);
        reviewerName = findViewById(R.id.workout_feedback_by);
        feedback = findViewById(R.id.workout_feedback_text);
        videoFeedback = findViewById(R.id.workout_video);

    }

    @Override
    public void onBackPressed() {
        //Go to homepage
        Intent i = new Intent(getApplicationContext(), TrainerHomePage.class);
        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
        startActivity(i);
        finish();
        super.onBackPressed();
    }
}
