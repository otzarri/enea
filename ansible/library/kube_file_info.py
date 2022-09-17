#!/usr/bin/python

import os
import yaml

from ansible.module_utils.basic import AnsibleModule

def main():
    # Module arguments
    module_args = dict(
        kube_file=dict(type='str', required=True)
    )

    # Seed the result dictionary
    result = dict(
        changed=False,
        volumes=list()
    )

    # Abstraction of this module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Business logic
    kube_file = module.params['kube_file']

    try:
        with open(kube_file, 'r') as file:
            kube = yaml.safe_load(file)
    except:
        raise Exception(f"Missing file: {kube_file}")

    app_name = kube['metadata']['name']
    volumes = kube['spec']['template']['spec']['volumes']
    mounts = kube['spec']['template']['spec']['containers'][0]['volumeMounts']


    response = []
    for mount in mounts:
        # The volume related to this mount
        volume = next(volume for volume in volumes if volume["name"] == mount['name'])

        # Calculate local (ansible_controller) and remote (oci_host) paths for the volumes
        vol_path_local = os.path.join('../deployments', app_name, 'volumes', volume['name'])
        vol_path_oci = os.path.join('./deployments', app_name, 'volumes', volume['name'])

        if 'hostPath' in volume.keys():
            vol_type = 'bind'
            vol_action = 'ignore'
            if 'type' in volume['hostPath'].keys() and volume['hostPath']['type'].lower() == "file":
                vol_file = volume['hostPath']['path'].split(vol_path_oci)[1].strip('/')
                vol_path_local = os.path.join(vol_path_local, vol_file)
                vol_path_oci = os.path.join(vol_path_oci, vol_file)
        elif 'persistentVolumeClaim' in volume.keys():
            vol_type = 'named'
            if os.path.exists(vol_path_local):
                if len(os.listdir(vol_path_local)) > 0:
                    vol_action = 'create_and_copy'
                else:
                    vol_action = 'create_empty'
            else:
                vol_action = 'ignore'
        else:
            raise Exception('Only "hostPath" and "persistentVolumeClaim" volume types are supported.')

        response.append({
            "name": mount['name'],
            "type": vol_type,
            "src": vol_path_local,
            "dst": vol_path_oci,
            "action": vol_action
        })

    result['volumes'] = response

    # Exit the module
    module.exit_json(**result)

if __name__ == "__main__":
    main()
