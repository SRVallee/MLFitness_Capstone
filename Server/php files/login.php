<?php
$email = $_POST['email'];
$password = $_POST['password'];
$result = array();
$conn = mysqli_connect("localhost", "root", "", "ml_fitness"); //connect

if($conn){                                                       //if connection
    $sql = "select * from user where email = '".$email."'";
    $res = mysqli_query($conn, $sql);                             //get user with email
    if(mysqli_num_rows($res) != 0){                               //if user exists      
        $row = mysqli_fetch_assoc($res);
        if($email == $row["email"] && password_verify($password, $row["password"])){ //verify password
            //maybe use api keys later

            $result = array("status" => "success",     //return the user info
                            "user_id" => $row["user_id"],
                            "username" => $row["username"], 
                            "name" => $row["name"], 
                            "email" => $row["email"], 
                            "isTrainer" =>  $row["is_trainer"],
                            "api_key" => $row["api_key"]);
        }else{
            $result = array("status" => "Wrong Password");
        }
    }else{
        $result = array("status" => "User not found");
    }

}

echo json_encode($result, JSON_PRETTY_PRINT);