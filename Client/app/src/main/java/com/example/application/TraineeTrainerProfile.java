package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.app.ActivityOptions;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.HorizontalScrollView;
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
import java.util.logging.Handler;

public class TraineeTrainerProfile extends AppCompatActivity {

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;
    ArrayList<Integer> AllTrainerIds;
    Context context = this;
    private ScrollView trainer_Full_List;
    private Boolean exit = false;
    private long pressedTime;
    //this is for the vertical scroll view for the trainer search page it
    //is the adapter for getting and setting the views
    public class trainer_adapter extends FrameLayout{

        private Context context;
        private ArrayList<ObjectTrainer> trainerList;
        public trainer_adapter(@NonNull Context context, ArrayList<ObjectTrainer> trainerList) {
            super(context);
            this.context = context;
            this.trainerList = trainerList;

        }
        public void addView(View child, int index, ViewGroup viewgroup){

        }
    }
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
        setContentView(R.layout.activity_trainee_trainer_profile);

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
        //get trainers is asynchronous
        getTrainers();
        drawerToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);




        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                //flag activity to front makes no sense when all of it gets finished everytime
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
                        finish();
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
                    case R.id.trainers: {
                        //Go to trainers
                        //Close drawer
                        drawerLayout.closeDrawer(GravityCompat.START);
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
                        Intent i = new Intent(getApplicationContext(), TraineeProfile.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
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

    public ArrayList<ObjectTrainer> getTrainers() {
        ArrayList<ObjectTrainer> trainers = new ArrayList<>();

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_trainers.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    //this is async reyes didn't tell me NO ONE TOLD ME
                    //this runs on a different thread than the main
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                Log.d("Array: ", jsonResponse.getString("trainers"));
                                for (int i = 0; i < jsonResponse.getJSONArray("trainers").length(); i++) {
                                    String trainerlist;
                                    trainerlist = jsonResponse.getJSONArray("trainers").getString(i);
                                    String[] trainerSplit= trainerlist.split(",");
                                    if (trainerSplit[2].isEmpty()){
                                        trainerSplit[2] = "0.0";
                                    }
                                    ObjectTrainer trainerObj = new ObjectTrainer(Integer.valueOf(trainerSplit[0]),trainerSplit[1],
                                            Float.valueOf(trainerSplit[2]),trainerSplit[3],trainerSplit[4],trainerSplit[5]);
                                    trainers.add(trainerObj);
                                }
                                ScrollView trainer_list = findViewById(R.id.trainer_full_list);
                                LinearLayout linearLayout_trainer = findViewById(R.id.trainer_display_list);
                                // this is to inflate the trainer row
                                for (int i = 0; i < trainers.size(); i++) {
                                    View Trainer_constraint = LayoutInflater.from(context).inflate(R.layout.trainer_row, null);
                                    //this is to get the text view from the trainer row to change the set text
                                    TextView Trainer_name =Trainer_constraint.findViewById(R.id.Trainer_name_text);
                                    LinearLayout trainer;
                                    Trainer_name.setText("bombsas "+i);
                                    Trainer_name.setTextSize(25);
                                    linearLayout_trainer.addView(Trainer_constraint);
                                }
                            }

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        //everything has to be done here due to the on response is asynchronous

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
        return trainers;
    }
}
