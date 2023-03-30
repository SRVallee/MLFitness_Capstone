<?php
if (isset($_FILES['video'])) {
  $user_id = (int)$_POST["id"];
  $apiKey = $_POST["apiKey"];
  $exercise_id = $_POST["exercise_id"];


  $filename = 'video_' . date('Ymd_His') . '.mp4';

  $target_dir1 = "/var/www/html/MLFitness/videos/" . $user_id;
  if (!file_exists($target_dir1)) {
    mkdir($target_dir1, 0777, true);
  }
  //$target_path =  $target_dir1 . "/" . basename($_FILES['video']['name']);
  $target_path =  $target_dir1 . "/" . $filename;

  $conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
  $sql = "SELECT * from user where (user_id = '".$user_id."' and api_key = '".$apiKey."')";
  $res = mysqli_query($conn, $sql);

  if(mysqli_num_rows($res) != 0){
    $sql = "SELECT model_name FROM exercise WHERE exercise_id = ".$exercise_id;
    $res = mysqli_query($conn, $sql);
    if(mysqli_num_rows($res) != 0){
      $row = mysqli_fetch_assoc($res);
      try {
        if(move_uploaded_file($_FILES['video']['tmp_name'], $target_path)){
          $command = escapeshellcmd("/home/ubuntu/CapstoneFiles/MLFitness_Capstone/Server/ComputerVision ".$user_id." ".$row["model_name"]." ".$target_path);
          $output = shell_exec($command);

          $result = array("status" => "success",     //return the user info
          "output" => $output);
          
        }else{
          $result = array("status" => "Error saving video");
        }
        
      } catch (Exception $e) {
        $result = array("status" => "Caught exception: " . $e->getMessage());
      }
    }else{
      $result = array("status" => "Error finding exercise");
    }
  } else{
    $result = array("status" => "Error uploading video(user).");
  }
} else {
  $result = array("status" => "Video parameter not found.");
}

echo json_encode($result, JSON_PRETTY_PRINT);