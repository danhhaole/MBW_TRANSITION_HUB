/**
 * Helper functions for Unlayer Email Editor
 */

/**
 * Create a proper Unlayer design structure from HTML content
 * @param {string} htmlContent - HTML content to convert
 * @returns {Object} Unlayer design object
 */
export function createUnlayerDesignFromHtml(htmlContent) {
  console.log('[unlayerHelper] Creating design from HTML:', htmlContent?.substring(0, 100))
  
  const design = {
    counters: {
      u_column: 1,
      u_row: 1,
      u_content_text: 1
    },
    body: {
      id: 'body_' + Date.now(),
      rows: [
        {
          id: 'row_' + Date.now(),
          cells: [1],
          columns: [
            {
              id: 'column_' + Date.now(),
              contents: [
                {
                  id: 'content_text_' + Date.now(),
                  type: 'text',
                  values: {
                    text: htmlContent || '<p style="line-height: 140%;">Start designing your email...</p>',
                    containerPadding: '10px',
                    anchor: '',
                    fontSize: '14px',
                    textAlign: 'left',
                    lineHeight: '140%',
                    linkStyle: {
                      inherit: true,
                      linkColor: '#0000ee',
                      linkHoverColor: '#0000ee',
                      linkUnderline: true,
                      linkHoverUnderline: true
                    },
                    displayCondition: null,
                    _styleGuide: null,
                    _meta: {
                      htmlID: 'u_content_text_1',
                      htmlClassNames: 'u_content_text'
                    },
                    selectable: true,
                    draggable: true,
                    duplicatable: true,
                    deletable: true,
                    hideable: true,
                    locked: false,
                    _languages: {}
                  }
                }
              ],
              values: {
                backgroundColor: '',
                padding: '0px',
                border: {},
                borderRadius: '0px',
                _meta: {
                  htmlID: 'u_column_1',
                  htmlClassNames: 'u_column'
                },
                deletable: true,
                locked: false
              }
            }
          ],
          values: {
            displayCondition: null,
            columns: false,
            _styleGuide: null,
            backgroundColor: '',
            columnsBackgroundColor: '',
            backgroundImage: {
              url: '',
              fullWidth: true,
              repeat: 'no-repeat',
              size: 'custom',
              position: 'center',
              customPosition: ['50%', '50%']
            },
            padding: '0px',
            anchor: '',
            hideDesktop: false,
            _meta: {
              htmlID: 'u_row_1',
              htmlClassNames: 'u_row'
            },
            selectable: true,
            draggable: true,
            duplicatable: true,
            deletable: true,
            hideable: true,
            locked: false
          }
        }
      ],
      headers: [],
      footers: [],
      values: {
        _styleGuide: null,
        popupPosition: 'center',
        popupDisplayDelay: 0,
        popupWidth: '600px',
        popupHeight: 'auto',
        borderRadius: '10px',
        contentAlign: 'center',
        contentVerticalAlign: 'center',
        contentWidth: '500px',
        fontFamily: {
          label: 'Arial',
          value: 'arial,helvetica,sans-serif'
        },
        textColor: '#000000',
        popupBackgroundColor: '#FFFFFF',
        popupBackgroundImage: {
          url: '',
          fullWidth: true,
          repeat: 'no-repeat',
          size: 'cover',
          position: 'center'
        },
        popupOverlay_backgroundColor: 'rgba(0, 0, 0, 0.1)',
        popupCloseButton_position: 'top-right',
        popupCloseButton_backgroundColor: '#DDDDDD',
        popupCloseButton_iconColor: '#000000',
        popupCloseButton_borderRadius: '0px',
        popupCloseButton_margin: '0px',
        popupCloseButton_action: {
          name: 'close_popup',
          attrs: {
            onClick: "document.querySelector('.u-popup-container').style.display = 'none';"
          }
        },
        language: {},
        backgroundColor: '#F7F8F9',
        preheaderText: '',
        linkStyle: {
          body: true,
          linkColor: '#0000ee',
          linkHoverColor: '#0000ee',
          linkUnderline: true,
          linkHoverUnderline: true
        },
        backgroundImage: {
          url: '',
          fullWidth: true,
          repeat: 'no-repeat',
          size: 'custom',
          position: 'center'
        },
        _meta: {
          htmlID: 'u_body',
          htmlClassNames: 'u_body'
        }
      }
    },
    schemaVersion: 21
  }
  
  // Validate before returning
  const isValid = isValidUnlayerDesign(design)
  console.log('[unlayerHelper] Design created, valid:', isValid)
  console.log('[unlayerHelper] Design structure:', JSON.stringify(design, null, 2).substring(0, 500))
  
  return design
}

/**
 * Validate if a design object has proper Unlayer structure
 * @param {Object} design - Design object to validate
 * @returns {boolean} True if valid
 */
export function isValidUnlayerDesign(design) {
  if (!design || typeof design !== 'object') return false
  
  return (
    design.body &&
    design.body.rows &&
    Array.isArray(design.body.rows) &&
    design.schemaVersion
  )
}

/**
 * Extract HTML content from Unlayer design
 * @param {Object} design - Unlayer design object
 * @returns {string|null} HTML content or null
 */
export function extractHtmlFromDesign(design) {
  if (!isValidUnlayerDesign(design)) return null
  
  try {
    const firstRow = design.body.rows[0]
    if (!firstRow || !firstRow.columns || !firstRow.columns[0]) return null
    
    const firstContent = firstRow.columns[0].contents[0]
    if (firstContent && firstContent.type === 'html' && firstContent.values) {
      return firstContent.values.html
    }
  } catch (error) {
    console.error('Error extracting HTML from design:', error)
  }
  
  return null
}
