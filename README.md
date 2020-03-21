# AWS EC2 Describe Instances

This tool provides detailed information regarding EC2 instances in a specified account.

## Usage

You can provide specific AWS credentials to use, if AWS_KEY, AWS_SECRET, and AWS_REGION are left blank the script will default to your local AWS profile (if setup).

`aws_ec2_instances.py -h`

```
usage: aws_ec2_instances.py [-h] [--tag TAG] [--region [REGION]]
                            [--output [{csv,json}]] [--fields [FIELDS]] [-v]
                            [AWS_KEY] [AWS_SECRET] [AWS_REGION]

Describe AWS EC2 instances in a given account

positional arguments:
  AWS_KEY               Specify an AWS key.
  AWS_SECRET            Specify an AWS key secret
  AWS_REGION            Specify an AWS region. Default is us-east-1

optional arguments:
  -h, --help            show this help message and exit
  --tag TAG             Specify a tag. Default is Owner
  --region [REGION]     Specify a region to override. Default is us-east-1
  --output [{csv,json}]
                        Specify an output format: CSV or JSON. Default is csv.
  --fields [FIELDS]     Specify additional fields to display about the EC2
                        instances. Input is comma-separated values in string
  -v, --verbose         Increase output verbosity

```

## Ouput 

### CSV

```
id,Owner,instance_type,ImageId,launch_time
i-000000,Joe,t2.micro,ami-0fc61db8544a617ed,2020-01-17 11:52:37+00:00
i-000001,Bob,t2.micro,ami-0fc61db8544a617ed,2020-01-17 11:52:37+00:00
i-000002,Carl,t2.micro,ami-0fc61db8544a617ed,2020-01-17 11:52:37+00:00
i-000003,unknown,t2.micro,ami-0fc61db8544a617ed,2020-01-17 11:52:37+00:00
i-000004,unknown,t2.micro,ami-0fc61db8544a617ed,2020-01-17 11:52:37+00:00
```

### JSON

```
{'launch_time': '2020-01-17 11:52:37+00:00', 'ImageId': 'ami-0fc61db8544a617ed', 'instance_type': 't2.micro', 'Owner': 'Joe', 'id': 'i-000000'}
{'launch_time': '2020-01-17 11:52:37+00:00', 'ImageId': 'ami-0fc61db8544a617ed', 'instance_type': 't2.micro', 'Owner': 'Bob', 'id': 'i-000001'}
{'launch_time': '2020-03-17 11:52:37+00:00', 'ImageId': 'ami-0fc61db8544a617ed', 'instance_type': 't2.micro', 'Owner': 'Carl', 'id': '000002'}
{'launch_time': '2020-03-17 11:52:37+00:00', 'ImageId': 'ami-0fc61db8544a617ed', 'instance_type': 't2.micro', 'Owner': 'unknown', 'id': '000003'}
{'launch_time': '2020-03-17 11:52:37+00:00', 'ImageId': 'ami-0fc61db8544a617ed', 'instance_type': 't2.micro', 'Owner': 'unknown', 'id': '000004'}

```