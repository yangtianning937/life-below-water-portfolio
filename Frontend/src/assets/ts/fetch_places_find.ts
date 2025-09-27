import {api_prefix} from "./api_perfix";

/**
 * @function fetch_places_find
 * @description Convenience API: resolve the first autocomplete candidate and return its coordinates.
 *              Ideal for "press Enter to search" UX.
 * @param q        Query text (≥ 2 characters).
 * @param country  Country filter (ISO-2). Default: "AU".
 * @param language Response language. Default: "en".
 * @returns Promise<any> — { name: string, lat: number|null, lng: number|null } on 200; null otherwise.
 */
export async function fetch_places_find(
  q: string,
  country: string = "AU",
  language: string = "en"
): Promise<any> {
  if (!q || q.trim().length < 2) return null;
  const url = `${api_prefix()}/places/find` +
              `?q=${encodeURIComponent(q.trim())}` +
              `&country=${encodeURIComponent(country)}` +
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