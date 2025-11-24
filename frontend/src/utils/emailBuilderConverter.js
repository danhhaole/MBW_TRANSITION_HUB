import { blocksToMJML } from '@/components/Settings/MiraEmailTemplate/EmailBuilder/utils.js'
import mjml2html from 'mjml-browser'

/**
 * Convert EmailBuilder blocks format to HTML/CSS for storage and rendering
 * @param {Object} emailBuilderData - { blocks: [], emailSettings: {} }
 * @returns {Object} - { html: string, css: string, mjml: string }
 */
export function convertEmailBuilderToHtml(emailBuilderData) {
  if (!emailBuilderData || !emailBuilderData.blocks) {
    return { html: '', css: '', mjml: '' }
  }

  try {
    const { blocks, emailSettings } = emailBuilderData
    
    // Generate MJML from blocks
    const mjml = blocksToMJML(blocks, emailSettings)
    
    // Convert MJML to HTML
    const { html, errors } = mjml2html(mjml)
    
    if (errors && errors.length > 0) {
      console.warn('MJML conversion warnings:', errors)
    }
    
    // Extract inline CSS from HTML (MJML generates inline styles)
    const cssExtracted = extractInlineStyles(html)
    
    return {
      html: cssExtracted.html,
      css: cssExtracted.css,
      mjml: mjml
    }
  } catch (error) {
    console.error('Error converting EmailBuilder to HTML:', error)
    return { html: '', css: '', mjml: '' }
  }
}

/**
 * Convert HTML/CSS back to EmailBuilder blocks format (basic conversion)
 * @param {string} html - HTML content
 * @param {string} css - CSS content (optional)
 * @returns {Object} - { blocks: [], emailSettings: {} }
 */
export function convertHtmlToEmailBuilder(html, css = '') {
  if (!html) {
    return { blocks: [], emailSettings: getDefaultEmailSettings() }
  }

  try {
    // Create a temporary DOM element to parse HTML
    const parser = new DOMParser()
    const doc = parser.parseFromString(html, 'text/html')
    
    const blocks = []
    let blockId = Date.now()
    
    // Extract email settings from body styles
    const emailSettings = extractEmailSettingsFromHtml(doc)
    
    // Find main content container (usually mj-body or similar)
    const contentContainer = doc.querySelector('body') || doc.querySelector('[role="main"]') || doc
    
    // Convert common HTML elements to blocks
    const elements = contentContainer.querySelectorAll('p, h1, h2, h3, h4, h5, h6, img, hr, div[style*="border"], table')
    
    elements.forEach(element => {
      const block = convertElementToBlock(element, blockId++)
      if (block) {
        blocks.push(block)
      }
    })
    
    // If no blocks found, create a basic text block with the content
    if (blocks.length === 0 && html.trim()) {
      blocks.push({
        id: blockId,
        type: 'text',
        props: {
          content: html.replace(/<[^>]*>/g, ''), // Strip HTML tags
          ...getDefaultTextProps()
        }
      })
    }
    
    return { blocks, emailSettings }
  } catch (error) {
    console.error('Error converting HTML to EmailBuilder:', error)
    return { blocks: [], emailSettings: getDefaultEmailSettings() }
  }
}

/**
 * Extract inline styles and convert to separate CSS
 * @param {string} html - HTML with inline styles
 * @returns {Object} - { html: string, css: string }
 */
function extractInlineStyles(html) {
  // For now, keep inline styles as MJML generates responsive email-friendly CSS
  // In the future, we could extract common styles to a separate CSS block
  return {
    html: html,
    css: '' // MJML handles responsive CSS inline
  }
}

/**
 * Extract email settings from HTML document
 * @param {Document} doc - Parsed HTML document
 * @returns {Object} - Email settings object
 */
function extractEmailSettingsFromHtml(doc) {
  const body = doc.querySelector('body')
  const settings = getDefaultEmailSettings()
  
  if (body) {
    // Extract background color
    const bgColor = body.style.backgroundColor || getComputedStyleValue(body, 'background-color')
    if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)' && bgColor !== 'transparent') {
      settings.backgroundColor = bgColor
    }
    
    // Extract font family from body or main container
    const fontFamily = body.style.fontFamily || getComputedStyleValue(body, 'font-family')
    if (fontFamily) {
      settings.fontFamily = fontFamily
    }
  }
  
  // Try to detect content width from main container
  const mainContainer = doc.querySelector('[style*="width"]') || doc.querySelector('table[width]')
  if (mainContainer) {
    const width = mainContainer.style.width || mainContainer.getAttribute('width')
    if (width) {
      const numericWidth = parseInt(width)
      if (numericWidth >= 300 && numericWidth <= 800) {
        settings.contentWidth = numericWidth
      }
    }
  }
  
  return settings
}

/**
 * Convert HTML element to EmailBuilder block
 * @param {Element} element - HTML element
 * @param {number} id - Block ID
 * @returns {Object|null} - Block object or null
 */
function convertElementToBlock(element, id) {
  const tagName = element.tagName.toLowerCase()
  
  switch (tagName) {
    case 'p':
    case 'h1':
    case 'h2':
    case 'h3':
    case 'h4':
    case 'h5':
    case 'h6':
    case 'div':
      if (element.textContent.trim()) {
        return {
          id,
          type: 'text',
          props: {
            content: element.innerHTML,
            textType: tagName === 'p' ? 'paragraph' : 'heading',
            ...extractTextStyles(element),
            ...getDefaultTextProps()
          }
        }
      }
      break
      
    case 'img':
      return {
        id,
        type: 'image',
        props: {
          src: element.src || element.getAttribute('src') || '',
          alt: element.alt || 'Image',
          width: parseInt(element.width) || 600,
          height: parseInt(element.height) || null,
          ...extractImageStyles(element),
          ...getDefaultImageProps()
        }
      }
      
    case 'hr':
      return {
        id,
        type: 'divider',
        props: {
          ...extractDividerStyles(element),
          ...getDefaultDividerProps()
        }
      }
  }
  
  return null
}

