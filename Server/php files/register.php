<?php
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness");
$username = $_POST['username'];
$name = $_POST['name'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);
$isTrainer = $_POST['isTrainer'];
if($conn){
    $sql = "SELECT * from user where email = '".$email."'";
    $res = mysqli_query($conn, $sql);
        if(mysqli_num_rows($res) == 0){
        try{
            $apiKey = bin2hex(random_bytes(23));
        }catch(Exception $e){
            $apiKey = bin2hex(uniqid($email, true));
        }
        $sql = "INSERT INTO user(user_id, username, password, name, email, is_trainer, api_key) values(default,'".$username."','".$password."','".$name."','".$email."',".$isTrainer.",'".$apiKey."');";
        if(mysqli_query($conn, $sql)){
            $sql = "select * from user where email = '".$email."'";
            $res = mysqli_query($conn, $sql);
            if(mysqli_num_rows($res) != 0){                               //if user exists   
                $row = mysqli_fetch_assoc($res);
                if($isTrainer == 1){
                    $sql = "INSERT INTO trainer(trainer_id, credentials, reviews_location, ratings_amount) values('".$row["user_id"]."', 'No credatials yet', '/yes/here', 0);";
                    $res = mysqli_query($conn, $sql);
                    $sql = "SELECT * from user where trainer_id = ".$row["user_id"];
                    $res = mysqli_query($conn, $sql);
                    if(mysqli_num_rows($res) != 0){
                        $result = array("status" => "success",     //return the user info
                        "user_id" => $row["user_id"],
                        "api_key" => $row["api_key"]);
                    }else{
                        $result = array("status"=>"User created, but failed to register as trainer");
                    }
                }else{

                $result = array("status" => "success",     //return the user info
                "user_id" => $row["user_id"],
                "api_key" => $row["api_key"]);
                }
            }
            
        }else{
            $result = array("status"=>"Failed to register user");
        }
    }else{
        $result = array("status"=>"Email already linked");
    }
}else{
    $result = array("status"=>"Connection to database failed");
} 

echo json_encode($result, JSON_PRETTY_PRINT);