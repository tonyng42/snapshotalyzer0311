import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
	instances = []

	if project:
		filters = [{'Name':'tag:Project','Values':['Valkyrie']}]
		instances = ec2.instances.filter(Filters=filters)
	else:
		instances = ec2.instances.all()
	
	return instances

@click.group()
def instances():
	""" Commands for instances"""


@instances.command('list') #changed @click to @instances + the name 'list'
@click.option("--project", default=None, 
	help="Only instances for project (tag Project:<name>)")

def list_instances(project):
	'this lists all instances dummy'
	instances = filter_instances(project)

	for i in instances:
		tags = {t['Key']: t['Value'] for t in i.tags or [] }
		print (', '.join((
			i.id,
			i.instance_type,
			i.placement['AvailabilityZone'], 
			i.state['Name'],
			i.public_dns_name,
			tags.get('Project', '<no project>'))))

	return

@instances.command('stop')
@click.option('--project', default=None, help = 'Only instances for project')

def stop_instances(project):
	'this will stop the instances with the same project tag'
	#this entries below are the same as the list_instances function, and will find all the instances with the same project tag

	instances = filter_instances(project)

	for i in instances:
		print('Stopping {0}...'.format(i.id))
		i.stop()

	return

@instances.command('start')
@click.option('--project', default=None, help = 'Starting only instances with the same project tag')

def start_instances(project):
	'This will start the instances with the same project tag'

	instances = filter_instances(project)

	for i in instances:
		print('Starting {0}...'.format(i.id))
		i.start()

	return






if __name__ == '__main__': #this IF statement will ensure the code runs only it is used as a script
	
	instances() #changed from list_instances()

#with the sys module: print(sys.argv)
#this will print out just the value ass. to the Key of 'AvailabilityZone'
#this is something I am trying...