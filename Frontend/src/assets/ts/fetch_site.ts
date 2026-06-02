import {api_prefix} from "./api_perfix";
import {staticSites} from "./staticFallback";

/**
 * @method fetch_sites
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_sites(): Promise<any> {
    try {
        return await fetch(`${api_prefix()}/sites`,
        {mode: 'cors'})
        .then(async r => {
            switch (r.status) {
                case 200:
                    return await r.json()
                        .then(json => json);
                default:
                    return staticSites;
            }
        })
    } catch {
        return staticSites;
    }
}
/*
[
  {
    "longitude": 144.870407104492,
    "cutoff_date": "2023-05-17",
    "avg_water_quality_score": 1.5,
    "p_total_avg_score": 3,
    "records_count": 8,
    "avg_quality_level": 2,
    "avg_water_quality_simple": "good",
    "do_mg_mean": 8.1375,
    "avg_quality_label": "orange",
    "tss_mean": 1.925,
    "do_mg_avg_score": 0,
    "sal_mean": 34.375,
    "tss_avg_score": 0,
    "site_id": "1229",
    "n_total_mean": 218.75,
    "sal_avg_score": 0,
    "site_name_short": "Central",
    "latest_date": "2024-05-16",
    "p_po4_mean": 47.125,
    "n_total_avg_score": 3,
    "latitude": -38.0570335388183,
    "p_total_mean": 63.75,
    "p_po4_avg_score": 3
  }
]
 */
