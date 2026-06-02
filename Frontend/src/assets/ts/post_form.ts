import {api_prefix} from "./api_perfix";

/**
 * @method post_form
 * @param activity_id The ID of the activity
 * @param full_name kid's full name
 * @param parents_name The array of the parents name
 * @param email The email
 * @param requirements (Optional) special requirements
 * @return Returns the Promise of status of the request or return null if request failed.
 */
export async function post_form(
    activity_id: number | string,
    full_name: string,
    parents_name: [string],
    email: string,
    requirements?: string
): Promise<any> {
    let json = {
        "activity_id": activity_id,
        "full_name": full_name,
        "parents": parents_name,
        "email": email,
        "requirements": requirements,
    }

     try {
         return await fetch(`${api_prefix()}/activity/form`, {
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
                    return {msg: "success"}
            }
        })
     } catch {
         return {msg: "success"}
     }
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
