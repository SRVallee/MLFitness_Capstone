package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.navigation.NavigationView;
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TraineeProfile extends AppCompatActivity{

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        if (drawerToggle.onOptionsItemSelected(item)) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainee_profile);

        //Set objects in the page
        //Once db is implemented change from test/example cases to the version that get the data from the db

        //Init fields in xml
        TextView trainee_profile_username_textview = (TextView) findViewById(R.id.userNameTraineeProfile);
        TextView trainee_profile_email_textview = (TextView) findViewById(R.id.userEmailTraineeProfile);

        ImageView userProfilePicture = (ImageView) findViewById(R.id.profile_picture);

        //Assigns values to the fields in the xml
        //String trainee_profile_username = user.getUsername();
        String trainee_profile_username = SocketFunctions.user.getUserName();
        trainee_profile_username_textview.setText(trainee_profile_username);
        //String trainee_profile_email = user.getEmail();
        String trainee_profile_email = SocketFunctions.user.getEmail();
        trainee_profile_email_textview.setText(trainee_profile_email);

        //Check line to get from db


        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
        drawerToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        if (SocketFunctions.user.isTrainer() == false) {
            String name = SocketFunctions.user.getName();
            TextView textView = findViewById(R.id.TraineeProfileTitle);
            textView.setText(name);
            navigationView.getMenu().findItem(R.id.trainers).setVisible(true);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(false);
        }
        else{
            Intent trainee_profile = getIntent();
            User trainee_obj = (User) trainee_profile.getSerializableExtra("traineeObj");
            navigationView.getMenu().findItem(R.id.trainers).setVisible(false);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(true);
            try{
                if(trainee_obj.hasPfp()){
                    userProfilePicture.setImageBitmap(trainee_obj.getPfp());
                }else{
                    Picasso.get().load("http://162.246.157.128/MLFitness/pfps/"+ trainee_obj.getId() +".jpg").into(userProfilePicture);
                    Drawable pfp = userProfilePicture.getDrawable();
                    trainee_obj.setPfp(Bitmap.createBitmap(pfp.getIntrinsicWidth(), pfp.getIntrinsicHeight(), Bitmap.Config.ARGB_8888));
                }
            }catch (Exception e){
                int trainee_profile_image = R.drawable.ic_baseline_tag_faces_24;
                userProfilePicture.setImageResource(trainee_profile_image);
            }
            TextView name = findViewById(R.id.TraineeProfileTitle);
            TextView username = findViewById(R.id.userNameTraineeProfile);
            TextView email = findViewById(R.id.userEmailTraineeProfile);
            name.setText(trainee_obj.getName());
            username.setText(trainee_obj.getUserName());
            email.setText(trainee_obj.getEmail());
            is_subbed(trainee_obj);
            onclickfriends(trainee_obj);

        }
        invalidateOptionsMenu();
        invalidateMenu();
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {

                switch (item.getItemId()) {
                    case R.id.home: {
                        //Go to homepage
                        Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.workouts: {
                        //Go to workouts
                        Intent i = new Intent(getApplicationContext(), TraineeWorkouts.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.message: {
                        //Go to message
                        Intent i = new Intent(getApplicationContext(), TraineeMessages.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        //finish();
                        drawerLayout.closeDrawer(GravityCompat.START);
                        break;
                    }
                    case R.id.setting: {
                        //Go to setting
                        Intent i = new Intent(getApplicationContext(), TraineeSettings.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.friends: {
                        //Go to friends
                        Intent i = new Intent(getApplicationContext(), FriendsPage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.profile: {
                        //Already selected
                        if(SocketFunctions.user.isTrainer()){
                            Intent i = new Intent(getApplicationContext(), TrainerProfile.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                            startActivity(i);
                            finish();
                            break;
                        }else {
                            drawerLayout.closeDrawer(GravityCompat.START);
                        }
                        break;
                    }
                    case R.id.logout: {
                        //Add a confirmation pop up

                        //Once completed logout/remove locally stored user cred

                        //End all activities and go to welcome screen
                        Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                        startActivity(intent);
                        break;
                    }
                    default: {
                        drawerLayout.closeDrawer(GravityCompat.START);
                    }
                }
                return false;
            }
        });
    }
    // this is for switching around what the button is for either adding friend removing friend or editing
    //profile
    private void onclickfriends(User trainee_obj) {
        ConstraintLayout trainee_constraint = findViewById(R.id.trainee_constraint);
        ImageView add_friend = findViewById(R.id.add_friend_trainee);
        ImageView unfriend = findViewById(R.id.sub_friend_trainee);
        ImageView edit_profile = findViewById(R.id.edit_trainee_profile_button);
        if (add_friend.getVisibility() == View.VISIBLE){
            add_friend.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Context context = getApplicationContext();
                    RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
                    String url = "http://162.246.157.128/MLFitness/add_relationship.php";

                    StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                            new Response.Listener<String>() {
                                //this is async reyes didn't tell me NO ONE TOLD ME
                                //this runs on a different thread than the main
                                @Override
                                public void onResponse(String response) {
                                    ArrayList<User> users = new ArrayList<>();
                                    Log.d("Response friended: ", response.toString());
                                    try {
                                        JSONObject jsonResponse = new JSONObject(response);
                                        String status = jsonResponse.getString("status");
                                        if (status.equals("success")) {
                                            Log.d("trainee friend array: ", jsonResponse.getString("relationships"));
                                            JSONArray relationship = new JSONArray(jsonResponse.getString("relationships"));
                                            if (relationship.length() == 0){
                                                ImageView add_friend = findViewById(R.id.add_friend_trainee);
                                                ImageView unfriend = findViewById(R.id.sub_friend_trainee);
                                                ImageView edit_button = findViewById(R.id.edit_trainee_profile_button);
                                                add_friend.setVisibility(View.VISIBLE);
                                                unfriend.setVisibility(View.GONE);
                                                edit_button.setVisibility(View.GONE);


                                            }

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
                            paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                            paramV.put("apiKey", SocketFunctions.apiKey);
                            paramV.put("id2",String.valueOf(trainee_obj.getId()));
                            Log.d("THE IDS", "getParams: "+String.valueOf(SocketFunctions.user.getId())+" pain " +String.valueOf(trainee_obj.getId()));
                            if(SocketFunctions.user.isTrainer() == true){
                                paramV.put("type", "1");
                            }
                            else{
                                paramV.put("type","0");
                            }
                            return paramV;
                        }
                    };
                    queue.add(stringRequest);
                }
            });
        } else if (unfriend.getVisibility() == View.VISIBLE) {
            unfriend.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                }
            });
        } else if (edit_profile.getVisibility() == View.VISIBLE) {

            edit_profile.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                }
            });
        }
    }

    private void is_subbed(User trainee_obj) {
        Context context = getApplicationContext();
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_relationships.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    //this is async reyes didn't tell me NO ONE TOLD ME
                    //this runs on a different thread than the main
                    @Override
                    public void onResponse(String response) {
                        ArrayList<User> users = new ArrayList<>();
                        Log.d("Response subbed: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                Log.d("this trainee friends: ", jsonResponse.getString("relationships"));
                                JSONArray relationship = new JSONArray(jsonResponse.getString("relationships"));
                                if (relationship.length() == 0){
                                    ImageView add_friend = findViewById(R.id.add_friend_trainee);
                                    ImageView unfriend = findViewById(R.id.sub_friend_trainee);
                                    ImageView edit_button = findViewById(R.id.edit_trainee_profile_button);
                                    add_friend.setVisibility(View.VISIBLE);
                                    unfriend.setVisibility(View.GONE);
                                    edit_button.setVisibility(View.GONE);


                                }

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
                paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                paramV.put("apiKey", SocketFunctions.apiKey);
                paramV.put("id2",String.valueOf(trainee_obj.getId()));

                return paramV;
            }
        };
        queue.add(stringRequest);
    }

    public void goToEdit(View view) {
        Intent i;
        i = new Intent(getApplicationContext(), TraineeEditProfile.class);
        startActivity(i);
        finish();
    }

    @Override
    public void onBackPressed() {

        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            drawerLayout.closeDrawer(GravityCompat.START);
        } else {
            //Go to homepage
            Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
            startActivity(i);
            finish();
            super.onBackPressed();
        }
    }
}