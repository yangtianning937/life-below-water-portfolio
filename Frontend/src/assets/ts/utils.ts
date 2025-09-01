/**
 * @method format_date
 * @param date The Date
 * @param format The format string.
 * @return Returns the formatted date string.
 */
export function format_date(date: Date, format: string): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return format.replace('yyyy', String(year)).replace('MM', month).replace('dd', day).replace('hh', hours).replace('mm', minutes).replace('ss', seconds);
}

/**
 * @method arraybuffer_to_base64
 * @param buffer ArrayBuffer
 * @return The base64 string
 */
export const arraybuffer_to_base64 = (buffer: ArrayBuffer): string => {
    return btoa(new Uint8Array(buffer).reduce((data, byte) => data + String.fromCharCode(byte), ''));
}