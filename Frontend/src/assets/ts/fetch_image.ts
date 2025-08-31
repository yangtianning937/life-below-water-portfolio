import {api_prefix} from "./api_perfix";
import {arraybuffer_to_base64} from "./utils";

export async function fetch_image(name: string): Promise<any> {
    return await fetch(`${api_prefix()}/image/${name}`,
        {mode: 'cors'})
        .then(async r => {
            switch (r.status) {
                case 200:
                    let type = r.headers.get("Content-Type");
                    if (type != null && type.includes("image")) {
                        return await r.arrayBuffer().then(buffer => {
                            let base64 = arraybuffer_to_base64(buffer);
                            return `data:${type};base64,${base64}`;
                        })
                    } else {
                        return null;
                    }
                default:
                    return null;
            }
        })
}