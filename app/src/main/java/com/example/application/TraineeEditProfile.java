package com.example.application;

import android.app.ActivityOptions;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.ImageDecoder;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.squareup.picasso.Picasso;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;


public class TraineeEditProfile extends AppCompatActivity {

    String name, username, email, passwordOld, passwordOne, passwordTwo;
    Bitmap pfp;

    boolean wait = false;

    ImageView userProfilePicture;
    TextView traineeProfileUsernameEdit;
    TextView traineeProfileEmailEdit;
    TextView traineeProfileNameEdit;
    TextView editPasswordOld;
    TextView editPasswordOne;
    TextView editPasswordTwo;

    int SELECT_IMAGE_CODE=1;
    private ImageDecoder.Source newProfilePicture;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trainee_edit_profile);

        //Set objects in the page
        //Once db is implemented change from test/example cases to the version that get the data from the db

        //Init fields in xml
        userProfilePicture = (ImageView) findViewById(R.id.profile_picture);
        traineeProfileUsernameEdit = (TextView) findViewById(R.id.trainee_profile_username_edit);
        traineeProfileEmailEdit = (TextView) findViewById(R.id.trainee_profile_email_edit);
        traineeProfileNameEdit = (TextView) findViewById(R.id.trainee_profile_name_edit);

        //Assigns values to the fields in the xml

        String username = SocketFunctions.user.getUserName();
        traineeProfileUsernameEdit.setText(username);

        String email = SocketFunctions.user.getEmail();
        traineeProfileEmailEdit.setText(email);

        name = SocketFunctions.user.getName();
        traineeProfileNameEdit.setText(name);

        //Won't display password for security reasons
        editPasswordOld = findViewById(R.id.trainee_profile_old_password);
        editPasswordOne = findViewById(R.id.trainee_profile_password_one);
        editPasswordTwo = findViewById(R.id.trainee_profile_password_two);


        //Check line to get from db
        try {
            if (SocketFunctions.user.hasPfp()) {
                userProfilePicture.setImageBitmap(SocketFunctions.user.getPfp());
            } else {
                Picasso.get().load("http://162.246.157.128/MLFitness/pfps/" + SocketFunctions.user.getId() + ".jpg").into(userProfilePicture);
                Drawable pfp = userProfilePicture.getDrawable();
                SocketFunctions.user.setPfp(Bitmap.createBitmap(pfp.getIntrinsicWidth(), pfp.getIntrinsicHeight(), Bitmap.Config.ARGB_8888));
            }
        }catch (Exception e){
            int trainee_profile_image = R.drawable.ic_baseline_tag_faces_24;
            userProfilePicture.setImageResource(trainee_profile_image);
        }

    }

    public void cancelChange(View view){
        //Do nothing and just return to the profile page
        Intent i;
        i = new Intent(getApplicationContext(), TraineeProfile.class);
        startActivity(i);
        this.finish();
    }

    public void saveEmployeeButton(View view) {

        AlertDialog alertDialog = new AlertDialog.Builder(this).create();
        alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

        //Set user to then put into the db
        //User Object
        username = traineeProfileUsernameEdit.getText().toString();
        if(username.isEmpty()){
            alertDialog.setTitle("No username");
            alertDialog.setMessage("A username is required");
            alertDialog.show();
            return;
        }

        name = traineeProfileNameEdit.getText().toString();
        if(name.isEmpty()){
            alertDialog.setTitle("No name");
            alertDialog.setMessage("A name is required");
            alertDialog.show();
            return;
        }

        email = traineeProfileEmailEdit.getText().toString();
        if(email.isEmpty()){
            alertDialog.setTitle("No Email");
            alertDialog.setMessage("An email is Required");
            alertDialog.show();
            return;
        }

        else if(!emailIsValid(email)){
            alertDialog.setTitle("Invalid email: " + email);
            alertDialog.setMessage("Please enter a valid email");
            alertDialog.show();
            return;
        }

        passwordOld = editPasswordOld.getText().toString();
        passwordOne = editPasswordOne.getText().toString();
        passwordTwo = editPasswordTwo.getText().toString();
        if(!passwordOld.isEmpty()){

            if(passwordOne.isEmpty() || passwordTwo.isEmpty()){
                alertDialog.setTitle("Missing Fields");
                alertDialog.setMessage("You must fill both boxes to change password");
                alertDialog.show();
            }else if(!passwordOne.equals(passwordTwo)){
                alertDialog.setTitle("Passwords do not match");
                alertDialog.setMessage("Password reentered must match the previous");
                alertDialog.show();
            }
        }

        if(newProfilePicture != null){
            Log.d("User id: ", "newPfp not null");
            try {
                pfp = ImageDecoder.decodeBitmap(newProfilePicture);
                SocketFunctions.uploadPfp(getApplicationContext(), pfp);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }



        RequestQueue queue = Volley.newRequestQueue(getApplicationContext());
        String url = "http://162.246.157.128/MLFitness/update_profile.php";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        if (response.equals("success")) { //or email already exists if when implemented
                            //Log.d("Response: ", response);
                            SocketFunctions.user.setUserName(username);
                            SocketFunctions.user.setEmail(email);
                            SocketFunctions.user.setName(name);
                            Intent i;
                            i = new Intent(getApplicationContext(), TraineeProfile.class);
                            startActivity(i);
                            finish();
                        }
                        else{
                            alertDialog.setTitle("Error!");
                            alertDialog.setMessage(response);
                            alertDialog.show();
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
                paramV.put("username", username);
                paramV.put("name", name);
                paramV.put("email", email);
                paramV.put("apiKey", SocketFunctions.apiKey);
                paramV.put("old_password", passwordOld);
                paramV.put("new_password", passwordOne);

                return paramV;
            }
        };
        queue.add(stringRequest);

        //Set values
        //user.setName(name);
        //if(!email.isEmpty()){
        //    user.setEmail(email);
        //}



        //Replace Employee
        //int rowNum = db.addOrReplaceUser(user);
    }

    @Override
    public void onBackPressed(){
        //Do nothing and just return to the profile page
        Intent i;
        i = new Intent(getApplicationContext(), TraineeProfile.class);
        startActivity(i);
        this.finish();
    }

    public void editProfPic(){
        //ImagePicker.with(this)
        //        .crop()	    			//Crop image(Optional), Check Customization for more option
        //        .compress(1024)			//Final image size will be less than 1 MB(Optional)
        //        .maxResultSize(1080, 1080)	//Final image resolution will be less than 1080 x 1080(Optional)
        //        .start();
    }

    public void selectProfilePic(View view) {
        Intent intent = new Intent();
        intent.setType("image/*");
        intent.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(intent.createChooser(intent,"Title"),SELECT_IMAGE_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(requestCode==1 && data != null) {
            Uri uri;
            uri = data.getData();
            userProfilePicture.setImageURI(uri);
            //Use uri to set in db
            ImageDecoder.Source source = ImageDecoder.createSource(this.getContentResolver(), uri);
            newProfilePicture = source;
            try {
                SocketFunctions.user.setPfp(ImageDecoder.decodeBitmap(source));
            } catch (IOException e) {
                e.printStackTrace();
            }


        }

    }

    private boolean emailIsValid(String email){
        return (email.matches("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\\.[a-zA-Z0-9_-]+)"));
    }

}
