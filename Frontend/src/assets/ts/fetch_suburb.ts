import {api_prefix} from "./api_perfix";

/**
 * @method fetch_suburb
 * @param latitude The latitude of the position.
 * @param longitude The longitude of the position.
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_suburb(latitude: string | number,
                                         longitude: string | number): Promise<any> {
    return await fetch(`${api_prefix()}/reverse_geocode/${latitude}/${longitude}`,
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
/*
{"suburbName":"Manly","state":"New South Wales","postcode":"2095","confidence":0.95,"source":"google"}
 */