import {api_prefix} from "./api_perfix";

/**
 * @method fetch_fish_info
 * @param name The name of user as a String.
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_fish_info(name: string): Promise<any> {
    return await fetch(`${api_prefix()}/fish/info/${name}`,
        {mode: 'cors'})
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