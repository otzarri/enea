#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def main():
    # Module arguments
    module_args = dict(
        path=dict(type='str', required=True)
    )

    # Seed the result dictionary
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # Abstraction of this module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Exit the module
    module.exit_json(changed=False, meta=result)

if __name__ == "__main__":
    main()
