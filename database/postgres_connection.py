import psycopg2, sys


def calldetail(callsid):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="ameyodb",
        user="harsh.kumar",
        # password="your_password",
        # host="10.5.5.50",
        # host='144.24.127.232'
        # port="5432"
    )

    # d425-68342e3b-vcall-0

    # call_id=str(input("Please enter call-id :    "))
    call_id=callsid
    cur = conn.cursor()
    file_name=call_id+".txt"

    agent_data=0
    customer_data=0
    customer_cm_cdr_data=0
    agent_cm_cdr_data=0

    ############################################################## agent date query ###########################################################
    user_disposition_history_query="SELECT * FROM user_disposition_history where call_id='{}';".format(call_id)
    cur.execute(user_disposition_history_query)
    # print(user_disposition_history_query)
    # agent_call_leg=cur.fetchone()
    agent_data = cur.fetchall()

    if agent_data:
        print("Data present in user_dispostion_history table")


        agent_columns = [desc[0] for desc in cur.description]
        cur.execute(user_disposition_history_query)
        agent_call_leg=cur.fetchone()
        agent_call_leg_id=agent_call_leg[3]
        if agent_call_leg_id:
        ####################### agent cm_cdr_histoery data #######################################
            agent_cm_cdr_query="select * from cm_cdr_history  where call_leg_id='{}';".format(agent_call_leg_id)
            cur.execute(agent_cm_cdr_query)
            agent_cm_cdr_data = cur.fetchall()
            agent_cm_cdr_columns = [desc[0] for desc in cur.description]
        else:
            print("Data not present in cm_cdr_history for agent leg")
    else :
        print('data is not present in user_dispostion_history table for this callsid')



    ######################################################### customer query ###########################################################

    call_history_query="select * from call_history where call_id='{}';".format(call_id)
    cur.execute(call_history_query)
    # customer_call_leg=cur.fetchone()
    customer_data = cur.fetchall()
    if customer_data:
        print("Data present in call_history table")


        # customer_data = cur.fetchall()

        customer_columns = [desc[0] for desc in cur.description]
        cur.execute(call_history_query)
        customer_call_leg=cur.fetchone()
        customer_call_leg_id=customer_call_leg[1]
        ####################### agent cm_cdr_histoery data #######################################
        if customer_call_leg_id:
            print(customer_call_leg_id)
            customer_cm_cdr_query="select * from cm_cdr_history  where call_leg_id='{}';".format(customer_call_leg_id)
            cur.execute(customer_cm_cdr_query)
            customer_cm_cdr_data = cur.fetchall()
            customer_cm_cdr_columns = [desc[0] for desc in cur.description]
        else:
            print("Data not present in cm_cdr_history for customer leg")

    else:
        print("Data not present in call_history table")



    # Write in expanded display mode like \x
    with open(file_name, "w") as f:
        f.write("--------------------------------------- user_disposition_data (agent data) ------------------------------------------ \n\n")
        if agent_data!=0:
            for idx, row in enumerate(agent_data, 1):
                f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                for col, val in zip(agent_columns, row):
                    f.write(f"{col:<20}: {val}\n")
                f.write("\n")


            f.write("-------------------------------------------- Agent cm_cdr_history data  ------------------------------------------------------------------------ \n\n")
            if agent_cm_cdr_data!=0:

                for idx, row in enumerate(agent_cm_cdr_data, 1):
                    f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                    for col, val in zip(agent_cm_cdr_columns, row):
                        f.write(f"{col:<20}: {val}\n")
                    f.write("\n")
            else:
                f.write("Data not present in cm_cdr_history for agent leg")


        else:
            f.write("data is not present in user_dispostion_history table for this callsid\n\n")

        if customer_data!=0:

            # print(customer_data)
            f.write("-------------------------------------------- call_history_data (customer data)  ------------------------------------------------------------------------ \n\n")

            for idx, row in enumerate(customer_data, 1):
                f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                for col, val in zip(customer_columns, row):
                    f.write(f"{col:<20}: {val}\n")
                f.write("\n")

            f.write("-------------------------------------------- Customer cm_cdr_history data  ------------------------------------------------------------------------ \n\n")
            if customer_cm_cdr_data!=0:
                for idx, row in enumerate(customer_cm_cdr_data, 1):
                    f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                    for col, val in zip(customer_cm_cdr_columns, row):
                        f.write(f"{col:<20}: {val}\n")
                    f.write("\n")
            else:
                f.write("Data not present in cm_cdr_history for customer leg")

        else:
            f.write("Data not present in call_history table")

    cur.close()
    conn.close()

callsid=sys.argv[2]
command_list=['calldetail']
command=str(sys.argv[1])

if command in command_list:

    if str(command)==command_list[0]:
        calldetail(str(callsid))

    else:
        print("Something is wrong in Calldetail command")

else:
    print("Given command is not present")
