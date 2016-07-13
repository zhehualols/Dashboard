<?php 
$servername = "localhost";
$username = "root";
$password = "password";
$database= "hdmi";
//create connection
$conn = new mysql_connect($servername,$username,$password,$database);

//check connection
if ($conn->connect_error){
    die("connection failed:").$conn->connect_error);
}
echo "Connected successfully";
?>