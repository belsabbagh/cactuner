from src.cac import CAC


def brute_force(image_array, block_sizes, debug=False):
    max_CR = {'CR': -1, 'block_width': 0, 'block_height': 0}
    i = 10
    for block_width, block_height in block_sizes:
        CR = CAC(image_array, block_width, block_height, debug=debug)
        if CR > max_CR['CR']:
            max_CR['CR'] = CR
            max_CR['block_width'] = block_width
            max_CR['block_height'] = block_height
    return max_CR

