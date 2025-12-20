import mjml2html from 'mjml-browser'

// Helper to convert nested child blocks to MJML
function childrenToMJML(children) {
  if (!children || children.length === 0) {
    return '<mj-text></mj-text>'
  }
  return children.map(child => {
    // Render content blocks (no section wrapper for children)
    switch (child.type) {
      case 'text':
        // Convert newlines to <br> tags for nested text blocks too
        let nestedTextContent = child.props.content || ''
        if (nestedTextContent && !nestedTextContent.includes('<br>') && !nestedTextContent.includes('<p>')) {
          nestedTextContent = nestedTextContent.replace(/\n/g, '<br>')
        }
        return `<mj-text font-size="${child.props.fontSize}px" color="${child.props.color}" padding="${child.props.padding}px">${nestedTextContent}</mj-text>`
      case 'button':
        return `<mj-button href="${child.props.href}" background-color="${child.props.backgroundColor}" color="${child.props.color}" padding="${child.props.padding}px">${child.props.text}</mj-button>`
      case 'image':
        return `<mj-image src="${child.props.src}" alt="${child.props.alt}" width="${child.props.width}px" padding="${child.props.padding}px" />`
      case 'divider':
        return `<mj-divider border-color="${child.props.borderColor}" border-width="${child.props.borderWidth}px" padding="${child.props.padding}px" />`
      case 'spacer':
        return `<mj-spacer height="${child.props.height}px" />`
      default:
        return '<mj-text></mj-text>'
    }
  }).join('\n')
}

