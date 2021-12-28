import requests
import boto3
import sys

"""A lightweight application to ensure a constantly up to date DNS 
record that references the device's public IP, to facilitate 
connectivity from external devices.
"""

try:
    client = boto3.client('route53')
except:
    print('AWS Route53 client failed to load. Please ensure boto3 and ')
try:
    subdomain = sys.argv[1]
    dns_name = sys.argv[2]
except:
    print('At least one of the required arguments are missing')


def get_zone_id(dns_name):
    """Identify the R53 Hosted Zone that will be used for DDNS"""
    try:
        response = client.list_hosted_zones_by_name(DNSName=dns_name)
    except Exception as e:
        print(str(e))
    else:
        zone = response['HostedZones'][0]['Id'].removeprefix('/hostedzone/')
        return zone


zone = get_zone_id(dns_name)


def get_stored_ip(zone):
    """Get the existing IP stored by R53"""
    try:
        response = client.list_resource_record_sets(
            HostedZoneId=zone,
            StartRecordName='marmion.harryludlow.com',
            StartRecordType='A'
        )
    except Exception as e:
        print(str(e))
    else:
        try:
            stored_ip = response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
        except IndexError:
            print(
                f'No records exist for {subdomain}.{dns_name}. A record will be created.')
        else:
            return stored_ip


def get_current_ip():
    """Get the current public IP of the network the device runs on"""
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except Exception as e:
        print(str(e))
    else:
        return public_ip


stored_ip = get_stored_ip(zone)
current_ip = get_current_ip()

if stored_ip != current_ip:
    try:
        response = client.change_resource_record_sets(
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': f'{subdomain}.{dns_name}',
                            'ResourceRecords': [
                                {
                                    'Value': current_ip,
                                },
                            ],
                            'TTL': 600,
                            'Type': 'A',
                        },
                    },
                ],
                'Comment': 'IoT test',
            },
            HostedZoneId=zone,
        )
    except Exception as e:
        print(str(e))
    else:
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f'New IP: {current_ip}')
else:
    print(f'IP unchanged from: {stored_ip}')
