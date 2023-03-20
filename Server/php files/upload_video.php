<?php
if (isset($_FILES['video'])) {
  $user_id = (int)$_POST["id"];
  $apiKey = $_POST["apiKey"];
  $trainer_id = (int)$_POST["trainer_id"];
  $target_path = "../../../../videos" . basename($_FILES['video']['name']);

  $conn = mysqli_connect("localhost", "root", "MLFitness@123", "ml_fitness"); //connect
  $sql = "select * from user where (user_id = '".$user_id."' and api_key = '".$apiKey."')";
  $res = mysqli_query($conn, $sql);
  if(mysqli_num_rows($res) != 0){
    $row = mysqli_fetch_assoc($res);

    try {
      if (move_uploaded_file($_FILES['video']['tmp_name'], $target_path)) {
          echo "success";
      } else {
          echo "failed to move uploaded file";
      }
  } catch (Exception $e) {
      echo "Caught exception: " . $e->getMessage();
  }
  } else{
    echo "Error uploading video(user).";
  }
} else {
  echo "Video parameter not found.";
}