<?php

$path = '/home/harshkumar/new_BB/bumblebee/configs/config_sg.json';
$jsonString = file_get_contents($path);
$jsonData = json_decode($jsonString, true);
$firstName = $jsonData['internal_config'];

echo $firstName['v1_api_subdomain']
?>