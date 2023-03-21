package com.example.application;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.ContentResolver;
import android.content.Context;
import android.content.ContextWrapper;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.webkit.MimeTypeMap;
import android.widget.ImageView;
import android.widget.MediaController;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.navigation.NavigationView;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.HashMap;
import java.util.Map;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Retrofit;
import retrofit2.converter.scalars.ScalarsConverterFactory;

public class TraineeUpload extends AppCompatActivity {

    DrawerLayout drawerLayout;
    NavigationView navigationView;
    ActionBarDrawerToggle drawerToggle;


    VideoView videoPreviewer;

    //Permission codes that are used
    private static int CAMERA_PERMISSION_CODE = 100;
    private static int VIDEO_RECORD_CODE = 101;
    private static int WRITE_PERMISSION_CODE = 111;

    private static int PICK_VIDEO_REQUEST = 1111111;

    //This is when the video that is recorded is being stored
    private Uri videoPath;

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
        setContentView(R.layout.activity_trainee_upload);

        videoPreviewer = findViewById(R.id.videoView2);

        //RecyclerView recyclerView = findViewById(R.id.videoListViewer);
        TextView noFilesText = findViewById(R.id.noFilesTextView);

        //Get path to display for the video list

        String storagePath = Environment.getExternalStorageDirectory().getPath();
        String path = getIntent().getStringExtra("path");

        File root = new File(path);
        File[] filesAndFolders = root.listFiles();

        if (filesAndFolders==null||filesAndFolders.length==0) {
            noFilesText.setVisibility(View.VISIBLE);
        }

        noFilesText.setVisibility(View.INVISIBLE);

        //recyclerView.setLayoutManager(new LinearLayoutManager(this));
        //recyclerView.setAdapter(new videoListAdapter(getApplicationContext(),filesAndFolders));

        //Checks if device has a camera and then gets permission for it
        if (isCameraPresentInPhone()) {
            Log.i("VIDEO_RECORD_TAG", "Camera is detected");
            getCameraPermission();
        } else {
            Log.i("VIDEO_RECORD_TAG", "No camera is detected");
        }

