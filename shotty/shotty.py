import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
	'this lists all instances dummy'
	for i in ec2.instances.all():
	    print (', '.join((
	    	i.id,
	    	i.instance_type,
	    	i.placement['AvailabilityZone'],
	    	i.state['Name'],
	    	i.public_dns_name
	    	)))

if __name__ == '__main__': #this IF statement will ensure the code runs only it is used as a script
	
	list_instances()

#with the sys module: print(sys.argv)
