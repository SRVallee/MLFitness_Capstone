package com.example.application;

import static com.example.application.SocketFunctions.getWorkouts;

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
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.navigation.NavigationView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class TraineeHomePage extends AppCompatActivity {

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;
    Context context = this;

    private Boolean exit = false;
    private long pressedTime;
    private ListView workoutsListView;

    private ArrayList<Workout> workouts;
    ArrayList<ObjectTrainer> trainers = new ArrayList<>();


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
        setContentView(R.layout.activity_trainee_home_page);

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        workoutsListView = findViewById(R.id.listTrainee_eval);
        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);

        drawerToggle.syncState();
        Objects.requireNonNull(getSupportActionBar()).setDisplayHomeAsUpEnabled(true);
        if (!SocketFunctions.user.isTrainer()) {
            navigationView.getMenu().findItem(R.id.trainers).setVisible(true);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(false);
        }
        else{
            navigationView.getMenu().findItem(R.id.trainers).setVisible(false);
            navigationView.getMenu().findItem(R.id.trainees).setVisible(true);

        }

        // get workouts from server
        workouts = getWorkouts(getApplicationContext(), workoutsListView, SocketFunctions.user.getId());

        display_trainers();
        invalidateOptionsMenu();
        invalidateMenu();
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {

                switch (item.getItemId()) {
                    case R.id.home: {
                        //Already selected
                        //Close drawer
                        drawerLayout.closeDrawer(GravityCompat.START);
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
                        Intent i = new Intent(getApplicationContext(), FriendsPage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.profile: {
                        //Go to profile
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
        workoutsListView.setClickable(true);
        workoutsListView.setOnItemClickListener((adapterView, view, i, l) -> {
            Workout workoutItem = (Workout) workoutsListView.getAdapter().getItem(i);
            Intent intent = new Intent(getApplicationContext(), TraineeWorkoutFeedback.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
            intent.putExtra("workout_id", workoutItem.getWorkout_id());
            startActivity(intent);
            finish();
        });
    }

    public void click_btnNewWorkout(View view){
        Intent i = new Intent(getApplicationContext(), ChooseExercise.class);
        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
        startActivity(i);
        finish();
    }

    private void display_trainers() {
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_relationships.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    //this is async reyes didn't tell me NO ONE TOLD ME
                    //this runs on a different thread than the main
                    @Override
                    public void onResponse(String response) {
                        ArrayList<String> id1 = new ArrayList<>();
                        Log.d("display trainers: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                for (int i = 0; i < jsonResponse.getJSONArray("relationships").length(); i++) {
                                    JSONObject trainerid1;
                                    JSONObject trainerid2;
                                    trainerid1 = jsonResponse.getJSONArray("relationships").getJSONObject(i);
                                    trainerid2 = jsonResponse.getJSONArray("relationships").getJSONObject(i);
                                    String trainerObj = new String(trainerid1.getString("user_id"));
                                    String trainerObj2 = new String(trainerid2.getString("user_id_2"));
                                    if (!trainerObj.equals(String.valueOf(SocketFunctions.user.getId()))) {
                                        id1.add(trainerObj);
                                    }
                                    if (!trainerObj2.equals(String.valueOf(SocketFunctions.user.getId()))) {
                                        id1.add(trainerObj2);
                                    }

                                }
                                Log.d("trainer id list", "onResponse: "+ id1);
                                trainer_scroll(id1);


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
                paramV.put("id2",String.valueOf(SocketFunctions.user.getId()));
                paramV.put("type","1");
                return paramV;
            }
        };
        queue.add(stringRequest);
    }

    public void trainer_scroll(ArrayList<String> id1){
        Log.d("trainer scroll", "trainer_scroll: "+ id1);
        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_user_info.php";
        //this is for the interaction with  the scrollview

        //this for loop is to add each trainer into the linearlayout
        for (int i = 0; i < id1.size(); i++) {
            int finalI = i;
            int finalI1 = i;
            StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                    new Response.Listener<String>() {
                        //this is async reyes didn't tell me NO ONE TOLD ME
                        //this runs on a different thread than the main
                        @Override
                        public void onResponse(String response) {
                            HorizontalScrollView trainer_list = findViewById(R.id.trainer_pfp_scroll);
                            LinearLayout linearLayout_trainer = findViewById(R.id.trainer_home_linear);

                            Log.d("home trainer get: ", response.toString()+" pain "+ id1.get(finalI));
                            try {
                                JSONObject jsonResponse = new JSONObject(response);
                                String status = jsonResponse.getString("status");
                                if (status.equals("success")) {
                                    Log.d("trainer name: ", jsonResponse.getString("name"));
                                    //this is for the interaction with  the scrollview

                                    //this for loop is to add each trainer into the linearlayout
                                    // this is to inflate the trainer row
                                    View Trainer_constraint = LayoutInflater.from(context).inflate(R.layout.home_user_display, null);
                                    //this is to set the positions to get the item
                                    Trainer_constraint.setTag(finalI1);
                                    //this is to get the text view from the trainer row to change the set text
                                    TextView Trainer_name =Trainer_constraint.findViewById(R.id.trainer_home_name);
                                    Trainer_name.setText(jsonResponse.getString("name"));
                                    Trainer_name.setTextSize(25);
                                    //this adds the view
                                    linearLayout_trainer.addView(Trainer_constraint, finalI1);
                                    //linearLayout_trainer.setOnClickListener(clickInLinearLayout());
                                    //this is to set a onclick listener for each trainer row
                                    onclick_trainer_pfp(Trainer_constraint,id1.get(finalI));

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
                    paramV.put("id2", id1.get(finalI));
                    return paramV;
                }
            };
            queue.add(stringRequest);

        }
    }

    public void onclick_trainer_pfp(View Trainer_constraint, String name){

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
                                    if (trainerObj.getId().toString().equals(name)){
                                        trainers.add(trainerObj);
                                    }
                                }

                                    //linearLayout_trainer.setOnClickListener(clickInLinearLayout());
                                    //this is to set a onclick listener for each trainer row
                                    Trainer_constraint.setOnClickListener(new View.OnClickListener() {
                                        @Override
                                        public void onClick(View v) {
                                            Integer position = Integer.parseInt(v.getTag().toString());
                                            TextView name_text = findViewById(R.id.trainer_home_name);
                                            String trainer_text =  name_text.getText().toString();
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
                                            String trainer_name = trainers.get(position).getTrainer_name();
                                            Log.d("name on row", "onClick: "+trainer_name);
                                            Intent Trainer_profile = new Intent(getApplicationContext(), TrainerProfile.class);
                                            Trainer_profile.putExtra("trainerObj", trainers.get(position));
                                            startActivity(Trainer_profile);
                                            finish();

                                        }
                                    });

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
            //Close Application
            if (pressedTime + 2000 > System.currentTimeMillis()) {
                Intent i = new Intent(Intent.ACTION_MAIN);
                i.addCategory(Intent.CATEGORY_HOME);
                i.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                startActivity(i);
            } else {
                Toast.makeText(getBaseContext(), "Press back again to exit", Toast.LENGTH_SHORT).show();
            }
            pressedTime = System.currentTimeMillis();
        }
        //super.onBackPressed();
    }
}