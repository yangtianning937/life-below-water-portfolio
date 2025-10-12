import {api_prefix} from "./api_perfix";

/**
 * @method fetch_fish_avatar
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_fish_avatar(image_url: string): Promise<any> {
    return await fetch(`${api_prefix()}/fish/avatar`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_url })
    })
        .then(async r => {
            switch (r.status) {
                case 200:
                    return await r.json()
                        .then(json => json);
                default:
                    return null;
            }
        })
}