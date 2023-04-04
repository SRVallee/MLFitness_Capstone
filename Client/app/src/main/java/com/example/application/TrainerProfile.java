package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
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

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TrainerProfile extends AppCompatActivity {

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;

    private Boolean exit = false;
    private long pressedTime;

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
        setContentView(R.layout.activity_trainer_profile);
        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        Log.d("socket function", "onCreate in profile: "+SocketFunctions.user.isTrainer());

        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
        drawerToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        // trainer page checks if user is trainer if not than thgis is for user to find trainer
        if (SocketFunctions.user.isTrainer() == false) {
            Intent trainer_profile = getIntent();
            ObjectTrainer trainer_obj = (ObjectTrainer) trainer_profile.getSerializableExtra("trainerObj");
            TextView trainer_name = findViewById(R.id.trainerProfileTitle);
            trainer_name.setText(trainer_obj.getTrainer_name());
            navigationView.getMenu().findItem(R.id.trainers).setVisible(true);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(false);
            is_subbed(trainer_obj);
        }
        else{
            String name = SocketFunctions.user.getName();
            TextView trainer_name = findViewById(R.id.trainerProfileTitle);
            trainer_name.setText(name);
            navigationView.getMenu().findItem(R.id.trainers).setVisible(false);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(true);
            ImageView add_friend = findViewById(R.id.add_friend_trainee);
            ImageView unfriend = findViewById(R.id.sub_friend_trainee);
            ImageView edit_button = findViewById(R.id.edit_trainee_profile_button);
            add_friend.setVisibility(View.GONE);
            unfriend.setVisibility(View.GONE);
            edit_button.setVisibility(View.VISIBLE);

        }
        invalidateOptionsMenu();
        invalidateMenu();
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {

                switch (item.getItemId()) {
                    case R.id.home: {
                        //Go to home
                        if(!SocketFunctions.user.isTrainer()){
                            Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                            startActivity(i);
                            finish();
                            break;
                        }else {
                            Intent i = new Intent(getApplicationContext(), TrainerHomePage.class);
                            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                            startActivity(i);
                            finish();
                            break;
                        }
                    }
                    case R.id.workouts: {
                        //Go to upload
                        Intent i = new Intent(getApplicationContext(), TrainerUpload.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.message: {
                        //Go to messages
                        Intent i = new Intent(getApplicationContext(), TraineeMessages.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        //finish();
                        drawerLayout.closeDrawer(GravityCompat.START);
                        break;
                    }
                    case R.id.setting: {
                        //Go to setting
                        Intent i = new Intent(getApplicationContext(), TrainerSettings.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.trainees: {
                        //Go to trainees
                        Intent i = new Intent(getApplicationContext(), TrainerTraineeProfile.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.trainers:{
                        Intent i = new Intent(getApplicationContext(), TraineeTrainerProfile.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.friends: {
                        //Go to friends
                        Intent i = new Intent(getApplicationContext(), TrainerFriends.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.profile: {
                        //Already selected
                        if(!SocketFunctions.user.isTrainer()){
                            Intent i = new Intent(getApplicationContext(), TraineeProfile.class);
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

    private void is_subbed(ObjectTrainer trainer_obj) {
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
                                    ImageView add_friend = findViewById(R.id.add_friend_trainer);
                                    ImageView unfriend = findViewById(R.id.sub_friend_trainer);
                                    ImageView edit_button = findViewById(R.id.edit_profile_trainer);
                                    add_friend.setVisibility(View.VISIBLE);
                                    unfriend.setVisibility(View.GONE);
                                    edit_button.setVisibility(View.GONE);
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
                                                            Log.d("before if", "da fuq ");
                                                            if (response.toString().equals("success")) {
                                                                ImageView add_friend = findViewById(R.id.add_friend_trainer);
                                                                ImageView unfriend = findViewById(R.id.sub_friend_trainer);
                                                                ImageView edit_button = findViewById(R.id.edit_profile_trainer);
                                                                add_friend.setVisibility(View.GONE);
                                                                Log.d("TO FRONT", "onResponse: "+"made it");
                                                                unfriend.setVisibility(View.VISIBLE);
                                                                unfriend.bringToFront();
                                                                edit_button.setVisibility(View.GONE);
                                                                is_subbed(trainer_obj);
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
                                                    //trainee
                                                    paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                                                    paramV.put("apiKey", SocketFunctions.apiKey);
                                                    //trainer
                                                    paramV.put("id2",String.valueOf(trainer_obj.getId()));
                                                    Log.d("THE IDS", "getParams: "+String.valueOf(SocketFunctions.user.getId())+" pain " +String.valueOf(trainer_obj.getId()));
                                                    if(SocketFunctions.user.isTrainer() == false){
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


                                }
                                else{
                                    ImageView add_friend = findViewById(R.id.add_friend_trainer);
                                    ImageView unfriend = findViewById(R.id.sub_friend_trainer);
                                    ImageView edit_button = findViewById(R.id.edit_profile_trainer);
                                    add_friend.setVisibility(View.GONE);
                                    unfriend.setVisibility(View.VISIBLE);
                                    edit_button.setVisibility(View.GONE);
                                    unfriend.setOnClickListener(new View.OnClickListener() {
                                        @Override
                                        public void onClick(View v) {
                                            Context context = getApplicationContext();
                                            Log.d("unfriend1", "onClick: ");
                                            RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
                                            String url = "http://162.246.157.128/MLFitness/add_relationship.php";
                                            Log.d("unfriend", "onClick: ");
                                            StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                                                    new Response.Listener<String>() {
                                                        //this is async reyes didn't tell me NO ONE TOLD ME
                                                        //this runs on a different thread than the main
                                                        @Override
                                                        public void onResponse(String response) {
                                                            ArrayList<User> users = new ArrayList<>();
                                                            Log.d("Response unfriended: ", response.toString());
                                                            Log.d("before if un", "da fuq ");
                                                            if (response.toString().equals("success")) {
                                                                ImageView add_friend = findViewById(R.id.add_friend_trainer);
                                                                ImageView unfriend = findViewById(R.id.sub_friend_trainer);
                                                                ImageView edit_button = findViewById(R.id.edit_profile_trainer);
                                                                add_friend.setVisibility(View.VISIBLE);
                                                                Log.d("TO FRONT", "onResponse: "+"made it");
                                                                unfriend.setVisibility(View.GONE);
                                                                edit_button.setVisibility(View.GONE);
                                                                is_subbed(trainer_obj);



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
                                                    //trainee
                                                    paramV.put("id", String.valueOf(SocketFunctions.user.getId()));
                                                    paramV.put("apiKey", SocketFunctions.apiKey);
                                                    //trainer
                                                    paramV.put("id2",String.valueOf(trainer_obj.getId()));
                                                    Log.d("THE IDS", "getParams: "+String.valueOf(SocketFunctions.user.getId())+" pain " +String.valueOf(trainer_obj.getId()));
                                                    if(SocketFunctions.user.isTrainer() == false){
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
                paramV.put("id2",String.valueOf(trainer_obj.getId()));
                paramV.put("type","2");
                return paramV;
            }
        };
        queue.add(stringRequest);
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

