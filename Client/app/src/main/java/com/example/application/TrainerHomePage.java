package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.HorizontalScrollView;
import android.widget.ImageView;
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
import com.squareup.picasso.Picasso;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class TrainerHomePage extends AppCompatActivity {

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;

    ListView listTrainerWorkout;
    ListView listTraineeWorkout;

    ArrayList<Workout> trainerWorkouts;
    ArrayList<Workout> traineeSubWorkouts;
    Context context = this;

    ArrayList<User> trainees = new ArrayList<>();

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
        setContentView(R.layout.activity_trainer_home_page);

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        listTrainerWorkout = findViewById(R.id.list_trainerWorkouts);
        listTraineeWorkout = findViewById(R.id.list_traineeSubmitWorkouts);

        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
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

        trainerWorkouts = SocketFunctions.getWorkouts(getApplicationContext(), listTrainerWorkout, SocketFunctions.user.getId());
        traineeSubWorkouts = SocketFunctions.getWorkouts(
                getApplicationContext(),
                listTraineeWorkout,
                SocketFunctions.user.getId(),
                "http://162.246.157.128/MLFitness/get_trainer_workouts.php");

        display_trainees();
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
                        Intent i = new Intent(getApplicationContext(), FriendsPage.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.profile: {
                        //Go to profile
                        Intent i = new Intent(getApplicationContext(), TrainerProfile.class);
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

        listTraineeWorkout.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Workout workoutItem = (Workout) listTraineeWorkout.getAdapter().getItem(i);
                Intent intent = new Intent(getApplicationContext(), TrainerFeedback.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                intent.putExtra("workout_id", workoutItem.getWorkout_id());
                startActivity(intent);
            }
        });
    }

    private void display_trainees() {
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
                                    String traineeObj = new String(trainerid1.getString("user_id"));
                                    String trainerObj2 = new String(trainerid2.getString("user_id_2"));
                                    if (!traineeObj.equals(String.valueOf(SocketFunctions.user.getId()))) {
                                        id1.add(traineeObj);
                                    }
                                    if (!trainerObj2.equals(String.valueOf(SocketFunctions.user.getId()))) {
                                        id1.add(trainerObj2);
                                    }

                                }
                                Log.d("trainer id list", "onResponse: "+ id1);
                                trainee_scroll(id1);


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


    public void trainee_scroll(ArrayList<String> id1){
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
                            HorizontalScrollView trainer_list = findViewById(R.id.trainee_scroll);
                            LinearLayout linearLayout_trainer = findViewById(R.id.trainee_pfp_disp);

                            Log.d("home trainee get: ", response.toString()+" pain "+ id1.get(finalI));
                            try {
                                JSONObject jsonResponse = new JSONObject(response);
                                String status = jsonResponse.getString("status");
                                if (status.equals("success")) {
                                    Log.d("trainee name: ", jsonResponse.getString("name"));
                                    //this is for the interaction with  the scrollview

                                    //this for loop is to add each trainer into the linearlayout
                                    // this is to inflate the trainer row
                                    View Trainer_constraint = LayoutInflater.from(context).inflate(R.layout.home_user_display, null);
                                    //this is to set the positions to get the item
                                    Trainer_constraint.setTag(finalI1);
                                    //this is to get the text view from the trainer row to change the set text
                                    TextView Trainer_name = Trainer_constraint.findViewById(R.id.trainer_home_name);
                                    ImageView Trainer_pfp = Trainer_constraint.findViewById(R.id.Userpfp);
                                    Trainer_name.setText(jsonResponse.getString("name"));
                                    Trainer_name.setTextSize(25);
                                    //this adds the view
                                    linearLayout_trainer.addView(Trainer_constraint, finalI1);
                                    //linearLayout_trainer.setOnClickListener(clickInLinearLayout());
                                    //this is to set a onclick listener for each trainer row
                                    onclick_trainee_pfp(Trainer_constraint,id1.get(finalI));

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

    public void onclick_trainee_pfp(View Trainer_constraint, String name){

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_all_trainees.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    //this is async reyes didn't tell me NO ONE TOLD ME
                    //this runs on a different thread than the main
                    @Override
                    public void onResponse(String response) {

                        Log.d("all users: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                Log.d("Array: ", jsonResponse.getString("trainees"));
                                JSONArray user_obj = new JSONArray(jsonResponse.getString("trainees")) ;
                                for (int i = 0; i < user_obj.length(); i++) {
                                    User traineeObj = new User(user_obj.getJSONObject(i).getInt("user_id"),
                                            user_obj.getJSONObject(i).getString("username"),
                                            user_obj.getJSONObject(i).getString("name"),
                                            user_obj.getJSONObject(i).getString("email"));

                                    if (Integer.toString(traineeObj.getId()).equals(name)){
                                        trainees.add(traineeObj);
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
                                        String trainer_name = trainees.get(position).getName();
                                        Log.d("name on row", "onClick: "+trainer_name);
                                        Intent Trainee_profile = new Intent(getApplicationContext(), TraineeProfile.class);
                                        Trainee_profile.putExtra("traineeObj", trainees.get(position));
                                        startActivity(Trainee_profile);
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
