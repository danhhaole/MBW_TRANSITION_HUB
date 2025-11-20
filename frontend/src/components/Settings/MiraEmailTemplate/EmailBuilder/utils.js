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
        return `<mj-text font-size="${child.props.fontSize}px" color="${child.props.color}" padding="${child.props.padding}px">${child.props.content}</mj-text>`
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
            ${block.props.content}
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
    contentAlign: 'center',
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
          .compact-section { padding: 0 !important; }
          .compact-column { padding: 0 !important; }
        </mj-style>
      </mj-head>
      <mj-body background-color="${settings.backgroundColor}">
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
    const mjml = blocksToMJML(blocks)
    const { html, errors } = mjml2html(mjml)
    
    if (errors && errors.length > 0) {
      console.warn('[MJML] Rendering errors:', errors)
    }
    
    return html
  } catch (error) {
    console.error('[MJML] Render error:', error)
    return '<p style="text-align: center; padding: 40px; color: #f00;">Error rendering email</p>'
  }
}
