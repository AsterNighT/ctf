String['prototype']['encrypt'] = function (key) {
    const text_to_encrypt = new Array(2);
    const key_parts = new Array(4);
    let ret = '';
    let plaintext = escape(this); // literally the string content
    for (let i = 0; i < 4; i++) {
        key_parts[i] = Str4ToLong(key.slice(i * 4, (i + 1) * 4));
    }
    for (let i = 0; i < plaintext.length; i += 8) { // encrypt every 8 bytes
        text_to_encrypt[0] = Str4ToLong(plaintext.slice(i, i + 4));
        text_to_encrypt[1] = Str4ToLong(plaintext.slice(i + 4, i + 8));
        code(text_to_encrypt, key_parts);
        ret += LongToBase16(text_to_encrypt[0]) + LongToBase16(text_to_encrypt[1]);
    }
    return ret;
};

String['prototype']['decrypt'] = function (key) {
    const text_to_decrypt = new Array(2);
    const key_parts = new Array(4);
    let ret = '';
    let plaintext = escape(this); // literally the string content
    for (let i = 0; i < 4; i++) {
        key_parts[i] = Str4ToLong(key.slice(i * 4, (i + 1) * 4));
    }
    for (let i = 0; i < plaintext.length; i += 16) { // encrypt every 8 bytes
        text_to_decrypt[0] = Base16ToLong(plaintext.slice(i, i + 8));
        text_to_decrypt[1] = Base16ToLong(plaintext.slice(i + 8, i + 16));
        decode(text_to_decrypt, key_parts);
        ret += LongToStr4(text_to_decrypt[0]) + LongToStr4(text_to_decrypt[1]);
    }
    return ret;
};

function get_str_offset_1a6(index, _) {
    const str_set = get_str_closure();
    return get_str_offset_1a6 = function (index, _) {
        index = index - 0x1a6;
        let str = str_set[index]; //string 是基本类型，这个闭包无所谓
        return str;
    }, get_str_offset_1a6(index, _);
}

function code(text_to_encrypt, key_parts) {
    let text_part_0 = text_to_encrypt[0],
        text_part_1 = text_to_encrypt[1];
    const magic = 2654435769,
        magicx32 = 84941944608;
    let i = 0;
    while (i != magicx32) { // loop 32 times
        text_part_0 += (text_part_1 << 0x4 ^ text_part_1 >>> 0x5) + text_part_1 ^ i + key_parts[i & 0x3];
        i += magic;
        text_part_1 += (text_part_0 << 0x4 ^ text_part_0 >>> 0x5) + text_part_0 ^ i + key_parts[i >>> 0xb & 0x3];
    }
    text_to_encrypt[0] = text_part_0, text_to_encrypt[1] = text_part_1;
}

function decode(text_to_decrypt, key_parts) {
    let text_part_0 = text_to_decrypt[0],
        text_part_1 = text_to_decrypt[1];
    const magic = 2654435769,
        magicx32 = 84941944608;
    let i = magicx32;
    while (i != 0) { // loop 32 times
        text_part_1 -= (text_part_0 << 0x4 ^ text_part_0 >>> 0x5) + text_part_0 ^ i + key_parts[i >>> 0xb & 0x3];
        i -= magic;
        text_part_0 -= (text_part_1 << 0x4 ^ text_part_1 >>> 0x5) + text_part_1 ^ i + key_parts[i & 0x3];
    }
    text_to_decrypt[0] = text_part_0, text_to_decrypt[1] = text_part_1;
}

function Str4ToLong(str) { //'abcd' -> 0x64636261
    let ret = 0;
    for (let i = 0; i < 4; i++) ret |= str['charCodeAt'](i) << i * 8;
    return isNaN(ret) ? 0 : ret;
}

function LongToStr4(num) { // 0x64636261 -> 'abcd'
    const ret = String['fromCharCode'](num & 0xff, num >> 8 & 0xff, num >> 16 & 0xff, num >> 24 & 0xff);
    return ret;
}

function LongToBase16(num) { // 0x64636261 -> '64636261'
    let ret = '';
    for (let i = 3; i >= 0; i--) {
        let parti = (num >> 8 * i & 0xff)['toString'](16);
        if (parseInt('0x' + parti) <= 0xf) parti = '0' + parti;
        ret += parti;
    }
    return ret;
}

function Base16ToLong(str) { // '64636261' -> 0x64636261
    let ret = 0;
    for (let i = 0; i < 8; i += 2) {
        let parti = parseInt('0x' + str.slice(i, i + 2));
        ret = (ret << 8) + parti;
    }
    return ret;
}

function get_str_closure() {
    const str_set = ['slice', '1720848ZSQDkr', 'encrypt', '33MGcQht', '6fbde674819a59bfa12092565b4ca2a7a11dc670c678681daf4afb6704b82f0c', '14021KbbewD', 'charCodeAt', '808heYYJt', '5DlyrGX', '552oZzIQH', 'fromCharCode', '356IjESGA', '784713mdLTBv', '2529060PvKScd', '805548mjjthm', '844848vFCypf', '4bIkkcJ', '1356853149054377', 'length'];
    get_str_closure = function () {
        return str_set;
    };
    return get_str_closure();
}

function gyflagh(ans_string) {
    let cipher = ans_string['encrypt']('1356853149054377');
    if (cipher === '6fbde674819a59bfa12092565b4ca2a7a11dc670c678681daf4afb6704b82f0c') return true;
    return false;
}

console.log('aaaaaaaa'.encrypt('1356853149054377'))
console.log('6fbde674819a59bfa12092565b4ca2a7a11dc670c678681daf4afb6704b82f0c'.decrypt('1356853149054377'))