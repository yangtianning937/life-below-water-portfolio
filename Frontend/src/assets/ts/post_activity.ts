import {api_prefix} from "./api_perfix";

/**
 * @method post_activity
 * @param name The name of the activity
 * @param description The description of the activity
 * @param location The location of the activity
 * @param date The date of the activity
 * @param start The start time for the activity
 * @param end The end time for the activity
 * @param tags The tags for the activity
 * @return Returns the Promise of status of the request or return null if request failed.
 */
export async function post_activity(
    name: string,
    description: string,
    location: string,
    date: Date,
    start: Date,
    end: Date,
    tags: [string]
): Promise<any> {
    let json = {
        "name": name,
        "description": description,
        "location": location,
        "date": date,
        "start": start,
        "end": end,
        "tags": tags,
    }

    return await fetch(`${api_prefix()}/activity`, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(json),
        credentials: "include"
    })
        .then(async r => {
            switch (r.status) {
                case 200:
                    return await r.json()
                case 400:
                    return await r.json()
                default:
                    return null
            }
        })
}
/*
{
    "msg": "success"
}

Or

{
    "msg": Some Error Message
}
 */