import boto3, botocore
import argparse
import os
from string import Template


def create_s3_bucket(aws_cf_client, cf_stack_name, s3_bucket_name, cft_file):
    """
    Creates an s3 bucket if it does not already exist
    Updates the bucket if it already exists
    Parameter description:
        aws_cf_client: the client connection to AWS API
        cf_stack_name: the Cloud Formation stack name
        s3_bucket_name: the s3 bucket name we are creating. Must be globally unique
        cft_file: cloud formation template used to create the s3 bucket
    """

    cf_parameters = [
        {"ParameterKey": "BucketName", "ParameterValue": s3_bucket_name}
    ]

    try:
        if _stack_exists(cf_stack_name, aws_cf_client):
            print('Updating {}'.format(cf_stack_name))
            # stack_result = aws_cf_client.update_stack(cf_params)
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
            # stack_result = aws_cf_client.create_stack(cf_params)
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

def upload_files_to_s3(s3_client, s3_bucket_name, static_file_dir):
    """
    Upload a file to the s3 bucket and make it public-read.
    Parameter description:
        s3_bucket_name: the s3 bucket to upload to
        file_name: the file name to upload to the s3 bucket. Example: "index.html"
    """
    for file_name in os.listdir(static_file_dir):

        static_file_name = os.path.join(static_file_dir, file_name)
        print("Uploading " + static_file_name + " to " + s3_bucket_name)

        # Upload a new file
        data = open(static_file_name, 'rb')
        try:
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key=file_name,
                ACL = 'public-read',
                Body=data,
                ContentType='text/html')

        except Exception as e:
            print(e)

    
def _stack_exists(stack_name, aws_cf_client):
    stacks = aws_cf_client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

def substitute_templates(template_file_dir, static_file_dir, mapping):
    # Perform template string substitution 
    # mapping contains a key-value pair of strings to be substituted
    # For example,
    # ./template/index.html will be substituted and the result will be written to  ./static/index.thml

    for file_name in os.listdir(template_file_dir):
        template_file_name = os.path.join(template_file_dir, file_name)

        with open(template_file_name, 'r') as template_file:
            template = Template(template_file.read())
            result = template.substitute(mapping)
            # index.html.template will be
            static_file_name = os.path.join(static_file_dir, file_name)
            with open(static_file_name, "w") as fileout:
                fileout.write(result)
      

    # d={ "api_host_ip": "34.210.54.118" }

    # with open("./template/index.html.template", 'r') as filein:
    #     template = Template(filein.read())
    #     result = template.substitute(d)
    #     with open("./static/index.html", "w") as fileout:
    #         fileout.write(result)

def get_stack_output(aws_cf_client, stack_name):
    describe_stack = aws_cf_client.describe_stacks(StackName=stack_name)
    print(describe_stack)

    stacks = describe_stack["Stacks"]

    out_dict = {}
    for stack in stacks:
        for outputs in stack["Outputs"]:
            out_dict[outputs["OutputKey"]] = outputs["OutputValue"]
    
    return out_dict

def main():
    parser = argparse.ArgumentParser(description='Deployment Arguments')
    parser.add_argument("--stack_name", help="the Cloud Formation stack name to be created", required=True)
    parser.add_argument("--s3_bucket_name", help="the mysql host name", required=True)
    parser.add_argument("--middleware_stack_name", help="The middleware stack name. Used to get the IP address of the middleware EC2 host", required=True)

    args = parser.parse_args()
    stack_name = args.stack_name
    s3_bucket_name = args.s3_bucket_name
    middleware_stack_name = args.middleware_stack_name

    session = boto3.Session(profile_name='workshop', region_name='us-west-2')

    aws_cf_client = session.client('cloudformation')
    s3_client = session.client('s3')

    # mapping = { "api_host_ip": "34.210.54.118" }

    middleware_stack_output = get_stack_output(aws_cf_client=aws_cf_client, stack_name=middleware_stack_name)

    print(middleware_stack_output)

    catalog_api_url = middleware_stack_output.get("CatalogApiURL")

    mapping = { "catalog_api_url": catalog_api_url }


    # Create s3 bucket with the supplied arguments
    create_s3_bucket(aws_cf_client=aws_cf_client, 
                        cf_stack_name=stack_name, 
                        s3_bucket_name=s3_bucket_name, 
                        cft_file="catalog-frontend.yaml")


    # Replace the connection string in file
    substitute_templates(template_file_dir="./template",
                        static_file_dir="./static",
                        mapping=mapping)

    upload_files_to_s3(s3_client=s3_client, 
                        s3_bucket_name=s3_bucket_name, 
                        static_file_dir="./static")

if __name__ == '__main__':
    main()
