import {api_prefix} from "./api_perfix";

/**
 * @method fetch_fish_avatar
 * @param species_en - English name of the fish species
 * @return Returns the Promise of Data containing cartoon_image or null if request failed
 */
export async function fetch_fish_avatar(species_en: string): Promise<any> {
    try {
        return await fetch(`${api_prefix()}/fish/avatar`, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ species_en })
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
    } catch {
        return null;
    }
}
