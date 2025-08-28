import json
import os
import re

def main():
    """Parses the status files transferred from the node into jsons."""
    # Starter variables
    files_dir = os.listdir('files')
    procs = []
    name_re = re.compile('^Name:\t(.*)$')
    state_re = re.compile('^State:.*\((.*)\)$')
    thread_re = re.compile('^Threads:\t(.*)$')
    final = {}

    # Go into the file directory and go through each node
    for node in files_dir:
        if node == '.gitkeep':
            continue
        procs = os.listdir('files/%s' % node)
        node_dict = {}

        # Goes through each pid that was transferred over
        for proc in procs:
            name_found = False
            state_found = False
            thread_found = False
            state = ''
            filename = 'files/%s/%s' % (node, proc)
            stat_file = open(filename, 'r')
            proc_data = {}

            # Parse through the status file for the keys we want
            for _, line in enumerate(stat_file):
                if not name_found:
                    search = name_re.search(line)
                    if search:
                        name_found = True
                        proc_data['name'] = search.group(1)
                if not state_found:
                    search = state_re.search(line)
                    if search:
                        state_found = True
                        state = search.group(1)
                if not thread_found:
                    search = thread_re.search(line)
                    if search:
                        thread_found = True
                        proc_data['threads'] = int(search.group(1))

                if name_found and state_found and thread_found:
                    proc_data['pid'] = proc
                    if state not in node_dict:
                        node_dict[state] = {}

                    node_dict[state][proc] = proc_data
                    continue

        # Add the node to the whole dictionary
        final[node] = node_dict

    # We have completed the loop; now just to save our json
    with open('process_dump.json', 'w') as final_file:
        final_json = json.dumps(final, indent=4)
        final_file.write(final_json)

if __name__ == '__main__':
    main()

