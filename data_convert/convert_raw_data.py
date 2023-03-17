import collections
import json
from typing import List, Dict

type_start = '<extra_id_0>'
type_end = '<extra_id_1>'
role_start = '<extra_id_2>'
role_end = '<extra_id_3>'


def convert_data(src_path, tgt_path, mark_tree=False, multi_tree=False):
    # Read json file.
    with open(src_path) as file:
        raw_data = [json.loads(line) for line in file]

    # Load text and event information.
    converted_data = []
    count = 0
    for line in raw_data:
        converted_line = {}
        text = line['text']
        if not line.get('event_list'):
            converted_data += [{'text': text, 'event': ""}]
            continue
        events_info = line['event_list']
        if len(events_info) > 0:
            count += 1
        else:
            print("Missing event type!")
            break
        events = list()
        for event_info in events_info:
            event_type = event_info['event_type']
            trigger = event_info['trigger']
            argument_str_list = list()
            for argument_info in event_info['arguments']:
                role = argument_info['role']
                argument = argument_info['argument']
                if mark_tree:
                    argument_str = ' '.join([role_start, role, argument, role_end])
                else:
                    argument_str = ' '.join([type_start, role, argument, type_end])
                argument_str_list += [argument_str]
            argument_str_list_str = ' '.join(argument_str_list)
            event = f"{type_start} {event_type} {trigger} {argument_str_list_str} {type_end}"
            events += [event]

        if not multi_tree:
            events = f'{type_start} ' + ' '.join(events) + f' {type_end}'
        converted_data += [{'text': text, 'event': events}]

    # Write converted data.
    with open(tgt_path, 'w') as file:
        for line in converted_data:
            file.write(json.dumps(line, ensure_ascii=False) + '\n')

    print(f"{count} records are converted.")


def convert_schema(src_path, tgt_path):
    # Read json file.
    with open(src_path) as file:
        raw_schema = [json.loads(line) for line in file]

    event_type_list = list()
    role_list = list()
    role_set = set()
    event_to_role = collections.defaultdict(list)
    for line in raw_schema:
        pass
        event_type = line['event_type']
        event_type_list += [event_type]
        for role_dict in line['role_list']:
            role = role_dict['role']
            event_to_role[event_type].append(role)
            if role in role_set:
                continue
            role_list += [role]
            role_set.add(role)

    converted_schema = [event_type_list, role_list, event_to_role]
    # Write converted data.
    with open(tgt_path, 'w') as file:
        for line in converted_schema:
            file.write(json.dumps(line, ensure_ascii=False) + '\n')


raw_train_data_path = "../data/raw_data/train.json"
output_train_data_path = "../data/text2tree/one_ie_ace2005_subtype/train.json"
raw_val_data_path = "../data/raw_data/dev.json"
output_val_data_path = "../data/text2tree/one_ie_ace2005_subtype/val.json"
raw_test_data_path = "../data/raw_data/test.json"
output_test_data_path = "../data/text2tree/one_ie_ace2005_subtype/test.json"
raw_schema_path = '../data/raw_data/schema.json'
output_schema_path = '../data/text2tree/one_ie_ace2005_subtype/event.schema'
# convert_data(raw_train_data_path, output_train_data_path)
# convert_data(raw_val_data_path, output_val_data_path)
convert_data(raw_test_data_path, output_test_data_path)
convert_schema(raw_schema_path, output_schema_path)
