function _0x225b() {
    const _0x4fa837 = ['setFromMatrixColumn', 'addEventListener', '1553169yfTliU', 'pointerlockchange', 'pointerLockElement', 'YXZ', 'dispatchEvent', 'disconnect', 'requestPointerLock', 'lock', '142296oAQcND', 'webkitMovementY', 'THREE.PointerLockControls:\x20Unable\x20to\x20use\x20Pointer\x20Lock\x20API', 'mozMovementX', '32AFFpOl', 'position', 'ownerDocument', 'pointerlockerror', 'connect', '2319540LSJjOI', '30777kSZGdv', 'addScaledVector', 'unlock', 'setFromQuaternion', 'min', 'applyQuaternion', '918092EqEMqQ', '231955sydHAk', 'domElement', 'moveRight', 'exitPointerLock', 'THREE.PointerLockControls:\x20The\x20second\x20parameter\x20\x22domElement\x22\x20is\x20now\x20mandatory.', 'warn', 'minPolarAngle', 'movementX', 'mozMovementY', 'webkitMovementX', 'quaternion', 'dispose', 'matrix', 'getDirection', 'isLocked', '448857GifuPr', 'removeEventListener', 'setFromEuler', 'crossVectors', 'change', 'maxPolarAngle', '72YbVizE'];
    _0x225b = function() {
        return _0x4fa837;
    };
    return _0x225b();
}
const _0x1c1c21 = _0x162b;
(function(_0x55a02c, _0x222df6) {
    const _0xdb46e7 = _0x162b,
        _0x4a6e6a = _0x55a02c();
    while (!![]) {
        try {
            const _0x1bf7aa = parseInt(_0xdb46e7(0xf6)) / 0x1 * (-parseInt(_0xdb46e7(0xf0)) / 0x2) + parseInt(_0xdb46e7(0xe4)) / 0x3 + parseInt(_0xdb46e7(0xf5)) / 0x4 + parseInt(_0xdb46e7(0xfd)) / 0x5 + parseInt(_0xdb46e7(0xec)) / 0x6 + parseInt(_0xdb46e7(0xfc)) / 0x7 + parseInt(_0xdb46e7(0xe1)) / 0x8 * (-parseInt(_0xdb46e7(0xdb)) / 0x9);
            if (_0x1bf7aa === _0x222df6) break;
            else _0x4a6e6a['push'](_0x4a6e6a['shift']());
        } catch (_0x385008) {
            _0x4a6e6a['push'](_0x4a6e6a['shift']());
        }
    }
}(_0x225b, 0x574ce));
import {
    Euler,
    EventDispatcher,
    Vector3
} from '../../build/three.module.js';
const _euler = new Euler(0x0, 0x0, 0x0, _0x1c1c21(0xe7)),
    _vector = new Vector3(),
    _changeEvent = {
        'type': _0x1c1c21(0xdf)
    },
    _lockEvent = {
        'type': _0x1c1c21(0xeb)
    },
    _unlockEvent = {
        'type': 'unlock'
    },
    _PI_2 = Math['PI'] / 0x2;