        //Asks for permission to write to storage
        getWritePermission();

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
                        Intent i = new Intent(getApplicationContext(), TraineeTrainerProfile.class);
                        i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                        startActivity(i);
                        finish();
                        break;
                    }
                    case R.id.friends: {
                        //Go to friends
                        Intent i = new Intent(getApplicationContext(), TraineeProfile.class);
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

    /***
     * On click method for button to record video, calls recordVideo function.
     * Does not return anything.
     * ***/
    public void recordVideoButtonPressed(View view) {
        recordVideo();
    }

    /***
     * Function to check if phone has a camera.
     * Returns a boolean to indicate if there is a camera is present.
     * ***/
    private boolean isCameraPresentInPhone() {
        if (getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA_ANY)) {
            return true;
        } else {
            return false;
        }
    }

    /***
     * Function that asks the user to give the application permission to use the camera.
     * Returns nothing.
     * ***/
    private void getCameraPermission() {
        //Check if permission is not granted
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_DENIED) {
            //If not granted, request permission
            ActivityCompat.requestPermissions(this, new String[]
                    {Manifest.permission.CAMERA}, CAMERA_PERMISSION_CODE);
        }
    }

    /***
     * Function used to record video.
     * Does not return anything.
     * ***/
    private void recordVideo() {
        Intent intent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
        startActivityForResult(intent, VIDEO_RECORD_CODE);
    }

    /***
     * This function first checks if the video is recorded, then checks if the results are good.
     * Also assigns the videoPath variable to the path of the video.
     * Returns nothing.
     * ***/
    /***
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        //Gets results of the video recording
        super.onActivityResult(requestCode, resultCode, data);
        //Check if Video is recorded
        if (requestCode == VIDEO_RECORD_CODE) {
            //Checks if video recording was completed
            if (resultCode == RESULT_OK) {
                //Gets path to video
                videoPath = data.getData();
                Log.i("VIDEO_RECORD_TAG", "Video is recorded and available at path " + videoPath);
                //Checks if the video recording was cancelled
            } else if (resultCode == RESULT_CANCELED) {
                Log.i("VIDEO_RECORD_TAG", "Recorded video is cancelled");
                //Gives a log if there were any errors in the recording
            } else {
                Log.i("VIDEO_RECORD_TAG", "Recorded video encountered an error");
            }
        }
    }
    ***/
    /***
     * This function takes the recorded video's path, and stores it in a folder for this application.
     * This function returns nothing. Does make logs if it saved the video or not.
     * ***/
    private void saveVideoToInternalStorage(String filePath) {

        File newFile;
        try {

            File currentFile = new File(filePath);
            String fileName = currentFile.getName();

            ContextWrapper cw = new ContextWrapper(getApplicationContext());
            File directory = cw.getDir("videoDir", Context.MODE_PRIVATE);

            newFile = new File(directory, fileName);

            if (currentFile.exists()) {

                InputStream in = new FileInputStream(currentFile);
                OutputStream out = new FileOutputStream(newFile);

                //Copy the bits from in-stream to out-stream
                byte[] buf = new byte[1024];
                int len;

                while ((len = in.read(buf)) > 0) {
                    out.write(buf, 0, len);
                }

                in.close();
                out.close();

                Log.v("", "Video file saved successfully.");

            } else {
                Log.v("", "Video saving failed. Source file missing.");
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /***
     * This function can load the video from where it was stored. May need this function for
     * another view, specifically one that allows the user to review their workouts.
     * ***/
    private void loadVideoFromInternalStorage(String filePath) {
        return;
        //Uri uri = Uri.parse(Environment.getExternalStorageDirectory() + filePath);
        //myVideoView.setVideoURI(uri);
    }

    /***
     *
     * ***/
    private void getWritePermission() {
        //Check if permission is not granted
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_DENIED) {
            //If not granted, request permission
            ActivityCompat.requestPermissions(this, new String[]
                    {Manifest.permission.WRITE_EXTERNAL_STORAGE}, WRITE_PERMISSION_CODE);
        }
    }

    /***
     *
     * ***/

    public void storageButtonPressed(View view) {
        Intent intent = new Intent();
        intent.setType("video/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(intent, 5);
    }

    Uri videoURI;

    // startActivityForResult is used to receive the result, which is the selected video.
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 5 && resultCode == RESULT_OK && data != null && data.getData() != null) {
            videoURI = data.getData();
            //progressDialog.setTitle("Uploading...");
            //progressDialog.show();
            try {
                uploadVideo();
            } catch (IOException e) {
                e.printStackTrace();
            }
            String video = String.valueOf(videoURI);
            Log.d("video",""+videoURI);
            videoPreviewer.setMediaController(new MediaController(this));
            videoPreviewer.setVideoURI(Uri.parse(video));
            videoPreviewer.requestFocus();
            videoPreviewer.start();
        }
    }

    private String getFileType(Uri videoURI) {
        ContentResolver r = getContentResolver();
        // get the file type ,in this case its mp4
        MimeTypeMap mimeTypeMap = MimeTypeMap.getSingleton();
        return mimeTypeMap.getExtensionFromMimeType(r.getType(videoURI));
    }

    private void uploadVideo() throws IOException {
        if (videoURI != null) {
            InputStream inputStream = getContentResolver().openInputStream(videoURI);
            byte[] bytes = getBytes(inputStream);
            RequestBody requestBody = RequestBody.create(bytes, MediaType.parse(getContentResolver().getType(videoURI)));
            OkHttpClient client = new OkHttpClient.Builder().build();
            Retrofit retrofit = new Retrofit.Builder()
                    .baseUrl("http://162.246.157.128/MLFitness/")
                    .client(client)
                    .addConverterFactory(ScalarsConverterFactory.create())
                    .build();
            ApiService apiService = retrofit.create(ApiService.class);
            int trainerId = 0; //TODO set to trainer the video belongs to.
            Call<String> call = apiService.uploadVideo(requestBody, String.valueOf(SocketFunctions.user.getId()), SocketFunctions.apiKey, String.valueOf(trainerId));
            call.enqueue(new Callback<String>() {

                @Override
                public void onResponse(Call<String> call, retrofit2.Response<String> response) {
                    Log.d("Video upload: ", response.toString());
                    String messageResponse = response.body().toString();
                    if (messageResponse.equals("success")) {

                        Log.d("Video Upload:", messageResponse);
                        Toast toast = Toast.makeText(getApplicationContext(), "Video Uploaded!", Toast.LENGTH_SHORT);
                        toast.show();
                    }
                    else{
                        Log.d("Video Upload:", messageResponse);
                        Toast toast = Toast.makeText(getApplicationContext(), messageResponse, Toast.LENGTH_SHORT);
                        toast.show();
                    }
                }

                @Override
                public void onFailure(Call<String> call, Throwable t) {
                    Log.d("Video Upload:", t.getLocalizedMessage());                }
            });
        }
    }

    /***
     * This function is to handle if the back button is selected.
     * - First, if the drawer is open it will close it.
     * - Second, if the drawer is closed, closes the activity and goes to the home page.
     * ***/
    @Override
    public void onBackPressed() {

        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            drawerLayout.closeDrawer(GravityCompat.START);
        } else {
            //Go to homepage
            Intent i = new Intent(getApplicationContext(), TraineeUpload.class);
            i.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
            startActivity(i);
            finish();
            super.onBackPressed();
        }
    }

    /**
     * This method reads the bytes from the InputStream and writes them to a ByteArrayOutputStream,
     * which is then converted to a byte array and returned.
     * @param inputStream
     * @return byte array
     * @throws IOException
     */
    private byte[] getBytes(InputStream inputStream) throws IOException {
        ByteArrayOutputStream byteBuffer = new ByteArrayOutputStream();
        int bufferSize = 1024;
        byte[] buffer = new byte[bufferSize];

        int len = 0;
        while ((len = inputStream.read(buffer)) != -1) {
            byteBuffer.write(buffer, 0, len);
        }
        return byteBuffer.toByteArray();
    }
}