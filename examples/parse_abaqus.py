from abaqus_parser import inp

if __name__ == '__main__':
    # parse abaqus input from string
    content = inp.read_from_string(
        "*Node, nset=set-1\n"
        "1, 0, 0, 0\n"
        "2, 0, 0, 1\n"
        "3, 0, 1, 0\n"
        "4, 0, 1, 1\n"
        "5, 1, 0, 0\n"
        "6, 1, 0, 1\n"
        "7, 1, 1, 0\n"
        "8, 1, 1, 1\n"
        "9, 2, 0, 0\n"
        "10, 2, 0, 1\n"
        "11, 2, 1, 0\n"
        "12, 2, 1, 1\n"
        "13, 3, 0, 0\n"
        "14, 3, 0, 1\n"
        "15, 3, 1, 0\n"
        "16, 3, 1, 1\n"
        "*Element, type=C3D10\n"
        "1, 1, 2, 3, 4, 5, 6, 7, 8,\n"
        "9, 10\n"
        "2, 1, 2, 3, 4, 11, 12, 13, 14, \n"
        "15, 16\n"
    )

    # Rename node set
    node_block = content[0]
    node_block_parameters = node_block["parameters"]
    node_block_parameters["NSET"] = "ALL_NODES"

    # write updated input to string
    print(inp.write_to_string(content))