class PointerLockControls extends EventDispatcher {
    constructor(_0x5caee2, _0x4a4fd5) {
        const _0x509e05 = _0x1c1c21;
        super();
        _0x4a4fd5 === undefined && (console[_0x509e05(0xd1)](_0x509e05(0xd0)), _0x4a4fd5 = document['body']);
        this[_0x509e05(0xfe)] = _0x4a4fd5, this[_0x509e05(0xda)] = ![], this[_0x509e05(0xd2)] = 0x0, this[_0x509e05(0xe0)] = Math['PI'];
        const _0x60fcf8 = this;

        function _0x4fd16d(_0xf9c52e) {
            const _0x31b740 = _0x509e05;
            if (_0x60fcf8['isLocked'] === ![]) return;
            const _0x18259a = _0xf9c52e[_0x31b740(0xd3)] || _0xf9c52e[_0x31b740(0xef)] || _0xf9c52e[_0x31b740(0xd5)] || 0x0,
                _0x3e1510 = _0xf9c52e['movementY'] || _0xf9c52e[_0x31b740(0xd4)] || _0xf9c52e[_0x31b740(0xed)] || 0x0;
            _euler[_0x31b740(0xf9)](_0x5caee2[_0x31b740(0xd6)]), _euler['y'] -= _0x18259a * 0.002, _euler['x'] -= _0x3e1510 * 0.002, _euler['x'] = Math['max'](_PI_2 - _0x60fcf8['maxPolarAngle'], Math[_0x31b740(0xfa)](_PI_2 - _0x60fcf8[_0x31b740(0xd2)], _euler['x'])), _0x5caee2[_0x31b740(0xd6)][_0x31b740(0xdd)](_euler), _0x60fcf8[_0x31b740(0xe8)](_changeEvent);
        }

        function _0xe2cd74() {
            const _0x142e0c = _0x509e05;
            _0x60fcf8['domElement'][_0x142e0c(0xf2)][_0x142e0c(0xe6)] === _0x60fcf8['domElement'] ? (_0x60fcf8[_0x142e0c(0xe8)](_lockEvent), _0x60fcf8[_0x142e0c(0xda)] = !![]) : (_0x60fcf8[_0x142e0c(0xe8)](_unlockEvent), _0x60fcf8[_0x142e0c(0xda)] = ![]);
        }

        function _0x3c23ec() {
            const _0x448bb0 = _0x509e05;
            console['error'](_0x448bb0(0xee));
        }
        this[_0x509e05(0xf4)] = function() {
            const _0x58729f = _0x509e05;
            _0x60fcf8['domElement'][_0x58729f(0xf2)][_0x58729f(0xe3)]('mousemove', _0x4fd16d), _0x60fcf8[_0x58729f(0xfe)][_0x58729f(0xf2)][_0x58729f(0xe3)]('pointerlockchange', _0xe2cd74), _0x60fcf8[_0x58729f(0xfe)][_0x58729f(0xf2)][_0x58729f(0xe3)](_0x58729f(0xf3), _0x3c23ec);
        }, this[_0x509e05(0xe9)] = function() {
            const _0x227178 = _0x509e05;
            _0x60fcf8[_0x227178(0xfe)][_0x227178(0xf2)][_0x227178(0xdc)]('mousemove', _0x4fd16d), _0x60fcf8[_0x227178(0xfe)][_0x227178(0xf2)][_0x227178(0xdc)](_0x227178(0xe5), _0xe2cd74), _0x60fcf8[_0x227178(0xfe)]['ownerDocument']['removeEventListener']('pointerlockerror', _0x3c23ec);
        }, this[_0x509e05(0xd7)] = function() {
            const _0x26ef52 = _0x509e05;
            this[_0x26ef52(0xe9)]();
        }, this['getObject'] = function() {
            return _0x5caee2;
        }, this[_0x509e05(0xd9)] = function() {
            const _0x32bd10 = new Vector3(0x0, 0x0, -0x1);
            return function(_0x458cd4) {
                const _0x2937ec = _0x162b;
                return _0x458cd4['copy'](_0x32bd10)[_0x2937ec(0xfb)](_0x5caee2[_0x2937ec(0xd6)]);
            };
        }(), this['moveForward'] = function(_0x3eab47) {
            const _0x45ecc1 = _0x509e05;
            _vector[_0x45ecc1(0xe2)](_0x5caee2[_0x45ecc1(0xd8)], 0x0), _vector[_0x45ecc1(0xde)](_0x5caee2['up'], _vector), _0x5caee2[_0x45ecc1(0xf1)][_0x45ecc1(0xf7)](_vector, _0x3eab47);
        }, this[_0x509e05(0xce)] = function(_0x29b456) {
            const _0x4058e8 = _0x509e05;
            _vector[_0x4058e8(0xe2)](_0x5caee2[_0x4058e8(0xd8)], 0x0), _0x5caee2[_0x4058e8(0xf1)][_0x4058e8(0xf7)](_vector, _0x29b456);
        }, this[_0x509e05(0xeb)] = function() {
            const _0x13c2a9 = _0x509e05;
            this[_0x13c2a9(0xfe)][_0x13c2a9(0xea)]();
        }, this[_0x509e05(0xf8)] = function() {
            const _0x4c424e = _0x509e05;
            _0x60fcf8[_0x4c424e(0xfe)][_0x4c424e(0xf2)][_0x4c424e(0xcf)]();
        }, this[_0x509e05(0xf4)]();
    }
}

function _0x162b(_0x592eff, _0xcfd21c) {
    const _0x225b94 = _0x225b();
    return _0x162b = function(_0x162b7c, _0x2f55c9) {
        _0x162b7c = _0x162b7c - 0xce;
        let _0x5a3bd7 = _0x225b94[_0x162b7c];
        return _0x5a3bd7;
    }, _0x162b(_0x592eff, _0xcfd21c);
}
export {
    PointerLockControls
};