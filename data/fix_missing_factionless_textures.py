input_file = "descr_model_battle.txt"
output_file = "descr_model_battle_fixed.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

output = []
current_block = []

def process_block(block):
    texture_lines = []
    slave_texture = None
    already_has_default = False

    for line in block:
        stripped = line.strip()

        if stripped.startswith("texture"):
            texture_lines.append(line)

            # detect default (no faction)
            parts = stripped.split(",")
            if len(parts) == 1:
                already_has_default = True

            if "slave" in stripped.lower():
                slave_texture = line

    # skip if already has default or no textures
    if already_has_default or not texture_lines:
        return block

    # choose fallback
    if slave_texture:
        fallback_line = slave_texture
    else:
        fallback_line = texture_lines[0]

    # extract texture path
    parts = fallback_line.split(",")
    if len(parts) == 1:
        # already default-style
        return block
    else:
        texture_path = parts[1].strip()

    default_line = f"\ttexture\t\t\t{texture_path}\n"

    # find first faction texture index
    insert_index = None
    for i, line in enumerate(block):
        if line.strip().startswith("texture") and "," in line:
            insert_index = i
            break

    if insert_index is not None:
        block.insert(insert_index, default_line)

    return block


for line in lines:
    if line.strip().startswith("type"):
        if current_block:
            output.extend(process_block(current_block))
            current_block = []
    current_block.append(line)

# last block
if current_block:
    output.extend(process_block(current_block))

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(output)

print("Done. File saved as:", output_file)