package com.example.application;

import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

public class LoadAllExistingVideos extends AppCompatActivity {
    RecyclerView recyclerView;
    Toolbar toolbar;

    AllExistingVideosAdapter allExistingVideosAdapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_load_all_existing_videos);

        toolbar = findViewById(R.id.toolbar_load_all);
        toolbar.setTitle("Trim Videos");
        //setSupportActionBar(toolbar);
        allExistingVideosAdapter = new AllExistingVideosAdapter(this);
        recyclerView = findViewById(R.id.recyclerView_load_all_existing);
        GridLayoutManager gridLayoutManager = new GridLayoutManager(getApplicationContext(), 3);
        recyclerView.setLayoutManager(gridLayoutManager);
        recyclerView.setAdapter(allExistingVideosAdapter);
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Intent intent = new Intent(getApplicationContext(), Trimmer.class);
        overridePendingTransition(0, 0);
        startActivity(intent);
    }
}