import os
import json
import glob


def get_chains_from_datapack(datapack_path):
    data_path = os.path.join(datapack_path, "data")
    always_active_impulse_chains, always_active_repeating_chains = get_always_active_chains(data_path)
    return get_functions_in_datapack(data_path, always_active_impulse_chains, always_active_repeating_chains)


def get_always_active_chains(data_path):
    tags_path = os.path.join(data_path, "minecraft", "tags", "functions")

    always_active_impulse_chains = []
    always_active_repeating_chains = []

    load_file_path = os.path.join(tags_path, "load.json")
    if os.path.exists(load_file_path):
        load_file = open(load_file_path)
        always_active_impulse_chains = json.loads(load_file.read())["values"]

    tick_file_path = os.path.join(tags_path, "tick.json")
    if os.path.exists(tick_file_path):
        tick_file = open(tick_file_path)
        always_active_repeating_chains = json.loads(tick_file.read())["values"]

    return always_active_impulse_chains, always_active_repeating_chains


def get_functions_in_datapack(data_path, always_active_impulse_chains, always_active_repeating_chains):
    functions = {}

    for namespace_path in [f.path for f in os.scandir(data_path) if f.is_dir()]:
        functions = merge_two_dicts(functions, get_functions_in_namespace(namespace_path, always_active_impulse_chains,
                                                                          always_active_repeating_chains))

    return functions


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def get_functions_in_namespace(namespace_path, always_active_impulse_chains, always_active_repeating_chains):
    functions = {}
    functions_path = os.path.join(namespace_path, "functions")
    namespace_name = os.path.basename(namespace_path)

    if os.path.exists(functions_path):
        for function_path in glob.iglob(os.path.join(functions_path, "**", "*.mcfunction"), recursive=True):
            function_id = namespace_name + ":" + function_path.replace(functions_path, "").replace(".mcfunction", "").strip(
                "\\").strip("//")

            commands_raw = open(function_path, "r").readlines()
            commands = []
            for c in commands_raw:
                c = c.strip("\n").strip(" ")
                if len(c) == 0 or c[0] == "#":
                    continue
                commands.append(c)

            functions[function_id] = {
                "id": function_id,
                "repeating": function_id in always_active_repeating_chains,
                "active": function_id in always_active_impulse_chains or function_id in always_active_repeating_chains,
                "commands": commands
            }

    return functions
