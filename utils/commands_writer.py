import os
import shutil


def write_converter_datapack(source_datapack_path, chains, x, y, z, offset_x, offset_y, chains_per_row, force, delete,
                             segment):
    datapack_path = os.path.join(os.path.dirname(source_datapack_path), "converter_datapack")

    print_chains(chains)

    if os.path.exists(datapack_path):
        if not force:
            print("\nERROR: Datapack named converter_datapack already exists! Aborting.")
            exit(0)
        else:
            shutil.rmtree(datapack_path)

    shutil.copytree(os.path.join("utils", "converter_datapack"), datapack_path)

    place_chains(datapack_path, chains, x, y, z, offset_x, offset_y, chains_per_row, segment)

    if delete:
        shutil.rmtree(source_datapack_path)

    print("\nDone! Open the world to finalise the conversion")
    print("If you missed the finalisation text in-game or need to see it again, you can run the following command:")
    print("- /data remove storage dp_conv:init \"init\"")


def print_chains(chains):
    if len(chains) == 0:
        print("No commands found! Make sure the datapack is valid.")
        exit(0)

    print("Placing command blocks with the following chains:")
    for chain in chains:
        print_chain(chains[chain])


def print_chain(chain):
    chain_text = "\n"
    if chain["repeating"]:
        chain_text += "- REPEATING "
    else:
        chain_text += "- IMPULSE "

    if chain["active"]:
        chain_text += "ALWAYS ACTIVE "
    else:
        chain_text += "NEEDS REDSTONE "

    chain_text += "CHAIN " + chain["id"]
    print(chain_text)

    for command in chain["commands"]:
        print(command)


def place_chains(datapack_path, chains, x, y, z, offset_x, offset_y, chains_per_row, segment):
    chain_positions = {}
    for c in chains:
        n_x = x + (int(len(chain_positions) % chains_per_row)) * offset_x
        n_y = y + (int(len(chain_positions) / chains_per_row)) * offset_y
        n_z = z

        if not is_valid_location(n_x, n_y, n_z):
            shutil.rmtree(datapack_path)
            print("\nERROR: Invalid location " + str(n_x) + " " + str(n_y) + " " + str(
                n_z) + ". Change x, y and z parameters and try again!")
            exit(0)

        chain_positions[c] = (n_x, n_y, n_z)

    init_content = []
    for c in chains:
        chain = chains[c]

        init_content.append("\n# {}".format(chain["id"]))

        chain_start_location = chain_positions[c]

        offset = 0

        if len(chain["commands"]) == 0:
            place_command(init_content, None, None, None, chain_start_location)
        elif not chain["repeating"]:
            command = "data merge block ~ ~ ~ {auto:0b}"
            place_command(init_content, command, "", chain["active"], chain_start_location)
            offset += 1

        for i in range(len(chain["commands"])):
            command = format_command(chain["commands"][i], chain_positions)
            chain_location = (chain_start_location[0], chain_start_location[1], chain_start_location[2] + i + offset)

            place_command(init_content, command,
                          "chain_" if offset + i != 0 else ("repeating_" if chain["repeating"] else ""),
                          True if offset + i != 0 else chain["active"],
                          chain_location)

            if segment and command != chain["commands"][i]:
                place_command(init_content, "data merge block ~ ~ ~1 {auto:1b}", "chain_", True, (
                    chain_start_location[0], chain_start_location[1], chain_start_location[2] + i + offset + 1))
                place_command(init_content, "data merge block ~ ~ ~ {auto:0b}", "", False, (
                    chain_start_location[0], chain_start_location[1], chain_start_location[2] + i + offset + 2))
                offset += 2

        place_sign(init_content, chain["id"], chain_start_location)

        init_content.append("forceload add {} {} {} {}".format(chain_start_location[0], chain_start_location[2],
                                                               chain_start_location[0],
                                                               chain_start_location[2] + len(chain["commands"]) + 1))

    init_function_path = os.path.join(datapack_path, "data", "converter_datapack", "functions", "init.mcfunction")
    init_function = open(init_function_path, 'a')
    init_function.write("\n".join(init_content))
    init_function.close()


def is_valid_location(x, y, z):
    if x < -29999999 or x > 29999999:
        return False
    if y < -64 or y > 319:
        return False
    if z < -29999999 or z > 29999999:
        return False

    return True


def format_command(command, chain_positions):
    if "function " in command:
        c = command.split("function ")[1]
        if c in chain_positions:
            command = command.replace("function {}".format(c),
                                      "data merge block {} {} {} {{auto:1b}}".format(chain_positions[c][0],
                                                                                     chain_positions[c][1],
                                                                                     chain_positions[c][2]))

    return command.replace('\\', '\\\\').replace('"', '\\"')


def place_command(init_content, command, prefix, active, position):
    if command is None:
        init_content.append(
            "setblock {} {} {} red_concrete".format(position[0],
                                                    position[1],
                                                    position[2]))
    else:
        init_content.append(
            "setblock {} {} {} {}command_block[facing=south]".format(position[0],
                                                                     position[1],
                                                                     position[2], prefix))

        init_content.append(
            "data merge block {} {} {} {{\"auto\":{},\"Command\":\"{}\"}}".format(
                position[0], position[1],
                position[2], "1b" if active else "0b", command))


def place_sign(init_content, function_id, command_position):
    init_content.append(
        "setblock {} {} {} oak_wall_sign[facing=north]".format(command_position[0], command_position[1],
                                                               command_position[2] - 1))
    init_content.append(
        "data merge block {} {} {} {{\"Text1\":'{{\"text\":\"- - -\"}}',\"Text2\":'{{\"text\":\"{}\"}}',\"Text3\":'{{\"text\":\"{}\"}}',\"Text4\":'{{\"text\":\"- - -\"}}'}}".format(
            command_position[0], command_position[1],
            command_position[2] - 1, function_id.split(":")[0], function_id.split(":")[1]))