export function blockToMJML(block) {
  switch (block.type) {
    // Layouts with nested children
    case 'col-1':
      return `<mj-section css-class="compact-section" padding="${block.props.padding}px">
        <mj-column css-class="compact-column">${block.children && block.children[0] ? childrenToMJML(block.children[0]) : '<mj-text></mj-text>'}</mj-column>
      </mj-section>`

    case 'col-2-50-50':
      return `<mj-section css-class="compact-section" padding="${block.props.padding}px">
        <mj-column css-class="compact-column" width="50%">${block.children && block.children[0] ? childrenToMJML(block.children[0]) : '<mj-text></mj-text>'}</mj-column>
        <mj-column css-class="compact-column" width="50%">${block.children && block.children[1] ? childrenToMJML(block.children[1]) : '<mj-text></mj-text>'}</mj-column>
      </mj-section>`

    case 'col-2-33-67':
      return `<mj-section css-class="compact-section" padding="${block.props.padding}px">
        <mj-column css-class="compact-column" width="33%">${block.children && block.children[0] ? childrenToMJML(block.children[0]) : '<mj-text></mj-text>'}</mj-column>
        <mj-column css-class="compact-column" width="67%">${block.children && block.children[1] ? childrenToMJML(block.children[1]) : '<mj-text></mj-text>'}</mj-column>
      </mj-section>`

    case 'col-2-67-33':
      return `<mj-section css-class="compact-section" padding="${block.props.padding}px">
        <mj-column css-class="compact-column" width="67%">${block.children && block.children[0] ? childrenToMJML(block.children[0]) : '<mj-text></mj-text>'}</mj-column>
        <mj-column css-class="compact-column" width="33%">${block.children && block.children[1] ? childrenToMJML(block.children[1]) : '<mj-text></mj-text>'}</mj-column>
      </mj-section>`

    case 'col-3-33-33-33':
      return `<mj-section css-class="compact-section" padding="${block.props.padding}px">
        <mj-column css-class="compact-column" width="33.33%">${block.children && block.children[0] ? childrenToMJML(block.children[0]) : '<mj-text></mj-text>'}</mj-column>
        <mj-column css-class="compact-column" width="33.33%">${block.children && block.children[1] ? childrenToMJML(block.children[1]) : '<mj-text></mj-text>'}</mj-column>
        <mj-column css-class="compact-column" width="33.33%">${block.children && block.children[2] ? childrenToMJML(block.children[2]) : '<mj-text></mj-text>'}</mj-column>
      </mj-section>`

    // Content blocks
    case 'text':
      const padding = `${block.props.paddingTop || 8}px ${block.props.paddingRight || 16}px ${block.props.paddingBottom || 8}px ${block.props.paddingLeft || 16}px`
      const backgroundColor = block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined

      // Convert newlines to <br> tags if content is plain text
      // If content already has HTML tags, preserve them
      let textContent = block.props.content || ''
      if (textContent && !textContent.includes('<br>') && !textContent.includes('<p>')) {
        // Only convert \n to <br> if there are no existing HTML line break tags
        textContent = textContent.replace(/\n/g, '<br>')
      }

      return `<mj-section css-class="compact-section" ${backgroundColor ? `background-color="${backgroundColor}"` : ''}>
        <mj-column css-class="compact-column">
          <mj-text
            font-size="${block.props.fontSize}px"
            color="${block.props.color}"
            padding="${padding}"
            line-height="${block.props.lineHeight || '1.4'}"
            font-family="${block.props.fontFamily || 'Arial, sans-serif'}"
            font-style="${block.props.fontStyle || 'normal'}"
            font-weight="${block.props.fontWeight || 'normal'}"
            text-decoration="${block.props.textDecoration || 'none'}"
            letter-spacing="${block.props.letterSpacing || 0}px"
            align="${block.props.textAlign || 'left'}"
          >
            ${textContent}
          </mj-text>
        </mj-column>
      </mj-section>`

    case 'button':
      const buttonPadding = `${block.props.paddingTop || 12}px ${block.props.paddingRight || 24}px ${block.props.paddingBottom || 12}px ${block.props.paddingLeft || 24}px`
      const buttonWidth = block.props.width === 'custom' ? `${block.props.customWidth}px` : block.props.width || 'auto'
      const borderStyle = block.props.hasBorder ? `${block.props.borderWidth || 1}px solid ${block.props.borderColor || '#000000'}` : 'none'

      return `<mj-section css-class="compact-section">
        <mj-column css-class="compact-column">
          <mj-button
            href="${block.props.href}"
            background-color="${block.props.backgroundColor || '#3b82f6'}"
            color="${block.props.color || '#ffffff'}"
            padding="${buttonPadding}"
            font-family="${block.props.fontFamily || 'Arial, sans-serif'}"
            font-size="${block.props.fontSize || 16}px"
            font-weight="${block.props.fontWeight || 'normal'}"
            letter-spacing="${block.props.letterSpacing || 0}px"
            border-radius="${block.props.borderRadius || 4}px"
            border="${borderStyle}"
            width="${buttonWidth}"
            align="${block.props.align || 'center'}"
          >
            ${block.props.text}
          </mj-button>
        </mj-column>
      </mj-section>`

    case 'image':
      return `<mj-section css-class="compact-section">
        <mj-column css-class="compact-column">
          <mj-image src="${block.props.src}" alt="${block.props.alt}" width="${block.props.width}px" padding="${block.props.padding}px" />
        </mj-column>
      </mj-section>`

    case 'divider':
      const dividerPadding = `${block.props.paddingTop || 20}px ${block.props.paddingRight || 0}px ${block.props.paddingBottom || 20}px ${block.props.paddingLeft || 0}px`
      const dividerWidth = block.props.width === 'custom' ? `${block.props.customWidth}px` : block.props.width || '100%'
      const dividerBgColor = block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined

      return `<mj-section css-class="compact-section" ${dividerBgColor ? `background-color="${dividerBgColor}"` : ''}>
        <mj-column css-class="compact-column">
          <mj-divider
            border-color="${block.props.borderColor || '#e5e7eb'}"
            border-width="${block.props.height || 4}px"
            border-style="${block.props.style || 'solid'}"
            width="${dividerWidth}"
            padding="${dividerPadding}"
            align="${block.props.align || 'center'}"
          />
        </mj-column>
      </mj-section>`

    case 'spacer':
      const spacerBgColor = block.props.backgroundColor !== 'transparent' ? block.props.backgroundColor : undefined

      return `<mj-section css-class="compact-section" ${spacerBgColor ? `background-color="${spacerBgColor}"` : ''}>
        <mj-column css-class="compact-column">
          <mj-spacer height="${block.props.height}px" />
        </mj-column>
      </mj-section>`

    default:
      return ''
  }
}

