#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            message=dict(type='str',required=True)
        )
    )

    msg = module.params['message']


    if not msg.strip():
       module.fail_json(msg=   "Empty message not allowed", changed=False)

    reversed_msg = msg[::-1]

    if msg == "fail me":
        module.fail_json(msg="You requested this to fail", changed=True,
                         original_message=msg,
                         reversed_message=reversed_msg)

    module.exit_json(changed=(msg != reversed_msg),
                     original_message=msg,
                     reversed_message=reversed_msg
        )
if __name__== '__main__':
    main()
