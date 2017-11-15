import boto3, botocore
import mysql.connector
import argparse

def create_db(aws_cf_client, cf_stack_name, cft_file, db_admin_user, db_admin_password):
    """
    Creates a RDS MySQL Table that contains our catalog 
    Updates the table if it already exists
    Parameter description:
        aws_cf_client: the client connection to AWS API
        cf_stack_name: the Cloud Formation stack name
        cft_file: cloud formation template used to create the MySQL table
        db_admin_user: the database admin username
        db_admin_password: the database admin password 
    """

    cf_parameters = [
        {"ParameterKey": "DBName", "ParameterValue": "catalog"},
        {"ParameterKey": "DBAdminUser", "ParameterValue": db_admin_user},
        {"ParameterKey": "DBAdminPassword", "ParameterValue": db_admin_password}
    ]

    try:
        if _stack_exists(cf_stack_name, aws_cf_client):
            print('Updating {}'.format(cf_stack_name))
            with open(cft_file, 'r') as template:
                response = aws_cf_client.update_stack(
                    StackName=cf_stack_name,
                    TemplateBody=template.read(),
                    Parameters=cf_parameters
                )
                waiter = aws_cf_client.get_waiter('stack_create_complete')

            waiter = aws_cf_client.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(cf_stack_name))
            with open(cft_file, 'r') as template:
                response = aws_cf_client.create_stack(
                    StackName=cf_stack_name,
                    TemplateBody=template.read(),
                    Parameters=cf_parameters
                )
                waiter = aws_cf_client.get_waiter('stack_create_complete')

        print("...waiting for stack to be ready...")
        waiter.wait(StackName=cf_stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise

def _stack_exists(stack_name, aws_cf_client):
    stacks = aws_cf_client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

                                   
def seed_db(sql_file, db_hostname, db_admin_user, db_admin_password):
    print("Seeding host: " + db_hostname)
    try:
        cnx = mysql.connector.connect(user=db_admin_user, 
                                password=db_admin_password,
                                host=db_hostname)
        cursor = cnx.cursor()

        with open(sql_file, 'r') as sql_file:
            sqlCommands = sql_file.read().split(';')

            for command in sqlCommands:
                print(command)
                if command.strip() != '':
                    cursor.execute(command)
                    cnx.commit()

    except Exception as e:
        print(e)
    finally:
        cnx.close()

def get_stack_output(aws_cf_client, stack_name):
    describe_stack = aws_cf_client.describe_stacks(StackName=stack_name)
    print('Stack Output {}'.format(describe_stack))

    stacks = describe_stack["Stacks"]
    out_dict = {}
    for stack in stacks:
        for outputs in stack["Outputs"]:
            out_dict[outputs["OutputKey"]] = outputs["OutputValue"]
    
    return out_dict


def main():
    parser = argparse.ArgumentParser(description='Deployment Arguments')
    parser.add_argument("--stack_name", help="The Cloud Formation stack name to be created", required=True)
    parser.add_argument("--db_admin_user", help="the mysql user", required=True)
    parser.add_argument("--db_admin_password", help="the mysql password", required=True)
    parser.add_argument("--db_name", help="the mysql db name", required=True)

    args = parser.parse_args()

    stack_name = args.stack_name
    db_admin_user = args.db_admin_user
    db_admin_password = args.db_admin_password

    session = boto3.Session(profile_name='workshop', region_name='us-west-2')
    aws_cf_client = session.client('cloudformation')


    # Create the database server
    create_db(aws_cf_client=aws_cf_client, 
            cf_stack_name=stack_name, 
            cft_file="catalog-db.yaml",
            db_admin_user=db_admin_user,
            db_admin_password=db_admin_password)

    # Get the database hostname created by cloudformation
    db_stack_output = get_stack_output(aws_cf_client=aws_cf_client, stack_name=stack_name)
    db_hostname = db_stack_output["RDSEndpoint"]
    print("The database hostname is: " + db_hostname)

    # Seed the database with catalog data
    seed_db(sql_file="catalog-db.sql", 
            db_hostname=db_hostname, 
            db_admin_user=db_admin_user, 
            db_admin_password=db_admin_password)

if __name__ == '__main__':
    main()
