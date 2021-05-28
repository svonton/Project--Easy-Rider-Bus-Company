import json
import re
test_string = input()
user_input = json.loads(test_string)
#stage 2 code bellow
def type_validation():
    possible_datatype = {'bus_id': "<class 'int'>", 'stop_id': "<class 'int'>", 'stop_name': "<class 'str'>",
                         'next_stop': "<class 'int'>", 'stop_type': "<class 'str'>", 'a_time': "<class 'str'>"}
    error_dict = {x: 0 for x in user_input[0]}
    target_to_check = ['stop_name', 'stop_type', 'a_time']
    template_dict = {'stop_name': r'([A-Z][a-z]+ ?)+ ?(Avenue|Street|Road|Boulevard)$', 'stop_type': r'[FOS]$',
                     'a_time': r'[01]\d:[0-5]\d$'}
    for i in range(len(user_input)):
        for cntx in user_input[i]:
            if str(type(user_input[i][cntx])) != possible_datatype[cntx] or user_input[i][cntx] == "":
                if cntx == 'stop_type' and user_input[i][cntx] == "":
                    continue
                error_dict[cntx] += 1
            if cntx in target_to_check and str(type(user_input[i][cntx])) == possible_datatype[cntx]:
                if not re.match(template_dict[cntx], user_input[i][cntx]):
                    error_dict[cntx] += 1
    print(f'Type and required field validation: {sum(error_dict.values())} errors')
    for j in error_dict:
        if j in target_to_check:
            pass
            print(j + ': ' + str(error_dict[j]))
# stage 3 code below
def bus_line_info():
    count = {128: 0, 256: 0, 512: 0, 1024: 0}
    for i in range(len(user_input)):
        if user_input[i]['bus_id'] in count.keys():
            count[user_input[i]['bus_id']] += 1
    print('Line names and number of stops:\n')
    for ans in count.keys():
        print(f'bus_id: {ans}, stops: {count[ans]}')
# stage 4 code bellow
def st():
    stop_container = {128: {'S': set(), 'T': set(), 'F': set()}, 256: {'S': set(), 'T': set(), 'F': set()},
                      512: {'S': set(), 'T': set(), 'F': set()}, 1024: {'S': set(), 'T': set(), 'F': set()}}

    def serarcher(target):
        bus_id_set = set()
        for i in range(len(user_input)):
            if user_input[i]['bus_id'] not in bus_id_set:
                bus_id_set.update([user_input[i]['bus_id']])
            if user_input[i]['bus_id'] == target:
                if user_input[i]['stop_type'] in stop_container[target].keys():
                    stop_container[target][user_input[i]['stop_type']].update([user_input[i]['stop_name']])

        if target in bus_id_set and (len(stop_container[target]['S']) == 0 or len(stop_container[target]['F']) == 0):
            return False
        return True

    stop_count_dict = {'S': set(), 'T': set(), 'F': set()}
    show = True

    for i in stop_container.keys():
        if not serarcher(i):
            print(f"There is no start or end stop for the line: {i}.")
            show = False
            break
        for cntx in stop_count_dict.keys():
            stop_count_dict[cntx].update(stop_container[i][cntx])

    other_bus_line = {128, 256, 512, 1024}

    line_holder = {128: set(), 256: set(), 512: set(), 1024: set()}

    for i in range(len(user_input)):
        line_holder[user_input[i]['bus_id']].update([user_input[i]['stop_name']])

    for i in stop_container.keys():
        for j in other_bus_line.difference([i]):
            bus_stop_intersection = set.intersection(line_holder[i], line_holder[j])
            stop_container[i]['T'].update(bus_stop_intersection)
            stop_count_dict['T'].update(bus_stop_intersection)

    if show:
        print(f"""Start stops: {len(stop_count_dict['S'])} {sorted(list(stop_count_dict['S']))}
    Transfer stops: {len(stop_count_dict['T'])} {sorted(list(stop_count_dict['T']))}
    Finish stops: {len(stop_count_dict['F'])} {sorted(list(stop_count_dict['F']))}""")
# stage 5 code below
def time_cheker():
    stop_conteiner = {128: {'stop_name': list(), 'a_time': list()}, 256: {'stop_name': list(), 'a_time': list()},
    512: {'stop_name': list(), 'a_time': list()}, 1024: {'stop_name': list(), 'a_time': list()}}
    #sort json
    for cntx in user_input:
        for line_data_type in ['stop_name','a_time']:
            stop_conteiner[cntx['bus_id']][line_data_type].append(cntx[line_data_type])
    #check is time data correct
    #{128: {'stop_name': [], 'a_time': []}, 256: {'stop_name': [], 'a_time': []}, 512: {'stop_name': ['Bourbon Street', 'Sunset Boulevard'], 'a_time': ['08:13', '08:16']}, 1024: {'stop_name': [], 'a_time': []}}
    def time_check():
        line_error_container = {128: None, 256: None, 512: None, 1024: None}
        for bus, bus_info in stop_conteiner.items():
            previous_stop_time = ''
            if len(bus_info['a_time']) > 0:
                if sorted(bus_info['a_time']) != bus_info['a_time']:
                    for name, time in zip(bus_info['stop_name'],bus_info['a_time']):
                        if previous_stop_time == '':
                            previous_stop_time = time
                        else:
                            if previous_stop_time > time:
                                if not line_error_container[bus]:
                                    line_error_container[bus] = name
                            else:
                                previous_stop_time = time
        return line_error_container

    error_info = time_check()

    print('Arrival time test:')
    if any(error_info.values()):
        for cntx in error_info.keys():
            if error_info[cntx] != None:
                print(f'bus_id line {cntx}: wrong time on station {error_info[cntx]}')

    else:
        print('OK')
# stage 6 code below
def on_demand():
    other_bus_line = {128, 256, 512, 1024}
    transfer_stop_container = {128: set(), 256: set(), 512: set(), 1024: set()}
    line_holder = {128: set(), 256: set(), 512: set(), 1024: set()}

    for i in range(len(user_input)):
        line_holder[user_input[i]['bus_id']].update([user_input[i]['stop_name']])

    for i in transfer_stop_container.keys():
        for j in other_bus_line.difference([i]):
            bus_stop_intersection = set.intersection(line_holder[i], line_holder[j])
            transfer_stop_container[i].update(bus_stop_intersection)

    stop_on_demand = {128: set(), 256: set(), 512: set(), 1024: set()}
    for cntx in user_input:
        if cntx['stop_type'] == 'O':
            stop_on_demand[cntx['bus_id']].update([cntx['stop_name']])

    gotcha = []
    print('On demand stops test:')
    for i in transfer_stop_container:
        for j in stop_on_demand[i]:
            if j in transfer_stop_container[i]:
                gotcha.append([j])
    print(f"Wrong stop type: {gotcha}" if len(gotcha) > 0 else 'OK')

on_demand()