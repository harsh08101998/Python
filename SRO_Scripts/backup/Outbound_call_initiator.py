import subprocess
import json

value=2
# 08045243232 :- cf2436d06764f7f0f749306f372c197m
# 08045246232 :- 73c3a6010c8e10ef0779697cb5a8197m
# 08045243732 :- cf5eb291659d8b08ef6eb5a92da1197m
# Error: 08044620202 :- None Response: {"RestException":{"Status":503,"Message":"Service Unavailable; ","Code":35008}}
if value==1:
    # number1='07969083502'

    number1='08045243232'
    number2='08045246232'
    number3='08045243732'
    number4='08044620202'
    number5='08047359899'
    number6='08062314002'
    number7='08062322702'
    number8='08035730092'
    number9='08035009097'
    number10='08035273380'
    number11='08037905006'
    number12='08037902504'
    number13='08038024002'
    number14='09513963739'


    def make_exotel_call_subprocess():
        """Make call using subprocess curl"""
        numberr=number6


        curl_command = [
            'curl', '-X', 'POST',
            'https://exotelt:eb9132081dad84d938f207227c8a7e26467cbbeb5ed1151b@api.exotel.com/v1/Accounts/exotelt/Calls/connect.json',
            # 'https://exotel1248:39e0f50e4c14e37465133f1ce0c4521ce71e3472@api.exotel.com/v1/Accounts/exotel1248/Calls/connect.json',
            '-d', 'From=08570027091',
            '-d', f'CallerId={numberr}',
            '-d', 'To=08930256409',
            '-d', '__RequestedServerCode=080_32',
            '-d', '__IgnoreServerStatus=true',
            '-d', 'Record=true'
        ]
        # print(curl_command)
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True)

            if result.returncode == 0:

                # print("Call initiated successfully")
                print(f"Response: {result.stdout}")
                try:
                    call_data=json.loads(result.stdout)
                    call_sid = call_data["Call"]["Sid"]
                    print(f"{numberr} :- {call_sid}")
                except Exception as e:
                    print(f"Error: {numberr} ")
                    return None
                return result.stdout
            else:
                print(f"Error: {result.stderr}")
                return None

        except Exception as e:
            print(f"Error making call: {e}")
            return None

    # Usage
    result = make_exotel_call_subprocess()



if value==2:
    number1='01585580232'
    # number1='01585580231'
    number1='01585580246'

    def make_exotel_call_subprocess():
        """Make call using subprocess curl"""

        curl_command = [
            'curl', '-X', 'POST',
            'https://exotel1895:6c3a6eefed8a3c80742a5f75c23585e2ed334272@api.exotel.com/v1/Accounts/exotel1895/Calls/connect.json',
            '-d', 'From=sip:harshk3fa0b97d',
            '-d', f'CallerId={number1}',
            '-d', 'To=sip:vivekk701c3a50',
            '-d', '__RequestedServerCode=oci_telephonix_01',
            '-d', '__IgnoreServerStatus=true',
            '-d', 'Record=true'  ]


            # print(curl_command)
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True)

            if result.returncode == 0:

                print("Call initiated successfully")
                print(f"Response: {result.stdout}")
                return result.stdout
            else:
                print(f"Error: {result.stderr}")
                return None

        except Exception as e:
            print(f"Error making call: {e}")
            return None

    # Usage
    result = make_exotel_call_subprocess()