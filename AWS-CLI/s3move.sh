#!/bin/bash

#aws s3api create-bucket --bucket waddupppbucket --region us-east-1
#aws s3 ls s3://cf-templates-1ejh6nnk3mgjq-us-east-1
#aws s3 cp AWS-CLI s3://waddupppbucket 
aws s3 cp AWS-CLI s3://waddupppbucket --recursive
