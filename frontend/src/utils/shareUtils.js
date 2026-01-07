

/**
 * Generate SEO-friendly URL for job opening (frontend only)
 * @param {string} jobUrlCms - Prebuilt CMS job URL segment
 * @param {Object} utmParams - UTM parameters
 * @returns {string} SEO-friendly URL
 */
export function generateJobShareUrl(jobUrlCms, utmParams = {}) {
  try {
    const cleanSegment = (jobUrlCms || '').toString().trim()
    const baseUrl = `${window.location.origin}/mbw_transition_hub/jobs/${cleanSegment}`
    
    // Add UTM parameters if provided
    const utmSearchParams = new URLSearchParams()
    if (utmParams.utm_source) utmSearchParams.set('utm_source', utmParams.utm_source)
    if (utmParams.utm_medium) utmSearchParams.set('utm_medium', utmParams.utm_medium)
    if (utmParams.utm_campaign) utmSearchParams.set('utm_campaign', utmParams.utm_campaign)
    if (utmParams.utm_content) utmSearchParams.set('utm_content', utmParams.utm_content)

    return utmSearchParams.toString() ? `${baseUrl}?${utmSearchParams.toString()}` : baseUrl
  } catch (error) {
    console.error('Error generating share URL:', error)
    // Fallback to simple URL using provided segment
    return `${window.location.origin}/mbw_transition_hub/jobs/${jobUrlCms || ''}`
  }
}

/**
 * Copy URL to clipboard
 * @param {string} url - URL to copy
 * @returns {Promise<boolean>} Success status
 */
export async function copyUrlToClipboard(url) {
  try {
    // Modern clipboard API (requires HTTPS)
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(url)
      return true
    }
    
    // Fallback method for older browsers or HTTP
    const textArea = document.createElement('textarea')
    textArea.value = url
    textArea.style.position = 'fixed'
    textArea.style.left = '-999999px'
    textArea.style.top = '-999999px'
    document.body.appendChild(textArea)
    textArea.focus()
    textArea.select()
    
    const successful = document.execCommand('copy')
    document.body.removeChild(textArea)
    
    if (successful) {
      return true
    } else {
      throw new Error('execCommand copy failed')
    }
  } catch (error) {
    console.error('Error copying URL:', error)
    
    // Last resort: show URL in alert
    try {
      alert(`URL đã được copy: ${url}`)
      return true
    } catch (alertError) {
      console.error('Alert also failed:', alertError)
      return false
    }
  }
}

/**
 * Share on social media platforms
 * @param {string} platform - Platform name (facebook, linkedin, twitter, whatsapp, telegram, email)
 * @param {string} url - URL to share
 * @param {string} title - Title for sharing
 * @param {string} description - Description for sharing
 */
export function shareOnSocialMedia(platform, url, title = '', description = '') {
  const encodedUrl = encodeURIComponent(url)
  const encodedTitle = encodeURIComponent(title)
  const encodedDescription = encodeURIComponent(description)
  
  let shareUrl
  switch (platform.toLowerCase()) {
    case 'facebook':
      shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`
      break
    case 'linkedin':
      shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`
      break
    case 'twitter':
      shareUrl = `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`
      break
    case 'whatsapp':
      shareUrl = `https://wa.me/?text=${encodedTitle}%20${encodedUrl}`
      break
    case 'telegram':
      shareUrl = `https://t.me/share/url?url=${encodedUrl}&text=${encodedTitle}`
      break
    case 'email':
      const emailSubject = encodeURIComponent(title)
      const emailBody = encodeURIComponent(`${description}\n\nXem chi tiết tại: ${url}`)
      shareUrl = `mailto:?subject=${emailSubject}&body=${emailBody}`
      break
    default:
      console.error('Unsupported platform:', platform)
      return
  }
  
  if (platform.toLowerCase() === 'email') {
    // For email, we don't need to open a popup
    window.location.href = shareUrl
  } else {
    window.open(shareUrl, '_blank', 'width=600,height=400')
  }
}

/**
 * Track UTM parameters from URL
 * @param {string} jobId - Job opening ID
 * @returns {Promise<Object|null>} UTM data or null if no UTM parameters
 */
export async function trackUTMParameters(jobId) {
  const urlParams = new URLSearchParams(window.location.search)
  const utmSource = urlParams.get('utm_source')
  const utmMedium = urlParams.get('utm_medium')
  const utmCampaign = urlParams.get('utm_campaign')
  const utmContent = urlParams.get('utm_content')
  
  if (utmSource || utmMedium || utmCampaign || utmContent) {
    const utmData = {
      utm_source: utmSource,
      utm_medium: utmMedium,
      utm_campaign: utmCampaign,
      utm_content: utmContent,
      job_id: jobId,
      timestamp: new Date().toISOString(),
      url: window.location.href
    }
    
    // Store in localStorage
    localStorage.setItem('job_utm_data', JSON.stringify(utmData))
    
    // Send to backend for tracking
    try {
      const { call } = await import('frappe-ui')
      await call('mbw_transition_hub.mbw_transition_hub.doctype.ats_jobopening.api.track_utm_visit', {
        job_id: jobId,
        utm_source: utmSource,
        utm_medium: utmMedium,
        utm_campaign: utmCampaign,
        utm_content: utmContent,
        session_id: generateSessionId()
      })
      console.log('UTM Parameters tracked and saved to database:', utmData)
    } catch (error) {
      console.error('Error tracking UTM parameters:', error)
    }
    
    return utmData
  }
  
  return null
}

/**
 * Generate unique session ID
 * @returns {string} Session ID
 */
function generateSessionId() {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
}

/**
 * Get stored UTM data
 * @returns {Object|null} Stored UTM data or null
 */
export function getStoredUTMData() {
  try {
    const stored = localStorage.getItem('job_utm_data')
    return stored ? JSON.parse(stored) : null
  } catch (error) {
    console.error('Error getting stored UTM data:', error)
    return null
  }
}

/**
 * Clear stored UTM data
 */
export function clearStoredUTMData() {
  localStorage.removeItem('job_utm_data')
}

/**
 * Generate UTM parameters for common sources
 * @param {string} source - Source name
 * @param {string} campaign - Campaign name
 * @param {string} content - Content identifier
 * @returns {Object} UTM parameters object
 */
export function generateUTMParameters(source, campaign, content = '') {
  const utmParams = {
    utm_source: source,
    utm_medium: getMediumBySource(source),
    utm_campaign: campaign,
    utm_content: content
  }
  
  return utmParams
}

/**
 * Get medium based on source
 * @param {string} source - Source name
 * @returns {string} Medium name
 */
function getMediumBySource(source) {
  const sourceMediumMap = {
    'facebook': 'social',
    'linkedin': 'social',
    'twitter': 'social',
    'instagram': 'social',
    'youtube': 'social',
    'email': 'email',
    'newsletter': 'email',
    'google': 'cpc',
    'bing': 'cpc',
    'internal': 'referral',
    'referral': 'referral'
  }
  
  return sourceMediumMap[source.toLowerCase()] || 'social'
}

/**
 * Validate UTM parameters
 * @param {Object} utmParams - UTM parameters object
 * @returns {boolean} Validation result
 */
export function validateUTMParameters(utmParams) {
  const required = ['utm_source', 'utm_medium', 'utm_campaign']
  
  for (const field of required) {
    if (!utmParams[field] || utmParams[field].trim() === '') {
      return false
    }
  }
  
  return true
}
