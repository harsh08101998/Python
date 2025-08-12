import psycopg2
import sys

def run_query(cur, query):
    cur.execute(query)
    return cur.fetchall(), [desc[0] for desc in cur.description] if cur.description else []

def write_records_to_file(f, header, columns, data):
    f.write(f"------------ {header} ------------\n\n")
    if data:
        for idx, row in enumerate(data, 1):
            f.write(f"-[ RECORD {idx} ]" + "-" * 30 + "\n")
            for col, val in zip(columns, row):
                f.write(f"{col:<25}: {val}\n")
            f.write("\n")
    else:
        f.write(f"No data found for {header}.\n\n")

def analyze_call_data(agent_data, agent_cm_cdr_data, customer_data, customer_cm_cdr_data,
                      agent_columns, agent_cm_cdr_columns, customer_columns, customer_cm_cdr_columns):
    print("\n🔍 ANALYSIS REPORT")
    if agent_data:
        wrap_time = agent_data[0][agent_columns.index("wrap_time")]
        talk_time = agent_data[0][agent_columns.index("talk_time")]
        print(f"🕒 Agent Wrap Time: {wrap_time} ms")
        print(f"🗣️ Agent Talk Time: {talk_time} ms")

    if agent_cm_cdr_data:
        hangup_cause = agent_cm_cdr_data[0][agent_cm_cdr_columns.index("hangup_cause")]
        print(f"📞 Agent Hangup Cause: {hangup_cause}")

    if customer_data:
        call_result = customer_data[0][customer_columns.index("call_result")]
        hangup_detail = customer_data[0][customer_columns.index("hangup_details")]
        print(f"🎯 Call Result: {call_result}")
        print(f"📴 Hangup Detail: {hangup_detail}")

    if customer_cm_cdr_data:
        talk_time = customer_cm_cdr_data[0][customer_cm_cdr_columns.index("talk_time")]
        print(f"🗣️ Customer Talk Time: {talk_time} ms")

def calldetail(call_id):
    conn = psycopg2.connect(
        dbname="ameyodb",
        user="harsh.kumar"
    )
    cur = conn.cursor()
    file_name = f"{call_id}.txt"

    user_disposition_query = f"SELECT * FROM user_disposition_history WHERE call_id='{call_id}';"
    agent_data, agent_columns = run_query(cur, user_disposition_query)
    agent_call_leg_id = agent_data[0][agent_columns.index("call_leg_id")] if agent_data else None

    agent_cm_cdr_data, agent_cm_cdr_columns = ([], [])
    if agent_call_leg_id:
        agent_cm_cdr_query = f"SELECT * FROM cm_cdr_history WHERE call_leg_id='{agent_call_leg_id}';"
        agent_cm_cdr_data, agent_cm_cdr_columns = run_query(cur, agent_cm_cdr_query)

    call_history_query = f"SELECT * FROM call_history WHERE call_id='{call_id}';"
    customer_data, customer_columns = run_query(cur, call_history_query)
    customer_call_leg_id = customer_data[0][customer_columns.index("call_leg_id")] if customer_data else None

    customer_cm_cdr_data, customer_cm_cdr_columns = ([], [])
    if customer_call_leg_id:
        customer_cm_cdr_query = f"SELECT * FROM cm_cdr_history WHERE call_leg_id='{customer_call_leg_id}';"
        customer_cm_cdr_data, customer_cm_cdr_columns = run_query(cur, customer_cm_cdr_query)

    with open(file_name, "w") as f:
        write_records_to_file(f, "Agent: user_disposition_history", agent_columns, agent_data)
        write_records_to_file(f, "Agent: cm_cdr_history", agent_cm_cdr_columns, agent_cm_cdr_data)
        write_records_to_file(f, "Customer: call_history", customer_columns, customer_data)
        write_records_to_file(f, "Customer: cm_cdr_history", customer_cm_cdr_columns, customer_cm_cdr_data)

    analyze_call_data(agent_data, agent_cm_cdr_data, customer_data, customer_cm_cdr_data,
                      agent_columns, agent_cm_cdr_columns, customer_columns, customer_cm_cdr_columns)

    cur.close()
    conn.close()

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
