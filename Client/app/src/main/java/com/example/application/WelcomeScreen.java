package com.example.application;

import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.Settings;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class WelcomeScreen extends AppCompatActivity implements View.OnClickListener{

    Button button1, button2, button3, button4;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome_screen);

        button1 = (Button) findViewById(R.id.loginButtonWelcome);
        button1.setOnClickListener(WelcomeScreen.this);

        button2 = (Button) findViewById(R.id.signUpButtonWelcome);
        button2.setOnClickListener(WelcomeScreen.this);

        //button3 = (Button) findViewById(R.id.tempB1);
        //button3.setOnClickListener(WelcomeScreen.this);

        //button4 = (Button) findViewById(R.id.tempB2);
        //button4.setOnClickListener(WelcomeScreen.this);

        if (Build.VERSION.SDK_INT >= 30){
            if (!Environment.isExternalStorageManager()){
                Intent getpermission = new Intent();
                getpermission.setAction(Settings.ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION);
                startActivity(getpermission);
            }
        }

    }

    @Override
    public void onClick(View v) {

        Intent i;

        switch (v.getId()) {
            //Go to login
            case R.id.loginButtonWelcome:
                i = new Intent(getApplicationContext(), Login.class);
                startActivity(i);
                break;
            //Go to signup, goes to role select first but then to signup activity
            case R.id.signUpButtonWelcome:
                i = new Intent(getApplicationContext(), SignUp.class);
                startActivity(i);
                break;
            //Trainee temp
            //case R.id.tempB1:
            //    i = new Intent(getApplicationContext(), TraineeHomePage.class);
            //    startActivity(i);
            //    break;
            //Trainer temp
            //case R.id.tempB2:
            //    i = new Intent(getApplicationContext(), TrainerHomePage.class);
            //    startActivity(i);
            //    break;
            default:
                break;
        }
    }
}
