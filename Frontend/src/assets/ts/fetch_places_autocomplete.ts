import {api_prefix} from "./api_perfix";
import {staticPlacesAutocomplete} from "./staticFallback";

/**
 * @function fetch_places_autocomplete
 * @description Get place suggestions (Google Places Autocomplete via your backend).
 * @param q        Query text (must be at least 2 characters).
 * @param country  Country filter (ISO-2). Default: "AU".
 * @param limit    Max suggestions to return. Default: 8.
 * @param language Response language. Default: "en" (e.g., "zh-CN" also works).
 * @returns Promise<any> — { suggestions: [{ label: string, place_id: string }, ...] } on 200; null otherwise.
 */
export async function fetch_places_autocomplete(
  q: string,
  country: string = "AU",
  limit: number = 8,
  language: string = "en"
): Promise<any> {
  if (!q || q.trim().length < 2) return null;
  const url = `${api_prefix()}/places/autocomplete` +
              `?q=${encodeURIComponent(q.trim())}` +
              `&country=${encodeURIComponent(country)}` +
              `&limit=${limit}` +
              `&language=${encodeURIComponent(language)}`;

  try {
    return await fetch(url, { mode: "cors" }).then(async (r) => {
      switch (r.status) {
        case 200:
          return await r.json().then((json) => json);
        default:
          return staticPlacesAutocomplete(q, limit);
      }
    });
  } catch {
    return staticPlacesAutocomplete(q, limit);
  }
}
