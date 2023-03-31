package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

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

public class TrainerTraineeProfile extends AppCompatActivity {

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
        setContentView(R.layout.activity_trainer_trainee_profile);

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
        getUsers();
        drawerToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        if (SocketFunctions.user.isTrainer() == false) {
            navigationView.getMenu().findItem(R.id.trainers).setVisible(true);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(false);
        }
        else{
            navigationView.getMenu().findItem(R.id.trainers).setVisible(false);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(true);

        }
        invalidateOptionsMenu();
        invalidateMenu();
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {

                switch (item.getItemId()) {
                    case R.id.home: {
                        //Go to home
                        Intent i = new Intent(getApplicationContext(), TrainerHomePage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
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
                        //Close drawer
                        drawerLayout.closeDrawer(GravityCompat.START);
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

    public void getUsers(){
        Context context = getApplicationContext();
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_all_trainees.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    //this is async reyes didn't tell me NO ONE TOLD ME
                    //this runs on a different thread than the main
                    @Override
                    public void onResponse(String response) {
                        ArrayList<User> users = new ArrayList<>();
                        Log.d("Response trainee: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                Log.d("trainee array: ", jsonResponse.getString("trainees"));
                                JSONArray user_obj = new JSONArray(jsonResponse.getString("trainees")) ;
                                for (int i = 0; i < user_obj.length(); i++) {
                                    User user = new User(
                                            user_obj.getJSONObject(i).getInt("user_id"),
                                            user_obj.getJSONObject(i).getString("username"),
                                            user_obj.getJSONObject(i).getString("name"),
                                            user_obj.getJSONObject(i).getString("email"));
                                    users.add(user);
                                }
                                //this is for the interaction with  the scrollview
                                ScrollView user_list = findViewById(R.id.trainee_scroll);
                                LinearLayout linearLayout_trainer = findViewById(R.id.trainee_list);
                                //this for loop is to add each trainer into the linearlayout
                                for (int i = 0; i < users.size(); i++) {
                                    // this is to inflate the trainer row
                                    View Trainer_constraint = LayoutInflater.from(context).inflate(R.layout.trainer_row, null);
                                    //this is to set the positions to get the item
                                    Trainer_constraint.setTag(i);
                                    //this is to get the text view from the trainer row to change the set text
                                    TextView Trainer_name =Trainer_constraint.findViewById(R.id.Trainer_name_text);
                                    Trainer_name.setText(users.get(i).getName());
                                    Trainer_name.setTextSize(25);
                                    //this adds the view
                                    linearLayout_trainer.addView(Trainer_constraint,i);
                                    //this is to set a onclick listener for each trainer row
                                    Trainer_constraint.setOnClickListener(new View.OnClickListener() {
                                        @Override
                                        public void onClick(View v) {
                                            Integer position = Integer.parseInt(v.getTag().toString());
                                            //count down timer just so that it shows gray on what you clicked
                                            CountDownTimer countdown = new CountDownTimer(1000, 1000) {
                                                @Override
                                                public void onTick(long millisUntilFinished) {
                                                    v.setBackgroundColor(getColor(R.color.light_grey));
                                                }

                                                @Override
                                                public void onFinish() {
                                                    v.setBackgroundColor(getColor(R.color.white));
                                                }
                                            };
                                            countdown.start();
                                            Log.d("in onclick", "onClick: "+position);
                                            String trainer_name = users.get(position).getName();
                                            Log.d("name on row", "onClick: "+trainer_name);
                                            Intent Trainee_profile = new Intent(getApplicationContext(), TraineeProfile.class);
                                            Trainee_profile.putExtra("traineeObj", users.get(position));
                                            startActivity(Trainee_profile);
                                            finish();

                                        }
                                    });
                                    Log.d("inside for loop", "onResponse: "+i);
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
