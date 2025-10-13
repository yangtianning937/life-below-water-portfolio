import {api_prefix} from "./api_perfix";

/**
 * @function fetch_place_details
 * @description Get coordinates for a specific place_id (Google Place Details via your backend).
 * @param place_id  Place ID from autocomplete.
 * @param language  Response language. Default: "en".
 * @returns Promise<any> — { name: string, lat: number|null, lng: number|null } on 200; null otherwise.
 */
export async function fetch_place_details(
  place_id: string,
  language: string = "en"
): Promise<any> {
  if (!place_id) return null;

  const url =
    `${api_prefix()}/places/details` +
    `?place_id=${encodeURIComponent(place_id)}` +
    `&language=${encodeURIComponent(language)}`;

  return await fetch(url, { mode: "cors" }).then(async (r) => {
    switch (r.status) {
      case 200:
        return await r.json().then((json) => json);
      default:
        return null;
    }
  });
}