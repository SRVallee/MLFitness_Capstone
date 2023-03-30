package com.example.application;

import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.sendbird.uikit.SendBirdUIKit;
import com.sendbird.uikit.adapter.SendBirdUIKitAdapter;
import com.sendbird.uikit.interfaces.UserInfo;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.sql.Array;
import java.util.HashMap;
import java.util.Map;

public class Login extends AppCompatActivity implements View.OnClickListener {

    String USER_ID;
    String USER_NICKNAME;
    String USER_PROFILE_URL;
    String email, password;

    EditText usernameLogin;
    EditText passwordLogin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //Init fields in xml
        usernameLogin = findViewById(R.id.userNameEditText);
        passwordLogin = findViewById(R.id.passwordEditText);

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

        //Check email input
        email = usernameLogin.getText().toString();
        if(email.isEmpty()){
            alertDialog.setTitle("No email");
            alertDialog.setMessage("email is required");
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
        //Check email and password with database
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/login.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response){
                        Log.d("Response: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) { //or email already exists if when implemented
                                //Log.d("Response: ", response.toString());
                                SocketFunctions.user.setId(Integer.parseInt(jsonResponse.getString("user_id")));
                                SocketFunctions.user.setUserName(jsonResponse.getString("username"));
                                SocketFunctions.user.setEmail(jsonResponse.getString("email"));
                                SocketFunctions.user.setName(jsonResponse.getString("name"));
                                SocketFunctions.user.setTrainer(jsonResponse.getString("isTrainer").equals("1"));
                                SocketFunctions.apiKey = jsonResponse.getString("api_key");
                                Log.d("User id: ", "successful login");
                                Intent i;
                                int tempInt = SocketFunctions.user.getId();
                                USER_ID = String.valueOf(tempInt);
                                USER_NICKNAME = SocketFunctions.user.getName();
                                //Once profile pictures are implemented change this
                                USER_PROFILE_URL = "";
                                if (SocketFunctions.user.isTrainer()) {
                                    //User has entered all inputs and has indicated to signup as trainee
                                    //First connects to sendbird and makes account
                                    SendBirdUIKit.init(new SendBirdUIKitAdapter() {
                                        @Override
                                        public String getAppId() {
                                            return "011F57DA-BA7D-4DCF-96AC-12217F169139";  // The ID of the Sendbird application
                                        }

                                        @Override
                                        public String getAccessToken() {
                                            return "";
                                        }

                                        @Override
                                        public UserInfo getUserInfo() {
                                            return new UserInfo() {
                                                @Override
                                                public String getUserId() {
                                                    return USER_ID; // The userID of the user you wish to log in as
                                                }

                                                @Override
                                                public String getNickname() {
                                                    return USER_NICKNAME; // The nickname of the user you wish to log in as
                                                }

                                                @Override
                                                public String getProfileUrl() {
                                                    return USER_PROFILE_URL;
                                                }
                                            };
                                        }
                                    }, getApplicationContext());// If errors use this and move
                                    //Goes to homepage
                                    i = new Intent(getApplicationContext(), TrainerHomePage.class);
                                    startActivity(i);
                                    finish();
                                } else {
                                    //User has entered all inputs and has indicated to signup as trainee
                                    //First connects to sendbird and makes account
                                    SendBirdUIKit.init(new SendBirdUIKitAdapter() {
                                        @Override
                                        public String getAppId() {
                                            return "011F57DA-BA7D-4DCF-96AC-12217F169139";  // The ID of the Sendbird application
                                        }

                                        @Override
                                        public String getAccessToken() {
                                            return "";
                                        }

                                        @Override
                                        public UserInfo getUserInfo() {
                                            return new UserInfo() {
                                                @Override
                                                public String getUserId() {
                                                    return USER_ID; // The userID of the user you wish to log in as
                                                }

                                                @Override
                                                public String getNickname() {
                                                    return USER_NICKNAME; // The nickname of the user you wish to log in as
                                                }

                                                @Override
                                                public String getProfileUrl() {
                                                    return USER_PROFILE_URL;
                                                }
                                            };
                                        }
                                    }, getApplicationContext());// If errors use this and move
                                    //Goes to homepage
                                    //makeUser(username, name, email, passwordOne, isTrainer);
                                    i = new Intent(getApplicationContext(), TraineeHomePage.class);
                                    startActivity(i);
                                    finish();
                                }
                            }
                            else{
                                alertDialog.setTitle("Error!");
                                alertDialog.setMessage(jsonResponse.getString("status"));
                                alertDialog.show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("User id: ", error.getLocalizedMessage());
            }
        }) {
            protected Map<String, String> getParams() {
                Map<String, String> paramV = new HashMap<>();
                paramV.put("email", email);
                paramV.put("password", password);
                return paramV;
            }
        };
        queue.add(stringRequest);
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
