import {api_prefix} from "./api_perfix";
import {staticActivity} from "./staticFallback";

/**
 * @method fetch_activity
 * @param id (Optional) The id of the activity
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_activity(id?: number | string): Promise<any> {
    try {
        if (id) {
            return await fetch(`${api_prefix()}/activity/${id}`,
            {mode: 'cors'})
            .then(async r => {
                switch (r.status) {
                    case 200:
                        return await r.json()
                            .then(json => json);
                    default:
                        return staticActivity(id);
                }
            })
        } else {
            return await fetch(`${api_prefix()}/activity`,
            {mode: 'cors'})
            .then(async r => {
                switch (r.status) {
                    case 200:
                        return await r.json()
                            .then(json => json);
                    default:
                        return staticActivity();
                }
            })
        }
    } catch {
        return staticActivity(id);
    }
}
/*
[
    {
        "date": "2025-09-19 14:00:00+00:00",
        "name": "Beach Clean-up",
        "id": "6e31457f67c54a3a81519e204b2aa211",
        "description": "Join the community to remove plastics and keep Port Phillip Bay clean.",
        "start": "2025-09-19 23:30:00+00:00",
        "end": "2025-09-20 01:30:00+00:00",
        "location": "Port Melbourne",
        "tags": "['community', 'plastics', 'kids']",
        "image": "beach.jpg"
    }
]
 */
