package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.app.ActivityOptions;
import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

import android.app.Activity;
import android.graphics.*;
import android.os.Bundle;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.androidplot.util.PixelUtils;
import com.androidplot.xy.SimpleXYSeries;
import com.androidplot.xy.XYSeries;
import com.androidplot.xy.*;

import java.text.FieldPosition;
import java.text.Format;
import java.text.ParsePosition;
import java.util.*;

import com.google.android.material.navigation.NavigationView;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.logging.Handler;

public class TraineeWorkouts extends AppCompatActivity implements View.OnClickListener{

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;

    private Boolean exit = false;
    private long pressedTime;
    private Spinner s;
    private ArrayList<JSONObject> workouts = new ArrayList<>();

    Button button1, button2;

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        if (drawerToggle.onOptionsItemSelected(item)) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private XYPlot plot;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainee_workouts);

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
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

        //Initialize XYPlot reference
        plot = (XYPlot) findViewById(R.id.plot);
        // Set the range of the y-axis to be between 0 and 100
        plot.setRangeBoundaries(0, BoundaryMode.FIXED, 100, BoundaryMode.FIXED);

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
                        //Already selected
                        //Close drawer
                        drawerLayout.closeDrawer(GravityCompat.START);
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

        s = findViewById(R.id.workoutSelector);
        ArrayAdapter<Exercise> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, SocketFunctions.exercises);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        s.setAdapter(adapter);
        s.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){ // Listener for exercise
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l) {
                try {
                    plotGraph();
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView) {
                //has to be here
            }
        });

        button1 = (Button) findViewById(R.id.reviewFeedback);
        button1.setOnClickListener(TraineeWorkouts.this);

        button2 = (Button) findViewById(R.id.submitWorkouts);
        button2.setOnClickListener(TraineeWorkouts.this);
        getWorkouts();
    }

    @Override
    public void onClick(View v) {

        Intent i;

        switch (v.getId()) {
            //Go to review feedback
            case R.id.reviewFeedback:
                i = new Intent(getApplicationContext(), TraineeWorkoutFeedback.class);
                startActivity(i);
                break;
            //Go to upload
            case R.id.submitWorkouts:
                Intent intent = new Intent(TraineeWorkouts.this, TraineeUpload.class);
                String path = Environment.getExternalStorageDirectory().getPath();
                intent.putExtra("path", path);
                startActivity(intent);
                break;
            default:
                break;
        }
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

    public void getWorkouts() {
        ArrayList<ObjectTrainer> trainers = new ArrayList<>();

        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/get_workouts.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("Response: ", response.toString());
                        try {
                            JSONObject jsonResponse = new JSONObject(response);
                            String status = jsonResponse.getString("status");
                            if (status.equals("success")) {
                                Log.d("Array: ", jsonResponse.getString("workouts"));
                                for (int i = 0; i < jsonResponse.getJSONArray("workouts").length(); i++) {
                                    workouts.add(jsonResponse.getJSONArray("workouts").getJSONObject(i));
                                }
                                plotGraph();
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
                paramV.put("user_id", String.valueOf(SocketFunctions.user.getId()));
                return paramV;
            }
        };
        queue.add(stringRequest);

    }

    private void plotGraph() throws JSONException {

        plot.clear();
        ArrayList<Double> scores = new ArrayList<>();
        //Create a couple arrays of y-values to plot
        for (JSONObject workout:workouts){
            if(((Exercise)s.getSelectedItem()).getId() == workout.getInt("exercise_exercise_id")){
                scores.add(workout.getDouble("score")*100);
            }
        }

        if(scores.isEmpty()){
            return;
        }
        Log.d("scores", scores.toString());
        final Number[] domainLabels = {1, 2, 3, 6, 7, 8, 9, 10, 13, 14};

        //Turn the above arrays into XYSeries
        //(Y_VALS_ONLY means use the element index as the x value)
        XYSeries scoresWithDate = new SimpleXYSeries(
                scores, SimpleXYSeries.ArrayFormat.Y_VALS_ONLY, "score");
        Log.d("scores with date", String.valueOf(scoresWithDate.size()));

        //Create formatters to use for drawing a series using LineAndPointRenderer
        //and configure them from xml:
        LineAndPointFormatter series1Format =
                new LineAndPointFormatter(this, R.xml.line_point_formatter_with_labels);

        //Add some smoothing to the lines:
        if(scores.size() > 3) {
            series1Format.setInterpolationParams(
                    new CatmullRomInterpolator.Params(10, CatmullRomInterpolator.Type.Centripetal));
        }
        //Add a new series' to the xyplot:
        plot.addSeries(scoresWithDate, series1Format);

        plot.getGraph().getLineLabelStyle(XYGraphWidget.Edge.BOTTOM).setFormat(new Format() {
            @Override
            public StringBuffer format(Object obj, StringBuffer toAppendTo, FieldPosition pos) {
                int i = Math.round(((Number) obj).floatValue());
                return toAppendTo.append(domainLabels[i]);
            }
            @Override
            public Object parseObject(String source, ParsePosition pos) {
                return null;
            }
        });

        plot.redraw();
    }

}