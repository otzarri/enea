import os
import yaml

from pprint import pprint

kube_file = '../deployments/nginx-waf/kube-file.yaml'

with open(kube_file, 'r') as file:
   kube = yaml.safe_load(file)


app_name = kube['metadata']['name']
volumes = kube['spec']['template']['spec']['volumes']
mounts = kube['spec']['template']['spec']['containers'][0]['volumeMounts']

response = []

for mount in mounts:
    # Get the volume related to the mount
    volume = next(volume for volume in volumes if volume["name"] == mount['name'])

    # Path of the volume into this project
    vol_path_local = os.path.join('../deployments', app_name, 'volumes', volume['name'])
    vol_path_oci = os.path.join('./deployments', app_name, 'volumes', volume['name'])

    if 'hostPath' in volume.keys():
        vol_type = 'bind'
        if 'type' in volume['hostPath'].keys() and volume['hostPath']['type'].lower() == "file":
            print('debug' + volume['hostPath']['path'])
            print('debug' + vol_path_oci)
            vol_file = volume['hostPath']['path'].split(vol_path_oci)[1].strip('/')
            vol_path_local = os.path.join(vol_path_local, vol_file)
            vol_path_oci = os.path.join(vol_path_oci, vol_file)
    elif 'persistentVolumeClaim' in volume.keys():
        vol_type = 'named'
        # vol_src = os.path.join('../deployments', app_name, volume['name'])
        # vol_dst = volume['persistentVolumeClaim']['claimName']
    else:
        raise Exception('Only "hostPath" and "persistentVolumeClaim" volume types are supported.')

    response.append({
        "name": mount['name'],
        "type": vol_type,
        "src": vol_path_local,
        "dst": vol_path_oci
    })

pprint(response)