export function blocksToMJML(blocks, emailSettings = {}) {
  // Default email settings
  const settings = {
    backgroundColor: '#ffffff',
    contentWidth: 600,
    contentAlign: 'left',
    fontFamily: 'Arial, sans-serif',
    ...emailSettings
  }

  // Ensure blocks is an array
  if (!Array.isArray(blocks)) {
    console.error('[MJML] blocksToMJML: blocks is not an array', blocks)
    return `
      <mjml>
        <mj-body background-color="${settings.backgroundColor}">
          <mj-section>
            <mj-column>
              <mj-text>No content</mj-text>
            </mj-column>
          </mj-section>
        </mj-body>
      </mjml>
    `
  }

  const mjmlBlocks = blocks.map(block => blockToMJML(block)).join('\n')

  // Custom CSS to force left alignment if requested
  let customCss = `
          .compact-section { padding: 0 !important; }
          .compact-column { padding: 0 !important; }
  `

  if (settings.contentAlign === 'left') {
    // Override MJML default centering
    customCss += `
          /* Force left alignment for main container and inner wrappers */
          body > div, div[style*="max-width"], .mj-container {
            max-width: 100% !important;
            width: 100% !important;
          }
          /* Ensure text is left aligned if not overridden */
          .mj-column-per-100 {
            vertical-align: top;
            display: inline-block;
            direction: ltr;
            font-size: 13px;
            text-align: left;
            width: 100% !important;
            max-width: 100% !important;
          }
          /* Reset table widths just in case */
          table { width: 100% !important; }
    `
  }

  // Determine body width
  const bodyWidth = settings.contentAlign === 'left' ? '100%' : '600px'

  return `
    <mjml>
      <mj-head>
        <mj-attributes>
          <mj-section padding="0px" />
          <mj-column padding="0px" />
          <mj-text padding="8px 16px" line-height="1.4" font-family="${settings.fontFamily}" />
          <mj-button padding="8px 16px" font-family="${settings.fontFamily}" />
          <mj-image padding="8px 16px" />
          <mj-divider padding="8px 16px" />
        </mj-attributes>
        <mj-style>
          ${customCss}
        </mj-style>
      </mj-head>
      <mj-body background-color="${settings.backgroundColor}" width="${bodyWidth}">
        ${mjmlBlocks}
      </mj-body>
    </mjml>
  `
}

export function renderHTML(blocks) {
  // Ensure blocks is an array
  if (!Array.isArray(blocks)) {
    console.error('[MJML] renderHTML: blocks is not an array', blocks)
    return '<p style="text-align: center; padding: 40px; color: #999;">Invalid data format</p>'
  }

  if (blocks.length === 0) {
    return '<p style="text-align: center; padding: 40px; color: #999;">No content</p>'
  }

  try {
    // 🔧 SIMPLE APPROACH: Build clean HTML directly from blocks instead of using MJML
    // MJML adds too much complexity with nested tables, making emails hard to read

    const html = buildCleanHTML(blocks)

    console.log('[EMAIL] HTML built and cleaned successfully')
    return html
  } catch (error) {
    console.error('[EMAIL] Render error:', error)
    return '<p style="text-align: center; padding: 40px; color: #f00;">Error rendering email</p>'
  }
}

/**
 * Build clean, simple HTML directly from blocks without using MJML
 * This ensures proper formatting, left alignment, and readability in all email clients
 */
