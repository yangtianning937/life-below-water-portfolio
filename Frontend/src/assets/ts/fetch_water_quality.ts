import {format_date} from "./utils";
import {api_prefix} from "./api_perfix";

/**
 * @method fetch_water_quality
 * @param site_id The site ID
 * @param date (Optional) the date of the water quality
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_water_quality(site_id: number | string, date?: Date): Promise<any> {
    if (date) {
        let formatted_date = format_date(date, "yyyy-MM-dd");
        console.log(formatted_date);
        return await fetch(`${api_prefix()}/water_quality/${site_id}/date/${formatted_date}`,
            {mode: "cors"})
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
    "water_body": "Port Phillip  Bay",
    "record_id": 214,
    "type": "surface",
    "sal": 35,
    "n_total": 430,
    "p_total": 340,
    "site_id": "369",
    "site_name_short": "Long Reef",
    "date": "1991-03-08",
    "do_mg": 5.4,
    "tss": 5.8,
    "p_po4": 290
  }
]
 */