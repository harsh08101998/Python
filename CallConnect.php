<?php 
#Link to developer portal  for connect to agent https://developer.exotel.com/api/#call-agent
$post_data = array(
    'From' => '08570027091',
    'To' => '07988532204',
    'CallerId' => '08045681174'
); 
$api_key     = "exotel905"; 
$api_token   = "102ea1c06725eedc481e93ea61df480c702b648b"; 
$exotel_sid  = "exotel905";
#Replace <subdomain> with the region of your account
#<subdomain> of Singapore cluster is @api.exotel.com
#<subdomain> of Mumbai cluster is @api.in.exotel.com 
$url = "https://" . $api_key .  ":"  . $api_token . "@api.exotel.com/v1/Accounts/" . $exotel_sid . "/Calls/connect"; 
$ch  = curl_init();
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_FAILONERROR, 0);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($post_data));
$http_result = curl_exec($ch);
curl_close($ch);
print "Response = ".print_r($http_result);
?>