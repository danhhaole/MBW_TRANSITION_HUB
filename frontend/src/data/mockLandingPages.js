/**
 * Mock Landing Page Data
 * TODO: Replace with real API call when backend is ready
 * API endpoint: /api/method/mira.api.landing_pages.get_list
 */

export const mockLandingPages = [
  {
    value: 'landing-page-1',
    label: 'Job Opening - Software Engineer',
    url: '/landing/job-software-engineer',
    description: 'Landing page for Software Engineer position',
    form_connected: true,
    created_at: '2024-01-15'
  },
  {
    value: 'landing-page-2',
    label: 'Job Opening - Marketing Manager',
    url: '/landing/job-marketing-manager',
    description: 'Landing page for Marketing Manager position',
    form_connected: true,
    created_at: '2024-01-20'
  },
  {
    value: 'landing-page-3',
    label: 'Job Opening - Sales Executive',
    url: '/landing/job-sales-executive',
    description: 'Landing page for Sales Executive position',
    form_connected: true,
    created_at: '2024-02-01'
  },
  {
    value: 'landing-page-4',
    label: 'Career Page - General',
    url: '/landing/career-general',
    description: 'General career opportunities page',
    form_connected: true,
    created_at: '2024-02-10'
  },
  {
    value: 'landing-page-5',
    label: 'Job Opening - Product Designer',
    url: '/landing/job-product-designer',
    description: 'Landing page for Product Designer position',
    form_connected: false, // Not connected yet
    created_at: '2024-03-01'
  }
]

/**
 * Get landing page options for dropdown
 */
export function getLandingPageOptions() {
  return mockLandingPages.map(page => ({
    label: page.label,
    value: page.value,
    // Can add icon, description, etc. if needed
  }))
}

/**
 * Get landing page by ID
 */
export function getLandingPageById(id) {
  return mockLandingPages.find(page => page.value === id)
}

/**
 * Get full URL for landing page
 */
export function getLandingPageUrl(pageId) {
  const page = getLandingPageById(pageId)
  if (!page) return ''
  
  const baseUrl = window.location.origin
  return `${baseUrl}${page.url}`
}

/**
 * Check if landing page form is connected
 */
export function isFormConnected(pageId) {
  const page = getLandingPageById(pageId)
  return page?.form_connected || false
}
