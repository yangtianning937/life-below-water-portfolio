import {format_date} from "./utils";
import {api_prefix} from "./api_perfix";
import {staticWaterQuality} from "./staticFallback";

/**
 * @method fetch_water_quality
 * @param site_id The site ID
 * @param date (Optional) the date of the water quality
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_water_quality(site_id: number | string, date?: Date): Promise<any> {
    try {
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
                        return staticWaterQuality(site_id);
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
                        return staticWaterQuality(site_id);
                }
            })
        }
    } catch {
        return staticWaterQuality(site_id);
    }
}
/*
[
  {
    "date": "1984-07-19",
    "water_quality_score": 2,
    "quality_label": "darkred",
    "type": "surface",
    "do_mg_score": 1,
    "water_quality_simple": "bad",
    "do_mg": 7.9,
    "tss_score": 1,
    "sal": 40,
    "sal_score": 1,
    "site_id": "1991",
    "tss": 5.1,
    "n_total_score": 3,
    "record_id": 3,
    "n_total": 380,
    "p_po4_score": 3,
    "site_name_short": "Hobsons Bay",
    "p_po4": 62,
    "p_total_score": 3,
    "water_body": "Port Phillip  Bay",
    "p_total": 78,
    "quality_level": 3,
    "site": {
      "longitude": 144.933807373046,
      "cutoff_date": "2023-05-17",
      "avg_water_quality_score": 1.7,
      "p_total_avg_score": 3,
      "records_count": 8,
      "avg_quality_level": 2,
      "avg_water_quality_simple": "good",
      "do_mg_mean": 8,
      "avg_quality_label": "orange",
      "tss_mean": 5.6125,
      "do_mg_avg_score": 0,
      "sal_mean": 33.125,
      "tss_avg_score": 1,
      "site_id": "1991",
      "n_total_mean": 260,
      "sal_avg_score": 0,
      "site_name_short": "Hobsons Bay",
      "latest_date": "2024-05-16",
      "p_po4_mean": 54.625,
      "n_total_avg_score": 3,
      "latitude": -37.870189666748,
      "p_total_mean": 77.5,
      "p_po4_avg_score": 3
    }
  }
]
 */
