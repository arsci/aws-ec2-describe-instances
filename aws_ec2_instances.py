#!/usr/bin/env python

import boto3
import argparse
import logging
from operator import itemgetter
import json

def main(args):
    
    # Set the region, --region will override. If no override and not specified in AWS_REGION input, type is None defulting to local AWS profile setting.
    logging.info('Setting region')
    if args.region:
        region = args.region
    else:
        region = args.AWS_REGION
    
    # Define AWS profile. If no specific params are passed at command line AWS_KEY and AWS_SECRET are type None, defaulting to local aws profile
    ec2 = boto3.client('ec2',region_name=region,aws_access_key_id=args.AWS_KEY,aws_secret_access_key=args.AWS_SECRET)
    
    instances = getInstancesjson(ec2,args.tag,args.fields)
    
    # Print the output
    output(instances,args.output)
    
    logging.info('Done')
    
    return 0

def getInstancesjson(ec2,tag_key,fields):
    
    instances = [ ]
    
    describe_instances = ec2.describe_instances()
    
    for reservation in describe_instances['Reservations']:
        for instance in reservation['Instances']:
           
            # Collect instanceid, type, and launch time
            logging.info('Building instance details for ' + instance['InstanceId'])
            instance_details = {
                "id": instance['InstanceId'],
                "instance_type": instance['InstanceType'],
                "launch_time": str(instance["LaunchTime"])
            }
            
            # Handle Owner tag (or other specified tag by --tag flag)
            logging.info('Building tag info for ' + tag_key + ' tag for ' + instance['InstanceId'])
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag_key in tag['Key']:
                        instance_details[tag_key] = tag['Value']
                        break
                    else: 
                        instance_details[tag_key] = 'unknown'
            else:
                instance_details[tag_key] = 'unknown'
                
            # Handle additional fields (specified by --fields flag)
            logging.info('Building additional fields for ' + instance['InstanceId'])
            if fields:
                fieldArr = fields.split(',')
                for field in fieldArr:
                    # Handle string and JSON objects in additional fields
                    if(isinstance(instance[field],str)):
                        instance_details[field] = instance[field]
                    elif(isinstance(instance[field],dict)):
                        # Attempt to flatten any JSON object for formatting
                        instance_details[field] = json.dumps(instance[field], indent=4, sort_keys=True, default=str).replace('\n','').replace(' ','').replace('"','')
        
            instances.append(instance_details)
    
    return sorted(instances,key=itemgetter(tag_key))
    
def output(instances,output):
    
    # CSV Output
    if output == 'csv':
        logging.info('Generating CSV Output')
        head = [ ]
        for key, value in reversed(instances[0].items()):
            head.append(key)
        print(','.join(head))
        for instance in instances:
            inst = [ ]
            for key, value in reversed(instance.items()):
                inst.append(value)
            print(','.join(inst))
    
    # JSON Output
    if output == 'json':
        logging.info('Generating JSON output')
        for instance in instances:
            print(instance)
            
    return 0
    
def parseArgs():

    parser = argparse.ArgumentParser(description='Describe AWS EC2 instances in a given account')   
    
    # AWS config. Set to optional, uses local default profile if not specified. Can specify region only with --region flag  
    parser.add_argument('AWS_KEY',  type=str, nargs='?', help='Specify an AWS key.', default=None)
    parser.add_argument('AWS_SECRET',  type=str, nargs='?',  help='Specify an AWS key secret', default=None) 
    parser.add_argument('AWS_REGION',  type=str, nargs='?', default='us-east-1', help='Specify an AWS region. Default is us-east-1')

    # Allow for specifying tag, default is owner.
    parser.add_argument('--tag',  type=str, default="Owner", help='Specify a tag. Default is Owner')
    
    # Allow for region specificity only, no input creds, use aws profile stored. Will override AWS_REGION if this is set
    parser.add_argument('--region',  type=str, nargs='?', help='Specify a region to override. Default is us-east-1')
    
    # Allow for either CSV or JSON output
    parser.add_argument('--output',  type=str, nargs='?', help='Specify an output format: CSV or JSON. Default is csv.', choices=['csv','json'], default='csv')

    # Allow for specifying additional fields from the EC2 DESCRIBE INSTANCES call e.g --fields 'State,ImageId'
    parser.add_argument('--fields', type=str, nargs='?', help='Specify additional fields to display about the EC2 instances. Input is comma-separated values in string', default=None)

    # Verbose output logging
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
    
    