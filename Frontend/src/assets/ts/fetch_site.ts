import {api_prefix} from "./api_perfix";

/**
 * @method fetch_sites
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_sites(): Promise<any> {
    return await fetch(`${api_prefix()}/sites`,
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
[
    {
        "site_id": "1229",
        "site_name_long": "PORT PHILLIP BAY CENTRAL SEGMENT MSG #1229",
        "site_name_short": "Central",
        "water_body": "Port Phillip  Bay",
        "latitude": "-38.0570335388183",
        "longitude": "144.870407104492",
        "": ""
    },
]
 */