function buildCleanHTML(blocks) {
  let bodyContent = ''

  // Process each block and convert to simple HTML
  for (const block of blocks) {
    switch (block.type) {
      case 'text':
        const text = block.props.content || ''
        const fontSize = block.props.fontSize || 14
        const color = block.props.color || '#333333'
        const textAlign = block.props.textAlign || 'left'

        // Split by newlines and wrap each line in proper formatting
        const lines = text.split('\n').filter(line => line.trim())

        if (lines.length > 0) {
          // Use simple divs with left-align forced with !important
          // NO padding - just margin for spacing between blocks
          bodyContent += `<div style="font-size: ${fontSize}px; color: ${color}; text-align: left !important; line-height: 1.8; margin: 16px 0;">`
          lines.forEach((line) => {
            // Each line as separate paragraph with explicit spacing
            bodyContent += `<p style="margin: 10px 0; padding: 0; text-align: left !important; word-wrap: break-word;">${line}</p>`
          })
          bodyContent += '</div>\n'
        }
        break

      case 'button':
        const btnText = block.props.text || 'Click me'
        const btnUrl = block.props.href || '#'
        const btnBg = block.props.backgroundColor || '#3b82f6'
        const btnColor = block.props.color || '#ffffff'
        const btnAlign = block.props.align || 'center'

        bodyContent += `<div style="text-align: ${btnAlign}; margin: 24px 0; padding: 0;"><a href="${btnUrl}" style="display: inline-block; background-color: ${btnBg}; color: ${btnColor}; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; text-align: center !important;">${btnText}</a></div>\n`
        break

      case 'image':
        const imgSrc = block.props.src || ''
        const imgAlt = block.props.alt || 'Image'
        const imgWidth = block.props.width || 'auto'

        if (imgSrc) {
          bodyContent += `<div style="margin: 20px 0; padding: 0; text-align: left !important;"><img src="${imgSrc}" alt="${imgAlt}" style="max-width: 100%; width: ${imgWidth}px; height: auto; display: block;" /></div>\n`
        }
        break

      case 'divider':
        const borderColor = block.props.borderColor || '#e5e7eb'
        const borderWidth = block.props.borderWidth || 1

        bodyContent += `<div style="margin: 20px 0; padding: 0;"><hr style="border: none; border-top: ${borderWidth}px solid ${borderColor}; margin: 0; padding: 0;" /></div>\n`
        break

      case 'spacer':
        const height = block.props.height || 20
        bodyContent += `<div style="height: ${height}px; padding: 0; margin: 0;"></div>\n`
        break

      // Handle layout blocks (col-1, col-2-50-50, etc)
      case 'col-1':
      case 'col-2-50-50':
      case 'col-2-33-67':
      case 'col-2-67-33':
      case 'col-3-33-33-33':
        // For simplicity, just render children sequentially
        if (block.children && Array.isArray(block.children)) {
          block.children.forEach(childArray => {
            if (Array.isArray(childArray)) {
              childArray.forEach(child => {
                const childHtml = renderSingleBlock(child)
                if (childHtml) bodyContent += childHtml + '\n'
              })
            }
          })
        }
        break

      default:
        break
    }
  }

  // Wrap in clean HTML document with STRONG CSS to override email client defaults
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style type="text/css">
    /* Force left alignment everywhere */
    body, table, td, div, p, span, h1, h2, h3, h4, h5, h6 {
      text-align: left !important;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
      font-size: 14px;
      line-height: 1.8;
      color: #333333;
      margin: 0 !important;
      padding: 0 !important;
      background-color: #ffffff;
      text-align: left !important;
    }

    .email-container {
      background-color: #ffffff;
      width: 100%;
      margin: 0;
      padding: 0;
      border-radius: 0;
      box-shadow: none;
      text-align: left !important;
    }

    .email-body {
      text-align: left !important;
      color: #333333;
      margin: 0;
      padding: 0;
      line-height: 1.8;
    }

    .email-body div {
      text-align: left !important;
      margin: 0;
      padding: 0;
      width: 100%;
      display: block;
    }

    .email-body p {
      text-align: left !important;
      margin: 10px 0 !important;
      padding: 0;
      width: 100%;
      word-wrap: break-word;
      word-break: break-word;
    }

    a {
      color: #0066cc;
      text-decoration: none;
    }

    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="email-body">
      ${bodyContent}
    </div>
  </div>
</body>
</html>`
}

/**
 * Render a single block to HTML
 */
function renderSingleBlock(block) {
  if (!block) return ''

  switch (block.type) {
    case 'text':
      const text = block.props?.content || ''
      const fontSize = block.props?.fontSize || 14
      const color = block.props?.color || '#333333'
      const textAlign = block.props?.textAlign || 'left'

      const lines = text.split('\n').filter(line => line.trim())
      if (lines.length === 0) return ''

      let html = `<div style="font-size: ${fontSize}px; color: ${color}; text-align: ${textAlign}; line-height: 1.6; margin: 12px 0;">`
      lines.forEach((line) => {
        html += `<p style="margin: 8px 0;">${line}</p>`
      })
      html += '</div>'
      return html

    case 'button':
      const btnText = block.props?.text || 'Click me'
      const btnUrl = block.props?.href || '#'
      const btnBg = block.props?.backgroundColor || '#3b82f6'
      const btnColor = block.props?.color || '#ffffff'

      return `<div style="text-align: center; margin: 16px 0;"><a href="${btnUrl}" style="display: inline-block; background-color: ${btnBg}; color: ${btnColor}; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">${btnText}</a></div>`

    case 'image':
      const imgSrc = block.props?.src || ''
      const imgAlt = block.props?.alt || 'Image'
      if (imgSrc) {
        return `<div style="margin: 16px 0;"><img src="${imgSrc}" alt="${imgAlt}" style="max-width: 100%; height: auto;" /></div>`
      }
      return ''

    case 'divider':
      const borderColor = block.props?.borderColor || '#e5e7eb'
      const borderWidth = block.props?.borderWidth || 1
      return `<hr style="border: none; border-top: ${borderWidth}px solid ${borderColor}; margin: 16px 0;" />`

    case 'spacer':
      const height = block.props?.height || 20
      return `<div style="height: ${height}px;"></div>`

    default:
      return ''
  }
}
