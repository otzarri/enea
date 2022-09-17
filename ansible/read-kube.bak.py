import os
import yaml

from pprint import pprint

app_name = 'nginx-waf'
kube_file = '../deployments/nginx-waf/kube-file.yaml'

with open(kube_file, 'r') as file:
   kube = yaml.safe_load(file)

volumes = kube['spec']['template']['spec']['volumes']
mounts = kube['spec']['template']['spec']['containers'][0]['volumeMounts']

response = []

for mount in mounts:
    volume = next(volume for volume in volumes if volume["name"] == mount['name'])

    vol_src = ''
    vol_dir = os.path.join('../deployments', app_name, 'volumes', volume['name'])

    print(vol_dir)

    if 'hostPath' in volume.keys():
        vol_type = 'bind'
        vol_src = os.path.join('../deployments', app_name, volume['name'])
        vol_dst = volume['hostPath']['path']

        if 'type' in volume['hostPath'].keys() and volume['hostPath']['type'] == file:
            vol_file = volume['hostPath']['path'].split(vol_dst)[1].strip('/')
            vol_src = os.path.join(vol_src, vol_file)
            vol_dst = os.path.join(vol_dir, vol_file)

    elif 'persistentVolumeClaim' in volume.keys():
        vol_type = 'named'
        vol_src = os.path.join('../deployments', app_name, volume['name'])
        vol_dst = volume['persistentVolumeClaim']['claimName']
    else:
        raise Exception('Only volumes of type "hostPath" and "persistentVolumeClaim" are supported.')

    response.append({
        "name": mount['name'],
        "type": vol_type,
        "src": vol_src,
        "dst": vol_dst
    })

pprint(response)
