import psycopg2
import sys

def calldetail(call_id):
    """
    Fetches and writes detailed call information for the given call_id
    from PostgreSQL tables: user_disposition_history, cm_cdr_history, and call_history.
    """

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="ameyodb",
        user="harsh.kumar",
        # password="your_password",
        # host="your_host",
        # port="5432"
    )
    cur = conn.cursor()
    file_name = f"{call_id}.txt"

    agent_data = []
    customer_data = []
    agent_cm_cdr_data = []
    customer_cm_cdr_data = []

    # -------------------------------- Agent Data --------------------------------
    user_disposition_query = f"SELECT * FROM user_disposition_history WHERE call_id='{call_id}';"
    cur.execute(user_disposition_query)
    agent_data = cur.fetchall()

    if agent_data:
        print("✅ Data found in user_disposition_history")
        agent_columns = [desc[0] for desc in cur.description]

        # Get agent call_leg_id
        cur.execute(user_disposition_query)
        agent_call_leg = cur.fetchone()
        agent_call_leg_id = agent_call_leg[3]

        # Fetch agent cm_cdr_history data
        if agent_call_leg_id:
            agent_cm_cdr_query = f"SELECT * FROM cm_cdr_history WHERE call_leg_id='{agent_call_leg_id}';"
            cur.execute(agent_cm_cdr_query)
            agent_cm_cdr_data = cur.fetchall()
            agent_cm_cdr_columns = [desc[0] for desc in cur.description]
        else:
            print("⚠️ No agent leg ID found in user_disposition_history.")
    else:
        print("❌ No data found in user_disposition_history for this call ID.")

    # ------------------------------ Customer Data ------------------------------
    call_history_query = f"SELECT * FROM call_history WHERE call_id='{call_id}';"
    cur.execute(call_history_query)
    customer_data = cur.fetchall()

    if customer_data:
        print("✅ Data found in call_history")
        customer_columns = [desc[0] for desc in cur.description]

        # Get customer call_leg_id
        cur.execute(call_history_query)
        customer_call_leg = cur.fetchone()
        customer_call_leg_id = customer_call_leg[1]

        # Fetch customer cm_cdr_history data
        if customer_call_leg_id:
            customer_cm_cdr_query = f"SELECT * FROM cm_cdr_history WHERE call_leg_id='{customer_call_leg_id}';"
            cur.execute(customer_cm_cdr_query)
            customer_cm_cdr_data = cur.fetchall()
            customer_cm_cdr_columns = [desc[0] for desc in cur.description]
        else:
            print("⚠️ No customer leg ID found in call_history.")
    else:
        print("❌ No data found in call_history for this call ID.")

    # --------------------------- Write to Output File --------------------------
    with open(file_name, "w") as f:
        f.write("------------ Agent: user_disposition_history ------------\n\n")
        if agent_data:
            for idx, row in enumerate(agent_data, 1):
                f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                for col, val in zip(agent_columns, row):
                    f.write(f"{col:<20}: {val}\n")
                f.write("\n")
        else:
            f.write("No data in user_disposition_history for this call ID\n\n")

        f.write("------------ Agent: cm_cdr_history ------------\n\n")
        if agent_cm_cdr_data:
            for idx, row in enumerate(agent_cm_cdr_data, 1):
                f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                for col, val in zip(agent_cm_cdr_columns, row):
                    f.write(f"{col:<20}: {val}\n")
                f.write("\n")
        else:
            f.write("No cm_cdr_history data for agent leg\n\n")

        f.write("------------ Customer: call_history ------------\n\n")
        if customer_data:
            for idx, row in enumerate(customer_data, 1):
                f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                for col, val in zip(customer_columns, row):
                    f.write(f"{col:<20}: {val}\n")
                f.write("\n")
        else:
            f.write("No call_history data for this call ID\n\n")

        f.write("------------ Customer: cm_cdr_history ------------\n\n")
        if customer_cm_cdr_data:
            for idx, row in enumerate(customer_cm_cdr_data, 1):
                f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
                for col, val in zip(customer_cm_cdr_columns, row):
                    f.write(f"{col:<20}: {val}\n")
                f.write("\n")
        else:
            f.write("No cm_cdr_history data for customer leg\n\n")

    # Cleanup
    cur.close()
    conn.close()


# --------------------------- Command-Line Execution ---------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py calldetail <call_id>")
        sys.exit(1)

    command = sys.argv[1]
    callsid = sys.argv[2]

    if command == "calldetail":
        calldetail(callsid)
    else:
        print("❌ Invalid command. Only 'calldetail' is supported.")
