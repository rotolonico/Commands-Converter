import os
import shutil


def write_converter_datapack(source_datapack_path, chains, x, y, z, offset_x, offset_y, chains_per_row, force, delete):
    datapack_path = os.path.join(os.path.dirname(source_datapack_path), "converter_datapack")

    print_chains(chains)

    if os.path.exists(datapack_path):
        if not force:
            print("\nERROR: Datapack named converter_datapack already exists! Aborting.")
            exit(0)
        else:
            shutil.rmtree(datapack_path)

    shutil.copytree(os.path.join("utils", "converter_datapack"), datapack_path)

    place_chains(datapack_path, chains, x, y, z, offset_x, offset_y, chains_per_row)

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


def place_chains(datapack_path, chains, x, y, z, offset_x, offset_y, chains_per_row):
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
        if len(chain["commands"]) == 0:
            init_content.append(
                "setblock {} {} {} red_concrete".format(chain_start_location[0],
                                                        chain_start_location[1],
                                                        chain_start_location[2]))
        else:
            init_content.append(
                "setblock {} {} {} {}command_block[facing=south]".format(chain_start_location[0],
                                                                         chain_start_location[1],
                                                                         chain_start_location[2],
                                                                         "repeating_" if chain["repeating"] else ""))

            init_content.append(
                "data merge block {} {} {} {{\"auto\":{},\"Command\":\"{}\"}}".format(
                    chain_start_location[0], chain_start_location[1],
                    chain_start_location[2], "1b" if chain["active"] else "0b",
                    format_command(chain["commands"][0], chain_positions)))

        for i in range(1, len(chain["commands"]), 1):
            command = format_command(chain["commands"][i], chain_positions)
            init_content.append(
                "setblock {} {} {} chain_command_block[facing=south]".format(chain_start_location[0],
                                                                             chain_start_location[1],
                                                                             chain_start_location[2] + i))
            init_content.append(
                "data merge block {} {} {} {{\"auto\":1b,\"Command\":\"{}\"}}".format(
                    chain_start_location[0], chain_start_location[1],
                    chain_start_location[2] + i, command))

        if len(chain["commands"]) != 0 and not chain["repeating"]:
            init_content.append(
                "setblock {} {} {} chain_command_block[facing=south]".format(chain_start_location[0],
                                                                             chain_start_location[1],
                                                                             chain_start_location[2] + len(
                                                                                 chain["commands"])))

            init_content.append(
                "data merge block {} {} {} {{\"auto\":1b,\"Command\":\"data merge block {} {} {} {{auto:0b}}\"}}".format(
                    chain_start_location[0], chain_start_location[1],
                    chain_start_location[2] + len(chain["commands"]), chain_start_location[0], chain_start_location[1],
                    chain_start_location[2]))

        init_content.append(
            "setblock {} {} {} oak_wall_sign[facing=north]".format(chain_start_location[0], chain_start_location[1],
                                                                   chain_start_location[2] - 1))
        init_content.append(
            "data merge block {} {} {} {{\"Text1\":'{{\"text\":\"- - -\"}}',\"Text2\":'{{\"text\":\"{}\"}}',\"Text3\":'{{\"text\":\"{}\"}}',\"Text4\":'{{\"text\":\"- - -\"}}'}}".format(
                chain_start_location[0], chain_start_location[1],
                chain_start_location[2] - 1, chain["id"].split(":")[0], chain["id"].split(":")[1]))

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
