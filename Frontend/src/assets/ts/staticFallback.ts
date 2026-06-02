const base = import.meta.env.BASE_URL || '/'

export const staticActivities = [
  {
    date: '2025-09-19 14:00:00+00:00',
    name: 'Beach Clean-up',
    id: '6e31457f67c54a3a81519e204b2aa211',
    description: 'Join the community to remove plastics and keep Port Phillip Bay clean.',
    start: '2025-09-19 23:30:00+00:00',
    end: '2025-09-20 01:30:00+00:00',
    location: 'Port Melbourne',
    tags: "['community', 'plastics', 'kids']",
    image: 'clean-up.png',
  },
  {
    date: '2025-09-05 14:00:00+00:00',
    name: 'Shell & Fish Count Walk',
    id: '33cd8a19380b40458b57f4b6632abc73',
    description: 'Join a guided walk to record shells and small fish along the shore.',
    start: '2025-09-05 23:30:00+00:00',
    end: '2025-09-06 01:00:00+00:00',
    location: 'St Kilda',
    tags: "['shell-walk', 'fish-count', 'beach-walk']",
    image: 'shell-fish-count.png',
  },
  {
    date: '2025-09-09 14:00:00+00:00',
    name: 'Poster-Making for Schools',
    id: '0d0689c7cbd4442597f337a4df873345',
    description: 'Create colorful Protect the Bay posters to share in your classroom.',
    start: '2025-09-10 05:30:00+00:00',
    end: '2025-09-10 07:00:00+00:00',
    location: 'Luna Park',
    tags: "['poster-making', 'art-for-ocean']",
    image: 'poster-making.png',
  },
  {
    date: '2025-09-12 14:00:00+00:00',
    name: 'Seashell Art Workshop',
    id: '0e9198874e724e31b8845b76b845bed9',
    description: 'Collect clean seashells and turn them into creative art pieces.',
    start: '2025-09-13 00:00:00+00:00',
    end: '2025-09-13 01:30:00+00:00',
    location: 'Cherry Lake',
    tags: "['art-workshop', 'marine-education']",
    image: 'seashell-art.png',
  },
  {
    date: '2025-09-26 14:00:00+00:00',
    name: 'Seagrass Discovery Snorkel',
    id: 'abcb906e431841cdaf186ba530dca9dd',
    description: 'Try snorkeling to see seagrass meadows and the fish that live in them.',
    start: '2025-09-27 01:00:00+00:00',
    end: '2025-09-27 02:30:00+00:00',
    location: 'Mordialloc Beach',
    tags: "['marine-life', 'mordialloc-beach']",
    image: 'seagrass-discovery.png',
  },
  {
    date: '2025-09-27 14:00:00+00:00',
    name: 'Rock Pool Explorer',
    id: 'bd010206077b485d90c1cc3939773bb6',
    description: 'Search for crabs, starfish, and sea snails in shallow rock pools.',
    start: '2025-09-28 04:00:00+00:00',
    end: '2025-09-28 05:30:00+00:00',
    location: 'Dromana Beach',
    tags: "['nature-learning', 'rock-pool-exploration']",
    image: 'rock-pool.png',
  },
]

export const staticPlaces = [
  { label: 'St Kilda Beach, Victoria, Australia', place_id: 'demo-st-kilda', name: 'St Kilda Beach', lat: -37.8677, lng: 144.9769, suburbName: 'St Kilda' },
  { label: 'Brighton Beach, Victoria, Australia', place_id: 'demo-brighton', name: 'Brighton Beach', lat: -37.9264, lng: 144.9863, suburbName: 'Brighton' },
  { label: 'Dromana Beach, Victoria, Australia', place_id: 'demo-dromana', name: 'Dromana Beach', lat: -38.3335, lng: 144.9644, suburbName: 'Dromana' },
  { label: 'Port Melbourne Beach, Victoria, Australia', place_id: 'demo-port-melbourne', name: 'Port Melbourne Beach', lat: -37.8421, lng: 144.9300, suburbName: 'Port Melbourne' },
]

export const staticSites = [
  {
    site_id: '1229',
    site_name_short: 'Central',
    water_body: 'Port Phillip Bay',
    latitude: -38.0570335388183,
    longitude: 144.870407104492,
    latest_date: '2024-05-16',
    avg_water_quality_simple: 'good',
    do_mg_mean: 8.1375,
    sal_mean: 34.375,
    tss_mean: 1.925,
    n_total_mean: 218.75,
    p_total_mean: 63.75,
  },
  {
    site_id: '1991',
    site_name_short: 'Hobsons Bay',
    water_body: 'Port Phillip Bay',
    latitude: -37.870189666748,
    longitude: 144.933807373046,
    latest_date: '2024-05-16',
    avg_water_quality_simple: 'good',
    do_mg_mean: 8,
    sal_mean: 33.125,
    tss_mean: 5.6125,
    n_total_mean: 260,
    p_total_mean: 77.5,
  },
]

export function activityImageUrl(name: string) {
  return `${base}activity/${encodeURIComponent(name)}`
}

