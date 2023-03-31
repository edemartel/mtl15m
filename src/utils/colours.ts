export type colour = [number, number, number];

export function lerp(a: number, b: number, ratio: number) {
    return (1 - ratio) * a + ratio * b;
}

export function hexify(x: number) {
    const val = Math.min(Math.floor(x * 255), 255);
    return val.toString(16).padStart(2, '0');
}

export function toHex(colour: colour): string {
    function hexify(x: number) {
        const val = Math.min(Math.floor(x * 255), 255);
        return val.toString(16).padStart(2, '0');
    }
    return '#' + colour.map(hexify).join('');
}

export function hsvToRgb(h: number, s: number, v: number): colour {
    let r, g, b;

    const i = Math.floor(h * 6);
    const f = h * 6 - i;
    const p = v * (1 - s);
    const q = v * (1 - f * s);
    const t = v * (1 - (1 - f) * s);

    switch (i % 6) {
    case 0:
        r = v, g = t, b = p; 
        break;
    case 1: 
        r = q, g = v, b = p; 
        break;
    case 2: 
        r = p, g = v, b = t; 
        break;
    case 3: 
        r = p, g = q, b = v; 
        break;
    case 4: 
        r = t, g = p, b = v; 
        break;
    case 5: 
        r = v, g = p, b = q; 
        break;
    default:
        return [0, 0, 0];
    }

    return [r, g, b];
}