import boto3
import click
import botocore
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

@click.group() #This is the main group. Volumes and Instances are commands nested inside of it
def cli():
	"""Shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
	"""Commands for SnapshotS"""
@snapshots.command('list') #copied from instances.command('list')
@click.option("--project", default=None, 
	help="Only snapshots for instances in project (tag Project:<name>)")
def list_snapshots(project):
	'this command will lists all the Snapshots idiot'
	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshots.all():
				print(", ".join((
					s.id,
					v.id,
					i.id,
					s.state,
					s.progress,
					s.start_time.strftime('%c')
				)))
	return

@cli.group('volumes')
def volumes():
	"""Commands for volumes"""

@volumes.command('list') #copied from instances.command('list')
@click.option("--project", default=None, 
	help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
	'this command will lists all the volumes dumbass'
	instances = filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			print(", ".join((
				v.id,
				i.id,
				v.state,
				str(v.size) + "GiB",
				v.encrypted and "Encrypted" or "Unencrypted"
			)))
	return

@cli.group('instances')
def instances():
	""" Commands for instances"""

@instances.command('snapshot', 
	help='Create snapshots of all volumes')
@click.option("--project", default=None, 
	help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
	'This function creates snapshots for EC2 instances'

	instances = filter_instances(project)
	for i in instances:
		print('Stopping {0}'.format(i.id))
		
		i.stop() #this will stop the instance before creating the snapshot
		i.wait_until_stopped()
		
		for v in i.volumes.all():
			print(" Creating snapshot of {0}".format(v.id))
			v.create_snapshot(Description='Created by SnapshotAlyzer 30000') #create_snapshot is a fcommand within Boto3
		print('Starting {0}'.format(i.id))
		
		i.start()
		i.wait_until_running()
	
	print('Job\'s Done!') #this is only printed after everything is done
	return


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
		try:
			i.stop() #this will stop the instance before creating the snapshot. IF it can stop the instance, the code will keep going (i.e will not hit an Exceptions). If there's a botocore.exceptions.ClientError error, it will print the line below.
		except botocore.exceptions.ClientError as e: # the 'as' just gives a valuable name to the Exception
			print ('Could not stop {0}. '.format(i.id) + str(e)) #this block of action will occur if the defined exception is raised, and print the valuable 'e'
			continue #this continue command isn't really needed


	return

@instances.command('start')
@click.option('--project', default=None, help = 'Starting only instances with the same project tag')

def start_instances(project):
	'This will start the instances with the same project tag'

	instances = filter_instances(project)

	for i in instances:
		print('Starting {0}...'.format(i.id))
		try:
			i.start()
		except botocore.exceptions.ClientError as e: # the 'as' just gives a valuable name to the Exception
			print ('Could not start {0}. '.format(i.id) + str(e)) #this block of action will occur if the defined exception is raised, and print the valuable 'e'
			continue #this continue command isn't really needed

	
	return






if __name__ == '__main__': #this IF statement will ensure the code runs only it is used as a script
	cli() #changed from list_instances(), then from instances()

#with the sys module: print(sys.argv)
#this will print out just the value ass. to the Key of 'AvailabilityZone'
#this is something I am trying...