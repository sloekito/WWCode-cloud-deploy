# WWCode Workshop: Deploying Your First Full Stack Application to the Cloud

## Install Prerequisites

### AWS Free Tier Account (requires credit card to sign up)

https://aws.amazon.com/free/

For this workshop, we will stay within the free tier so you won't get charged


### Python 3
##### MacOS: 

If you don't already have python installed:
https://www.python.org/downloads/mac-osx/

##### Windows: 

https://www.python.org/downloads/windows/

Follow these instructions:

https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation


To confirm installation works, on your terminal window, type:

```bash
python
```

### PIP (Python Package Index)
##### MacOS: 

On your terminal window, type:

```bash
curl https://bootstrap.pypa.io/ez_setup.py -o - | sudo python
sudo easy_install pip
```

##### Windows: 

Follow these instructions:

https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation


To confirm installation works, on your terminal window, type:

```bash

pip
```


### mysql connector

On your terminal window, type:

```bash
pip install mysql-connector```


### boto3 (AWS SDK for Python, which allows Python developers to write software that makes use of Amazon services like S3 and EC2)

On your terminal window, type:

```bash
pip install boto3```

More info: http://boto3.readthedocs.io/en/latest/

### AWS CLI (Open source tool built on top of the AWS SDK for Python (Boto) that provides commands for interacting with AWS services.)

On your terminal window, type:


```bash
pip install awscli --upgrade --user```

More info: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html

### Setup your AWS Credentials


1. Open AWS Console, go to "Identity and Access Management" to pen the IAM console.

1. In the navigation pane of the console, choose Users.

1. Choose your IAM user name (not the check box).

1. Choose the Security credentials tab and then choose Create access key.

1. To see the new access key, choose Show. Your credentials will look something like this:

    ```
    Access key ID: AKIAIOSFODNN7EXAMPLE
    Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    To download the key pair, choose Download .csv file. Store the keys in a secure location.
    ```

1. On your terminal window, type:
```bash
aws configure --profile workshop
```
When prompted for keys, copy paste the credentials you saved above. As an example:

```
AWS Access Key ID [None]: AKIAI44QH8DHBEXAMPLE
AWS Secret Access Key [None]: je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: text
```

If setup correctly, type:

```bash
more ~/.aws/credentials

```

You should see the following:
```
[workshop]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

More info here:

http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html


### Git client (for cloning this repo)
##### MacOS and Windows: 

https://git-scm.com/downloads


### Clone this repo

On your terminal window, type:
```bash
git clone https://github.com/sloekito/WWCode-cloud-deploy.git
```


## Optional Installation

### SSH Client

##### Windows:

Download from http://www.putty.org/

##### MacOS:

Should already have ssh

Alternatively, you can try the ssh client on Chrome Browser: https://chrome.google.com/webstore/detail/secure-shell/pnhechapfaindjhompbnflcldabbghjo?hl=en


### MySQL Client

##### Windows:
https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-6.3.9-winx64.msi

##### MacOS:
https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-6.3.9-osx-x86_64.dmg

### Python Flask

```bash
pip install Flask```
