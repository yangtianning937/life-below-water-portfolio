import {api_prefix} from "./api_perfix";

/**
 * @method fetch_activity
 * @param id (Optional) The id of the activity
 */
export async function fetch_activity(id?: number): Promise<any> {
    return await fetch(`${api_prefix()}/activity`,
        {mode: 'no-cors'})
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