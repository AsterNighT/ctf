import sys

if len(sys.argv) != 3:
    exit(0)

with open(sys.argv[1], 'r') as f:
    with open(sys.argv[2], 'w') as output:
        lines = f.readlines()
        for line in lines:
            content = line.strip().split(' ')
            if content[0] == 'up':
                output.write('向上 '+content[1]+' 步\n')
            if content[0] == 'down':
                output.write('向下 '+content[1]+' 步\n')
            if content[0] == 'left':
                output.write('向左 '+content[1]+' 步\n')
            if content[0] == 'right':
                output.write('向右 '+content[1]+' 步\n')
            if content[0] == 'di':
                output.write('放下 '+content[1]+' 个物品\n')
            if content[0] == 'pi':
                output.write('拿起 '+content[1]+' 个物品\n')
            if content[0] == 'dp':
                output.write('放下盘子\n')
            if content[0] == 'pp':
                output.write('拿起盘子\n')
            if content[0] == 'ifu':
                output.write('如果手上的物品大于等于 ' +
                             content[1]+' 向上跳转 '+content[2]+' 行\n')
            if content[0] == 'ifd':
                output.write('如果手上的物品大于等于 ' +
                             content[1]+' 向下跳转 '+content[2]+' 行\n')
