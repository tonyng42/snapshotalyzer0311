import boto3

if __name__ == '__main__': #this IF statement will ensure the code runs only it is used as a script
	session = boto3.Session(profile_name='shotty')
	ec2 = session.resource('ec2')

	for i in ec2.instances.all():
	    print (i)