/**
 * Extract text styles from element
 * @param {Element} element - HTML element
 * @returns {Object} - Style properties
 */
function extractTextStyles(element) {
  const styles = {}
  const computedStyle = window.getComputedStyle ? window.getComputedStyle(element) : element.style
  
  if (computedStyle.color) styles.color = computedStyle.color
  if (computedStyle.fontSize) styles.fontSize = parseInt(computedStyle.fontSize) || 16
  if (computedStyle.fontFamily) styles.fontFamily = computedStyle.fontFamily
  if (computedStyle.fontWeight) styles.fontWeight = computedStyle.fontWeight
  if (computedStyle.textAlign) styles.textAlign = computedStyle.textAlign
  if (computedStyle.backgroundColor && computedStyle.backgroundColor !== 'rgba(0, 0, 0, 0)') {
    styles.backgroundColor = computedStyle.backgroundColor
  }
  
  return styles
}

/**
 * Extract image styles from element
 * @param {Element} element - HTML element
 * @returns {Object} - Style properties
 */
function extractImageStyles(element) {
  const styles = {}
  const computedStyle = window.getComputedStyle ? window.getComputedStyle(element) : element.style
  
  if (computedStyle.textAlign) styles.align = computedStyle.textAlign
  if (computedStyle.border && computedStyle.border !== 'none') {
    styles.hasBorder = true
    styles.borderWidth = parseInt(computedStyle.borderWidth) || 1
    styles.borderColor = computedStyle.borderColor || '#e5e7eb'
  }
  if (computedStyle.borderRadius) {
    styles.borderRadius = parseInt(computedStyle.borderRadius) || 0
  }
  
  return styles
}

/**
 * Extract divider styles from element
 * @param {Element} element - HTML element
 * @returns {Object} - Style properties
 */
function extractDividerStyles(element) {
  const styles = {}
  const computedStyle = window.getComputedStyle ? window.getComputedStyle(element) : element.style
  
  if (computedStyle.height) styles.height = parseInt(computedStyle.height) || 4
  if (computedStyle.borderColor) styles.borderColor = computedStyle.borderColor
  if (computedStyle.borderStyle) styles.style = computedStyle.borderStyle
  
  return styles
}

/**
 * Get computed style value safely
 * @param {Element} element - HTML element
 * @param {string} property - CSS property
 * @returns {string} - Style value
 */
function getComputedStyleValue(element, property) {
  if (window.getComputedStyle) {
    return window.getComputedStyle(element).getPropertyValue(property)
  }
  return element.style[property] || ''
}

/**
 * Get default email settings
 * @returns {Object} - Default email settings
 */
function getDefaultEmailSettings() {
  return {
    backgroundColor: '#ffffff',
    contentWidth: 600,
    contentAlign: 'center',
    fontFamily: 'Arial, sans-serif'
  }
}

/**
 * Get default text block properties
 * @returns {Object} - Default text props
 */
function getDefaultTextProps() {
  return {
    height: null,
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    textType: 'paragraph',
    fontFamily: 'Arial, sans-serif',
    fontSize: 16,
    color: '#000000',
    lineHeight: '1.4',
    fontStyle: 'normal',
    fontWeight: 'normal',
    textDecoration: 'none',
    letterSpacing: 0,
    backgroundColor: 'transparent',
    textAlign: 'left',
    padding: 20
  }
}

/**
 * Get default image block properties
 * @returns {Object} - Default image props
 */
function getDefaultImageProps() {
  return {
    href: '',
    fileName: '',
    fileSize: 0,
    fullWidthMobile: false,
    widthType: 'fixed',
    width: 600,
    height: null,
    paddingTop: 20,
    paddingBottom: 20,
    paddingLeft: 20,
    paddingRight: 20,
    hasBorder: false,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    borderRadius: 0,
    backgroundColor: 'transparent',
    align: 'center',
    padding: 20
  }
}

/**
 * Get default divider block properties
 * @returns {Object} - Default divider props
 */
function getDefaultDividerProps() {
  return {
    height: 4,
    style: 'solid',
    borderColor: '#e5e7eb',
    width: '100%',
    customWidth: 300,
    paddingTop: 20,
    paddingBottom: 20,
    paddingLeft: 0,
    paddingRight: 0,
    backgroundColor: 'transparent',
    align: 'center',
    borderWidth: 1,
    padding: 20
  }
}

/**
 * Validate EmailBuilder data format
 * @param {any} data - Data to validate
 * @returns {boolean} - Is valid EmailBuilder format
 */
export function isEmailBuilderFormat(data) {
  if (!data || typeof data !== 'object') return false
  return Array.isArray(data.blocks) && typeof data.emailSettings === 'object'
}

/**
 * Validate HTML format
 * @param {any} data - Data to validate
 * @returns {boolean} - Is HTML format
 */
export function isHtmlFormat(data) {
  if (typeof data !== 'string') return false
  return data.trim().startsWith('<') && data.includes('>')
}
