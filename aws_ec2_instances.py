#!/usr/bin/env python

import boto3, botocore.exceptions
import argparse
import logging
import sys
import re
import json
from operator import itemgetter

def main(args):
    
    # Set the region, --region will override. If no override and not specified in AWS_REGION input, type is None defulting to local AWS profile setting.
    if args.region:
        region = args.region
    else:
        region = args.AWS_REGION
    
    # Define AWS profile. If no specific params are passed at command line AWS_KEY and AWS_SECRET are type None, defaulting to local aws profile
    ec2 = boto3.client('ec2',region_name=region,aws_access_key_id=args.AWS_KEY,aws_secret_access_key=args.AWS_SECRET)
    
    instances = getInstancesjson(ec2,args.tag)
    
    # Print the output
    output(instances)
    
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
            
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag_key in tag['Key']:
                        instance_details[tag_key] = tag['Value']
                        break
                        
                    else: 
                        instance_details[tag_key] = 'unknown'
            else:
                instance_details[tag_key] = 'unknown'
        
            instances.append(instance_details)
   
    return sorted(instances,key=itemgetter(tag_key))
    
def output(instances):
    
    for instance in instances:
        print(instance)
    
def parseArgs():

    parser = argparse.ArgumentParser(description='Describe AWS EC2 instances in a given account')   
    
    # Set to optional, use default profile if not specified. Can specify region only with --region flag  
    parser.add_argument('AWS_KEY',  type=str, nargs='?', help='Specify an AWS key.', default=None)
    parser.add_argument('AWS_SECRET',  type=str, nargs='?',  help='Specify an AWS key secret', default=None) 
    parser.add_argument('AWS_REGION',  type=str, nargs='?', default='us-east-1', help='Specify an AWS region. Default is us-east-1')

    parser.add_argument('--tag',  type=str, default="Owner", help='Specify a tag. Default is Owner')
    
    # Allow for region specificity only, no input creds, use aws profile stored
    parser.add_argument('--region',  type=str, nargs='?', help='Specify a region. Default is us-east-1')

    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
                     
    args = parser.parse_args()
    
    return args
    
if __name__ == "__main__":
    
    args = parseArgs()
    args.cmdLine = sys.argv
    
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    if(args.verbose):
        logging.getLogger().setLevel('DEBUG')
        logging.info('Log level set to DEBUG')
    else:
        logging.getLogger().setLevel('ERROR')

    main(args)
    
    