export function staticActivity(id?: number | string) {
  if (!id) return staticActivities
  return staticActivities.filter((activity) => activity.id === String(id))
}

export function staticImage(name: string) {
  if (!name) return null
  return activityImageUrl(name)
}

export function staticSuburb(latitude: string | number, longitude: string | number) {
  const lat = Number(latitude)
  const lng = Number(longitude)
  const nearest = staticPlaces.reduce((best, place) => {
    const distance = Math.abs(place.lat - lat) + Math.abs(place.lng - lng)
    return distance < best.distance ? { place, distance } : best
  }, { place: staticPlaces[0], distance: Number.POSITIVE_INFINITY })

  return {
    suburbName: nearest.place.suburbName,
    state: 'Victoria',
    postcode: '',
    confidence: 0.9,
    source: 'static-demo',
  }
}

export function staticPlacesAutocomplete(q: string, limit = 8) {
  const text = q.trim().toLowerCase()
  const matches = staticPlaces
    .filter((place) => place.label.toLowerCase().includes(text) || place.name.toLowerCase().includes(text))
    .slice(0, limit)
    .map(({ label, place_id }) => ({ label, place_id }))

  return { suggestions: matches.length ? matches : staticPlaces.slice(0, limit).map(({ label, place_id }) => ({ label, place_id })) }
}

export function staticPlaceDetails(placeId: string) {
  const place = staticPlaces.find((item) => item.place_id === placeId) || staticPlaces[0]
  return { name: place.name, lat: place.lat, lng: place.lng }
}

export function staticNearbyBeach(latitude?: string | number, longitude?: string | number) {
  const place = latitude && longitude
    ? staticPlaces.reduce((best, item) => {
      const distance = Math.abs(item.lat - Number(latitude)) + Math.abs(item.lng - Number(longitude))
      return distance < best.distance ? { item, distance } : best
    }, { item: staticPlaces[0], distance: Number.POSITIVE_INFINITY }).item
    : staticPlaces[0]

  return {
    name: place.name,
    location: { lat: place.lat, lon: place.lng },
    photos: [
      `${base}learning/beaches/hero_bay_aerial.jpg`,
      `${base}learning/beaches/brighton_bathing_boxes.jpg`,
      `${base}learning/beaches/st_kilda_penguin.jpg`,
    ],
    assessment: {
      water_quality: { clarity: 0.78, pollution: 0.24, fish_stock: 0.69 },
      recommendations: [
        'Try a family beach clean-up and remove small plastic pieces safely.',
        'Look for seabirds and rock-pool animals without disturbing their habitat.',
        'Check signs and swim between the flags when visiting the beach.',
      ],
    },
    recommendations: {
      attractions: [
        { name: 'St Kilda Pier', rating: 4.5 },
        { name: 'Brighton Bathing Boxes', rating: 4.4 },
        { name: 'Port Phillip Bay Trail', rating: 4.3 },
      ],
      restaurants: [
        { name: 'Beachside Cafe', rating: 4.2, address: 'Near the foreshore' },
        { name: 'Bay View Fish & Chips', rating: 4.1, address: 'Main beach road' },
        { name: 'Local Gelato Shop', rating: 4.3, address: 'Town centre' },
      ],
    },
  }
}

export function staticWaterQuality(siteId: number | string) {
  const site = staticSites.find((item) => item.site_id === String(siteId)) || staticSites[0]
  return [
    {
      record_id: 1,
      site_id: site.site_id,
      site_name_short: site.site_name_short,
      water_body: site.water_body,
      date: '2024-05-16',
      type: 'surface',
      do_mg: site.do_mg_mean,
      sal: site.sal_mean,
      tss: site.tss_mean,
      n_total: site.n_total_mean,
      p_total: site.p_total_mean,
      water_quality_simple: site.avg_water_quality_simple,
      site,
    },
  ]
}

export function staticFishInfo(name: string) {
  const displayName = name?.trim() || 'Ocean Friend'
  return {
    Complete_Base_Marine_Identity: {
      Species_Name_CN: '海龙',
      Species_Name_EN: 'Weedy Seadragon',
      Core_Feature_CN: '像海草一样伪装自己，安静地生活在澳大利亚南部海域。',
      Age_Size_Description_CN: '体型轻盈，适合在海草和礁石附近活动。',
      Personality_CN: '安静、细心、有观察力，擅长发现海洋里的小变化。',
      Habitat_CN: '常见于海草床、浅海礁石和较平静的海湾环境。',
      Fun_Story_CN: '它提醒我们保护海草床，因为那里是很多海洋生物的家。',
      Wikipedia_Image_URL: 'https://upload.wikimedia.org/wikipedia/commons/9/95/Phyllopteryx_taeniolatus1.jpg',
    },
    Personified_Fish_ID_Card: {
      Name: displayName,
      Species: 'Weedy Seadragon',
      Age: 'Young Explorer',
      Personality: 'Curious and careful',
      Hobbies: 'Exploring seagrass meadows and protecting tiny sea creatures',
      Special_Feature: 'Excellent camouflage and strong observation skills',
    },
  }
}
