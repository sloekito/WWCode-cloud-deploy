import boto3, botocore
import argparse

def create_ec2_catalog_web(aws_cf_client, stack_name, db_hostname, db_user, db_password, db_name, cft_file):
    """
    Creates the ec2 instance that contains our web application
    AMI:
    Keyname:
    """

    cf_parameters = [
        {"ParameterKey": "DBHostName", "ParameterValue": db_hostname},
        {"ParameterKey": "DBUser", "ParameterValue": db_user},
        {"ParameterKey": "DBPassword", "ParameterValue": db_password},
        {"ParameterKey": "DBName", "ParameterValue": db_name},
        {"ParameterKey": "ImageId", "ParameterValue": "ami-e689729e" },
        {"ParameterKey": "KeyName", "ParameterValue": "wwcode"}
    ]
    print(cf_parameters)

    try:
        if _stack_exists(stack_name, aws_cf_client):
            print('Updating {}'.format(stack_name))
            with open(cft_file, 'r') as template:
                response = aws_cf_client.update_stack(
                    StackName=stack_name,
                    TemplateBody=template.read(),
                    Parameters=cf_parameters            
                )
                waiter = aws_cf_client.get_waiter('stack_create_complete')

            waiter = aws_cf_client.get_waiter('stack_update_complete')
        else:
            print('Creating {}'.format(stack_name))
            with open(cft_file, 'r') as template:
                response = aws_cf_client.create_stack(
                    StackName=stack_name,
                    TemplateBody=template.read(),
                    Parameters=cf_parameters,
                    DisableRollback=True
                )
                waiter = aws_cf_client.get_waiter('stack_create_complete')

        print("...waiting for stack to be ready...")
        waiter.wait(StackName=stack_name)
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


def main():
    
    parser = argparse.ArgumentParser(description='Deployment Arguments')
    parser.add_argument("--stack_name", help="the cloud formation stack name", required=True)
    parser.add_argument("--db_hostname", help="the mysql host name", required=True)
    parser.add_argument("--db_user", help="the mysql user", required=True)
    parser.add_argument("--db_password", help="the mysql password", required=True)
    parser.add_argument("--db_name", help="the mysql db name", required=True)

    args = parser.parse_args()

    session = boto3.Session(profile_name='workshop', region_name='us-west-2')

    aws_cf_client = session.client('cloudformation')

    stack_name = args.stack_name
    db_hostname = args.db_hostname
    db_user = args.db_user
    db_password = args.db_password
    db_name = args.db_name

    # Get the DB Hostname from DB Cloud Formation Stack
    # get_db_hostname()

    create_ec2_catalog_web(aws_cf_client=aws_cf_client, 
        stack_name=stack_name, 
        db_hostname=db_hostname,
        db_user=db_user,
        db_password=db_password,
        db_name=db_name,
        cft_file="catalog-web.yaml")

if __name__ == '__main__':
    main()
