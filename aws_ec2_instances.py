#!/usr/bin/env python

import boto3, botocore.exceptions
import argparse
import logging
from operator import itemgetter

def main(args):
    
    logging.debug('Tag: %s', args.tag)
    logging.debug('Region: %s', args.region)
    
    boto3.setup_default_session(region_name=args.region)
    
    ec2 = boto3.client('ec2')
    
    instances = getInstancesjson(ec2,args.tag)
    
    for instance in instances:
        print(instance)
    
    return 0

def getInstancesjson(ec2,tag_key):
    
    instances = [ ]
    
    describe_instances = ec2.describe_instances()
    
    for reservation in describe_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_details = {
                "InstanceId": instance['InstanceId'],
                "InstanceType": instance['InstanceType'],
                "LaunchTime": str(instance["LaunchTime"])
            }
            
            for tag in instance['Tags']:
                if tag_key in tag['Key']:
                    instance_details[tag_key] = tag['Value']
                    break
                    
                else: 
                    instance_details[tag_key] = 'unknown'
        
        instances.append(instance_details)
    
    return sorted(instances,key=itemgetter(tag_key))
    
def parseArgs():
    
    parser = argparse.ArgumentParser(description='Describe AWS EC2 instances in a given account')
    parser.add_argument('--tag',  type=str, default="Owner", help='Specify a tag. Default is Owner')
    parser.add_argument('--region',  type=str, default="us-east-1", help='Specify an AWS region. Default is us-east-1')
    #parser.add_argument('--AWS_KEY',  type=str, help='Specify an AWS key.'')
    #parser.add_argument('--AWS_SECRET',  type=str, help='Specify an AWS key secret')

    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
                     
    args = parser.parse_args()
    
    return args
    
if __name__ == "__main__":
    
    args = parseArgs()
    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    if(args.verbose):
        logging.getLogger().setLevel('DEBUG')
        logging.info('Log level set to DEBUG')
    else:
        logging.getLogger().setLevel('ERROR')

    main(args)
    
    