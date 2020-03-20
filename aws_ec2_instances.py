#!/usr/bin/env python

import boto3, botocore.exceptions
import argparse
import logging

def main(args):
    
    return 0
    
def parse_args():
    
    parser = argparse.ArgumentParser(description='Describe AWS EC2 instances in a given account')
                     
    args = parser.parse_args()
    
    return args
    
if __name__ == "__main__":
    
    args = parse_args()

    main(args)
    
    