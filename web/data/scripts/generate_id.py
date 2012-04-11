#!/usr/bin/python

import json

def get_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f, 'utf-8')

    return data

def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, encoding='utf-8', indent=2)

def main():
    members = get_json('member-profile.json')

    for i, member in enumerate(members):
        member['id'] = '%06d' % i

    write_json('members_new.json', members)

if __name__ == '__main__':
    main()
