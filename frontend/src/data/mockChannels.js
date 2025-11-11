/**
 * Mock Channel Data
 * TODO: Replace with real API call when backend is ready
 * API endpoint: /api/method/mira.api.channels.get_available
 */

export const mockChannels = [
  {
    id: 'facebook',
    label: 'Facebook',
    icon: 'facebook',
    description: 'Post job openings to Facebook pages',
    color: 'blue',
    features: {
      presentation: 'Text Area, Image/Video, View More button',
      tracking: 'Auto-track URL clicks from Landing Page',
      utm_source: 'facebook'
    },
    enabled: true
  },
  {
    id: 'zalo',
    label: 'Zalo',
    icon: 'message-circle',
    description: 'Share job posts on Zalo',
    color: 'green',
    features: {
      presentation: 'Text Area, Image (no video), View More button',
      tracking: 'Auto-track URL clicks from Landing Page',
      utm_source: 'zalo'
    },
    enabled: true
  },
  {
    id: 'linkedin',
    label: 'LinkedIn',
    icon: 'linkedin',
    description: 'Share to LinkedIn company page',
    color: 'blue-700',
    features: {
      presentation: 'Text Area, Image/Video, Article link',
      tracking: 'Auto-track URL clicks from Landing Page',
      utm_source: 'linkedin'
    },
    enabled: false // Coming soon
  },
  {
    id: 'twitter',
    label: 'Twitter',
    icon: 'twitter',
    description: 'Tweet job openings',
    color: 'sky',
    features: {
      presentation: 'Text (280 chars), Image, Link preview',
      tracking: 'Auto-track URL clicks from Landing Page',
      utm_source: 'twitter'
    },
    enabled: false // Coming soon
  },
  {
    id: 'instagram',
    label: 'Instagram',
    icon: 'instagram',
    description: 'Post to Instagram business account',
    color: 'pink',
    features: {
      presentation: 'Image/Video, Caption, Story',
      tracking: 'Link in bio tracking',
      utm_source: 'instagram'
    },
    enabled: false // Coming soon
  }
]

/**
 * Get available channels (enabled only)
 */
export function getAvailableChannels() {
  return mockChannels.filter(channel => channel.enabled)
}

/**
 * Get all channels (including disabled)
 */
export function getAllChannels() {
  return mockChannels
}

/**
 * Get channel by ID
 */
export function getChannelById(id) {
  return mockChannels.find(channel => channel.id === id)
}

/**
 * Get channel options for dropdown
 */
export function getChannelOptions() {
  return getAvailableChannels().map(channel => ({
    label: channel.label,
    value: channel.id,
    icon: channel.icon
  }))
}

/**
 * Generate UTM parameters for channel
 */
export function generateUTMParams(channelId, campaignName, tags = []) {
  const channel = getChannelById(channelId)
  if (!channel) return {}

  return {
    utm_source: channel.features.utm_source,
    utm_campaign: campaignName || 'campaign',
    utm_medium: 'social',
    utm_content: channelId,
    utm_tag: tags.join(',')
  }
}

/**
 * Build URL with UTM parameters
 */
export function buildTrackingUrl(baseUrl, channelId, campaignName, tags = []) {
  const params = generateUTMParams(channelId, campaignName, tags)
  const urlParams = new URLSearchParams(params)
  return `${baseUrl}?${urlParams.toString()}`
}
