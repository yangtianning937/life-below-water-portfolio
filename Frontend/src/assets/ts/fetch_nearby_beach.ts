import {api_prefix} from "./api_perfix";
import {staticNearbyBeach} from "./staticFallback";

/**
 * @method fetch_nearby_beach
 * @param latitude The latitude of the position.
 * @param longitude The longitude of the position.
 * @return Returns the Promise of Data as shown below or return null if request failed.
 */
export async function fetch_nearby_beach(latitude: string | number,
                                         longitude: string | number): Promise<any> {
    try {
        return await fetch(`${api_prefix()}/nearby/${latitude}/${longitude}`,
        {mode: 'cors'})
        .then(async r => {
            switch (r.status) {
                case 200:
                    return await r.json()
                        .then(json => json);
                default:
                    return staticNearbyBeach(latitude, longitude);
            }
        })
    } catch {
        return staticNearbyBeach(latitude, longitude);
    }
}
/*
[
  {
    "name": "Manly Beach",
    "location": {
      "lat": -33.79645980000001,
      "lon": 151.2883992
    },
    "photos": [
      "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference=AciIO2c22pTwKoRBmAk-3V8q_5l7RhFMq4j8XbVtki1JoRRMB6WO0diKvRLairozYXzVs-swtVOoCCy3sSFQViCU__cuVnrLmpK_Yvd2Hhnco9eWlgO4lFH3ezKJpuFa8WvxNBw1oBe6fOX8ZvxjZ5BZIU72EgOZxw1svXhlZVwo9SMPg400n1ecPGzWiVeJ-BVDIrbMV_y0ZKmo9lZzlKel94Ai3x4hedJf7KAxM497dSQt0H70inFuDYS6Z9MReDL-98lsYIJ06aictBmz0PY-sgaFSYyJ-WSU0Kb6fhsuhFDaUy8Z4jLWGbs4Qil3zl62CGXw4t3q7987rZ7Wn2xjw1bU3_NpAdermQppkwutWkofjyw1nnFZ6_V9jwO0ERT6nYfzBZETzBX6s_MjwgLv1OBYU7NaDhb57u1_G-pZ1tUQ5OJE&key=AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg",
      "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference=AciIO2fcMfAzDZgCD-JsCVYY7PLfSdZXg1u7YYNF8fayn4Xb5zes7qlqFAlXJ3t67MYhac2wXfZMC4XxzGGo1eIx3KZJPAISye3r__wgb6gjUIfJA7Sie8PzvyRyDE2BuKhsViv9iIJXwMjJxEiJQGdjxQyitns6tcGT-8nOpA2-tMFnE08tbFdUuV95Kkbby68pHRHfZSNxJL8y88w6GR5D17N7vMZ7FoS1JIqNhGmHe7uDmXew3EPsks0euPtBF9RjGsZEeyEkFYykUSbyV1EmYuqFAzakpnQDy1JHMfFNXxEMbJJfAb8ioGgOlF9PS8Yga6VV5Azxd6rJYa6gbeuST4qA4GIqkRG0vKS2kXhKgH4YnnxJ2JatniVwC6igli-58OAKjFH3UUeYS4yajZPbmClpE4pdYSm8d4vqUTlwWeGghQ&key=AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg",
      "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference=AciIO2eUM27kZ5N6Pt4JHI4OWJJfLJPuwy_KHbjrzPd42nYc6aVuMK3iNw92sA-vZFhQupCElCYrKsR8JAqBdSOyNNT-FfMQv2FJIkWuddKt7Oo9ypmrGjKcSFhqEvMPkVJZ6q8Fi-6JWZmcPfHtnkuCMf9iELT7ydI1n0eCymFVmLCHoyCzRB_YKMW9mHxEZ7sjXa0Y7WP82c_Ome6jxMtvYstpL67-uAFfsWo-crGk5xV1WmaO7dISYJ3DXDMXSm4L0xhSM3cm9O9l7TeICAGGbFIJpW3Nt0-1LBIPrrQLHPHWsQRkOUiBtJnZjCO7LXJWXNo_wWtekN4CJq_fWDZ7j7F17vK4pRgdjBv5mB1MEcXntEIINfnofND3vAQZpBK24r3y1Dwvi1265qV5Kgc5Mp1nAl_h7v0HuFIXqJi1zKn5vQ&key=AIzaSyBlOgil_jAHzwKulAXTeTSxW_WtpQjCicg"
    ],
    "assessment": {
      "water_quality": {
        "clarity": 0.5840048052527094,
        "pollution": 0.6807807640466429,
        "fish_stock": 0.535913482603074
      },
      "recommendations": []
    }
  }
]
 */
