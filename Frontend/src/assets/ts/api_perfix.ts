/**
 * @member api_prefix
 * @return Returns the prefix of the URL base on the environment (dev or product).
 */
export function api_prefix() {
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    let port: string | null = window.location.port;
    if (port === null || port === undefined || port === "")
        port = null;

    return `${protocol}//${hostname}${port != null ? `:${8000}` : ""}/iter2/api`;
}