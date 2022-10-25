from typing_extensions import final


char_list = [
    '国', '气', '传', '必', '强', '种', '火', '样', '很', '水',
    '办', '眼', -27761, '了', '为', '机', '围', '够', '今', -29774,
    '公', '以', '每', '习', '叔', '提', -29701, '关', '破', '吗',
    '嘴', '爱', '位', '动', -28207, '再', '何', '候', '岁', -27082,
    '军', '报', '义', '夜', '早', '应', '法', -29783, '习', -29754,
    -29302, '劳', '开', '哇', '村', '特', -29321, -26490, '建', '忽',
    '库', '何', '工', -28589, '息', '展', '收', '找', -30270, -28589,
    '相', '带', '每', '好', '劳', '把', '实', '穿', '带', '呀',
    '列', '冲', '作', '体', '样', '直', '卡', '是', '最', '倒',
    -29731, '师', '底', '头', -28826, '紧', -28589, '区', -26004, '块']

final_list = []

for ch in char_list:
    if isinstance(ch , int) and ch < 0:
        final_list += chr(ch+65536)
    else:
        final_list += ch

print(final_list)

target = "鎏金哇卡呀库列"

ans = ""

for c in target:
    for i in range(len(final_list)):
        if final_list[i] == c:
            ans += "%02d" %i
            break

print(ans)
