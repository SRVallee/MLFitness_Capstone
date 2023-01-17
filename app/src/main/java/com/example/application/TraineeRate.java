package com.example.application;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.widget.Toast;

import com.google.android.material.navigation.NavigationView;

public class TraineeRate extends AppCompatActivity {

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
        setContentView(R.layout.activity_trainee_rate);

        drawerLayout = findViewById(R.id.drawer_layout);
        navigationView = findViewById(R.id.nav_view);
        drawerToggle = new ActionBarDrawerToggle(this, drawerLayout, R.string.open, R.string.close);
        drawerLayout.addDrawerListener(drawerToggle);
        drawerToggle.syncState();
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        navigationView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {

                switch (item.getItemId()) {
                    case R.id.home: {
                        Intent i = new Intent(getApplicationContext(), TraineeHomePage.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.upload: {
                        Intent i = new Intent(getApplicationContext(), TraineeUpload.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.message: {
                        Intent i = new Intent(getApplicationContext(), TraineeMessages.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.setting: {
                        Intent i = new Intent(getApplicationContext(), TraineeSettings.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.profile: {
                        Intent i = new Intent(getApplicationContext(), TraineeProfile.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.logout: {
                        Intent i = new Intent(getApplicationContext(), TraineeLogout.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.share: {
                        Intent i = new Intent(getApplicationContext(), TraineeShare.class);
                        startActivity(i);
                        break;
                    }
                    case R.id.rate: {
                        drawerLayout.closeDrawer(GravityCompat.START);
                        break;
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

            super.onBackPressed();
        }

    }
}

