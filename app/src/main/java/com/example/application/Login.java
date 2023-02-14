package com.example.application;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class Login extends AppCompatActivity implements View.OnClickListener {

    Button buttonTrainee, buttonTrainer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        buttonTrainee = (Button) findViewById(R.id.tempTraineeHome);
        buttonTrainee.setOnClickListener(Login.this);

        buttonTrainer = (Button) findViewById(R.id.tempTrainerHome);
        buttonTrainer.setOnClickListener(Login.this);

    }

    @Override
    public void onClick(View v) {

        Intent i;

        switch (v.getId()) {
            //Go to trainee home
            case R.id.tempTraineeHome:
                i = new Intent(getApplicationContext(), TraineeHomePage.class);
                startActivity(i);
                break;
            //Go to trainer home
            case R.id.tempTrainerHome:
                i = new Intent(getApplicationContext(), TrainerHomePage.class);
                startActivity(i);
                break;
            default:
                break;
        }
    }
}
