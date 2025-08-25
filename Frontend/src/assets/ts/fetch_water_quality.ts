import {format_date} from "./utils";
import {api_prefix} from "./api_perfix";

/**
 * @method fetch_water_quality
 * @param site_id The site ID
 * @param date (optional) the date of the water quality
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_water_quality(site_id: number | string, date?: Date): Promise<any> {
    if (date) {
        let formatted_date = format_date(date, "yyyy-MM-dd");
        console.log(formatted_date);
        return await fetch(`${api_prefix()}/water_quality/${site_id}/date/${formatted_date}`,
            {mode: "no-cors"})
            .then(async r => {
                switch (r.status) {
                    case 200:
                        return await r.json()
                            .then(json => json);
                    default:
                        return null;
                }
            })
    } else {
        return await fetch(`${api_prefix()}/water_quality/${site_id}`,
            {mode: "no-cors"})
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
}
/*
[
    {
        "site_id": "369",
        "site_name_short": "Long Reef",
        "water_body": "Port Phillip  Bay",
        "date": "1990-04-11",
        "Type": "surface",
        "DO_mg": "9.0",
        "Sal": "35.0",
        "TSS": "5.4",
        "N_TOTAL": "460.0",
        "P_PO4": "160.0",
        "P_TOTAL": "260.0"
    }
]
 */