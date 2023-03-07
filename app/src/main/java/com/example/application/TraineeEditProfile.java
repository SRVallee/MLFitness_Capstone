package com.example.application;

import android.app.ActivityOptions;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;


public class TraineeEditProfile extends AppCompatActivity {

    String name, username, email, passwordOld, passwordOne, passwordTwo;

    ImageView userProfilePicture;
    TextView traineeProfileUsernameEdit;
    TextView traineeProfileEmailEdit;
    TextView traineeProfileNameEdit;

    int SELECT_IMAGE_CODE=1;

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

        String trainee_profile_username = SocketFunctions.user.getUserName();
        traineeProfileUsernameEdit.setText(trainee_profile_username);

        String trainee_profile_email = SocketFunctions.user.getEmail();
        traineeProfileEmailEdit.setText(trainee_profile_email);

        String trainee_profile_name = SocketFunctions.user.getName();
        traineeProfileNameEdit.setText(trainee_profile_name);

        //Won't display password for security reasons

        //Check line to get from db
        int trainee_profile_image = R.drawable.ic_baseline_tag_faces_24;
        userProfilePicture.setImageResource(trainee_profile_image);

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
        name = traineeProfileUsernameEdit.getText().toString();

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

        if(!email.isEmpty() && !emailIsValid(email)){
            alertDialog.setTitle("Invalid email: " + email);
            alertDialog.setMessage("Please enter a valid email");
            alertDialog.show();
            return;
        }


        //Set values
        //user.setName(name);
        //if(!email.isEmpty()){
        //    user.setEmail(email);
        //}



        //Replace Employee
        //int rowNum = db.addOrReplaceUser(user);


        Intent i;
        i = new Intent(getApplicationContext(), TraineeProfile.class);
        startActivity(i);
        finish();
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

        if(requestCode==1) {
            Uri uri;
            uri = data.getData();
            userProfilePicture.setImageURI(uri);
            //Use uri to set in db
        }

    }

    private boolean emailIsValid(String email){
        return (email.matches("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\\.[a-zA-Z0-9_-]+)"));
    }

}
