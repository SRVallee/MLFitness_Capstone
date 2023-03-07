package com.example.application;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

public class Login extends AppCompatActivity implements View.OnClickListener {

    String username, password;

    EditText usernameLogin;
    EditText passwordLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //Init fields in xml
        usernameLogin = findViewById(R.id.userNameEditText);
        passwordLogin = findViewById(R.id.passwordEditText);
        passwordLogin.setTransformationMethod(new AsteriskPasswordTransformationMethod());

    }

    /***
     * Attempts to login using the user inputted data
     * ***/
    public void attemptLogin (View view) {

        //Check both fields have input
        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

        //Check username input
        username = usernameLogin.getText().toString();
        if(username.isEmpty()){
            alertDialog.setTitle("No Username");
            alertDialog.setMessage("Username is required");
            alertDialog.show();
            return;
        }

        //Check password input
        password = passwordLogin.getText().toString();
        if(password.isEmpty()){
            alertDialog.setTitle("No Password");
            alertDialog.setMessage("Password is Required");
            alertDialog.show();
            return;
        }

        //At this point have user input, thus check with server if the values entered are correct
        //Check username and password with database

        /*
        if(verifyLogin(username, password)) {
            //Username and password are valid
            //Check if user is trainee or trainer and then go to their respective home page
            Intent i;
            if(userIsTrainer(username)) {
                //User is trainer
                i = new Intent(getApplicationContext(), TrainerHomePage.class);
            } else {
                //User is trainee
                i = new Intent(getApplicationContext(), TraineeHomePage.class);
            }
            startActivity(i);
            this.finish();
        } else {
            //Username and password are not valid
            alertDialog.setTitle("Error");
            alertDialog.setMessage("Invalid username or password");
            alertDialog.show();
            return;
        }
        */
    }

    /***
     * Goes to forgot login creds page
     * ***/
    public void forgotPassword (View view) {

        Intent i;
        //Go to trainee home
        i = new Intent(getApplicationContext(), ForgotPassword.class);
        startActivity(i);
        this.finish();

    }


    /***
     * This function is just a temp func to access the application without logging in
     * ***/
    @Override
    public void onClick(View v) {
        Intent i;
        switch (v.getId()) {
            default:
                break;
        }
    }
}
