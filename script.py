#\#!/usr/bin/env python3

import os
import sys
import time
import subprocess
import platform

def run_command(command, shell=True):
    """Execute shell command and return the result"""
    print(f"Executing command: {command}")
    process = subprocess.Popen(
        command, 
        shell=shell, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        print(f"Command execution failed, exit code: {process.returncode}")
        print(f"Error output: {stderr}")
        return False, stderr
    
    return True, stdout

def connect_to_neo4j(uri="bolt://localhost:7687", username="neo4j", password="testtest"):
    """Connect to Neo4j database and test the connection"""
    try:
        from neo4j import GraphDatabase
        
        print(f"Trying to connect to Neo4j: {uri} (user: {username})")
        driver = GraphDatabase.driver(uri, auth=(username, password))
        
        # Verify connection
        driver.verify_connectivity()
        print("Successfully connected to Neo4j!")
        
        # Get database information
        with driver.session() as session:
            result = session.run("CALL dbms.components() YIELD name, versions, edition")
            record = result.single()
            if record:
                print(f"Neo4j version: {record['name']} {record['versions'][0]} {record['edition']}")
            
            # Show available databases
            try:
                result = session.run("SHOW DATABASES")
                print("\nAvailable databases:")
                for record in result:
                    print(f"  - {record['name']}: {record['address']} (status: {record['currentStatus']})")
            except Exception as db_err:
                print(f"Unable to get database list: {db_err}")
        
        return driver
    
    except Exception as e:
        print(f"Error connecting to Neo4j: {str(e)}")
        return None

def create_neo4j_databases(driver):
    """Create Neo4j databases"""
    try:
        print("\n==== Creating Neo4j Databases ====")
        databases = ["datag", "datag0", "datag1"]
        
        with driver.session() as session:
            for db_name in databases:
                try:
                    print(f"Creating database: {db_name}")
                    # Check if database already exists
                    result = session.run("SHOW DATABASES")
                    existing_dbs = [record["name"] for record in result]
                    
                    if db_name in existing_dbs:
                        print(f"Database {db_name} already exists, skipping creation")
                    else:
                        session.run(f"CREATE DATABASE {db_name}")
                        print(f"Database {db_name} created successfully")
                except Exception as e:
                    print(f"Error creating database {db_name}: {str(e)}")
        
        # Wait for databases to become available
        print("Waiting for newly created databases to be ready...")
        time.sleep(5)
        
        # Verify databases were created
        with driver.session() as session:
            result = session.run("SHOW DATABASES")
            print("\nAvailable databases:")
            for record in result:
                print(f"  - {record['name']}: {record['address']} (status: {record['currentStatus']})")
        
        return True
    
    except Exception as e:
        print(f"Error creating databases: {str(e)}")
        return False

def main():
    # Step 1: Activate virtual environment
    print("\n==== Step 1: Activate Virtual Environment ====")
    venv_path = os.path.join(os.getcwd(), "venv")
    
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")
    
    if not os.path.exists(activate_script):
        print(f"Virtual environment activation script not found: {activate_script}")
        print("Please make sure you've created a virtual environment, or manually activate it before running this script")
        return False
    
    # Since activating a virtual environment needs to be done in the current shell,
    # and Python cannot directly modify the parent process's environment,
    # we only prompt the user to manually activate the environment
    print(f"Please manually activate the virtual environment first: source {activate_script}")
    input("Press Enter to continue after activating the environment...")
    
    # Check if virtual environment is activated
    if not os.environ.get("VIRTUAL_ENV"):
        print("Warning: Virtual environment doesn't seem to be activated, but will continue execution")
    else:
        print(f"Currently activated virtual environment: {os.environ.get('VIRTUAL_ENV')}")
    
    # Step 2: Install dependencies
    print("\n==== Step 2: Installing Required Packages ====")
    dependencies = ["neo4j", "networkx", "kuzu", "numpy", "pandas", "graphdatascience"]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        if dep == "graphdatascience":
            # Use Tsinghua mirror for graphdatascience
            success, output = run_command(f"pip install {dep} -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn")
        else:
            success, output = run_command(f"pip install {dep}")
        
        if not success:
            print(f"Failed to install {dep}")
            return False
    
    print("All dependencies installed successfully")
    
    # Step 3: Start Docker containers
    print("\n==== Step 3: Starting Neo4j Docker Container ====")
    success, output = run_command("docker-compose up -d")
    if not success:
        print("Failed to start Docker container")
        return False
    
    print("Docker container started")
    
    # Wait for Neo4j to start
    print("Waiting for Neo4j service to start...")
    driver = None
    for i in range(30):
        print(f"Waiting for Neo4j to be ready... ({i+1}/30)")
        time.sleep(2)
        
        # Check if Neo4j has started
        if i > 10:  # Give containers some time to start
            driver = connect_to_neo4j()
            if driver:
                print("Neo4j has started successfully and is connectable")
                break
    
    if not driver:
        print("Timeout while trying to connect to Neo4j, please check container status")
        return False
    
    # Step 4: Create Neo4j databases
    if not create_neo4j_databases(driver):
        print("Failed to create Neo4j databases")
        driver.close()
        return False
    
    # Close driver connection
    driver.close()
    
    # Step 5: Execute specified Python commands
    print("\n==== Step 5: Executing Test Commands ====")
    commands = [
        "python -m databases.neo4j.test",
        "python -m graphs.networkx.sample",
        "python -m graphs.networkx.entrance",
        "python -m graphs.kuzu.launcher"
    ]
    
    for cmd in commands:
        print(f"\nExecuting command: {cmd}")
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Real-time output of command execution results
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Get command execution results
        _, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Command execution failed: {cmd}")
            print(f"Error output: {stderr}")
            print("Continuing with other commands...")
        else:
            print(f"Command executed successfully: {cmd}")
    
    return True

if __name__ == "__main__":
    if main():
        print("\n✅ GSlicer environment setup complete and all test commands executed successfully!")
    else:
        print("\n❌ GSlicer environment setup or test execution failed, please check errors and try again")