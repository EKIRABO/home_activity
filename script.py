from fabric import Connection

SERVER_IP = "3.89.92.200"      
SERVER_USER = "ubuntu"                 
PRIVATE_KEY_PATH = "/home/esther_k/.ssh/esther_key"

DB_NAME = "alu_database"
DUMP_PATH = "/home/esther_k/SQL/mysql.sql"   


connection = Connection(
    host=SERVER_IP,
    user=SERVER_USER,
    connect_kwargs={
        "key_filename": PRIVATE_KEY_PATH
    }
)

def setup_mysql():
    print("Updating packages...")
    connection.run("sudo apt update -y", pty=True)

    print("Installing MySQL...")
    connection.run("sudo apt install -y mysql-server", pty=True)
    connection.run(
    f"sudo mysql -e \"DROP DATABASE IF EXISTS {DB_NAME};\"",
    pty=True
)

    connection.run(
    f"sudo mysql -e \"CREATE DATABASE {DB_NAME};\"",
    pty=True
)
    print("Uploading SQL dump...")
    connection.put("/home/esther_k/SQL/mysql.sql", "/tmp/mysql.sql")

    print("Importing SQL dump...")
    connection.run(
        f"sudo mysql {DB_NAME} < /tmp/mysql.sql",
        pty=True
    )

setup_mysql()
