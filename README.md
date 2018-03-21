# snapshotalyzer0311
lab to automate via Pythonsnapshot of EC2 instances in AWS

## About
This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots

## Configuring
shotty uses the config file created by the AWS cli. e.g.

`aws configure --profile shotty`

## Running

`pipenv run "python shotty/shotty.py <command> <subcommand> <--project=PROJECT>"`

*command* is isntances, volumes, or snapshots
*subcommand* - depends on the command used, it can be things like: list, start, or stop
*project* is optional

