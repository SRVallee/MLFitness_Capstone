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

public class TrainerHomePage extends AppCompatActivity {

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
        setContentView(R.layout.activity_trainer_home_page);

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
                        Toast.makeText(TrainerHomePage.this, "Home Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.upload: {
                        Toast.makeText(TrainerHomePage.this, "Upload Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.message: {
                        Toast.makeText(TrainerHomePage.this, "Message Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.setting: {
                        Toast.makeText(TrainerHomePage.this, "Setting Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.profile: {
                        Toast.makeText(TrainerHomePage.this, "Profile Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.logout: {
                        Toast.makeText(TrainerHomePage.this, "Logout Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.share: {
                        Toast.makeText(TrainerHomePage.this, "Share Selected", Toast.LENGTH_SHORT).show();
                        break;
                    }
                    case R.id.rate: {
                        Toast.makeText(TrainerHomePage.this, "Rate Selected", Toast.LENGTH_SHORT).show();
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
