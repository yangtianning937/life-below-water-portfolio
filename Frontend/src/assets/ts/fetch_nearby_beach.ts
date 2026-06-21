import {api_prefix} from "./api_perfix";
import {staticNearbyBeach} from "./staticFallback";

/**
 * @method fetch_nearby_beach
 * @param latitude The latitude of the position.
 * @param longitude The longitude of the position.
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_nearby_beach(latitude: string | number,
                                         longitude: string | number): Promise<any> {
    try {
        return await fetch(`${api_prefix()}/nearby/${latitude}/${longitude}`,
        {mode: 'cors'})
        .then(async r => {
            switch (r.status) {
                case 200:
                    return await r.json()
                        .then(json => json);
                default:
                    return staticNearbyBeach(latitude, longitude);
            }
        })
    } catch {
        return staticNearbyBeach(latitude, longitude);
    }
}
