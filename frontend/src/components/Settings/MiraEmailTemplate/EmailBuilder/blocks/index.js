import TextBlock from './TextBlock.vue'
import ButtonBlock from './ButtonBlock.vue'
import ImageBlock from './ImageBlock.vue'
import LayoutBlock from './LayoutBlock.vue'
import DividerBlock from './DividerBlock.vue'
import SpacerBlock from './SpacerBlock.vue'

export const blockComponents = {
  text: TextBlock,
  button: ButtonBlock,
  image: ImageBlock,
  divider: DividerBlock,
  spacer: SpacerBlock,
  // Layouts
  'col-1': LayoutBlock,
  'col-2-50-50': LayoutBlock,
  'col-2-33-67': LayoutBlock,
  'col-2-67-33': LayoutBlock,
  'col-3-33-33-33': LayoutBlock,
}

export const defaultBlockProps = {
  // Layouts
  'col-1': { padding: 20 },
  'col-2-50-50': { padding: 20 },
  'col-2-33-67': { padding: 20 },
  'col-2-67-33': { padding: 20 },
  'col-3-33-33-33': { padding: 20 },
  // Content
  text: { 
    content: 'Enter your text here...', 
    // Dimension
    height: null,
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    // Typography
    textType: 'paragraph',
    fontFamily: 'Arial, sans-serif',
    fontSize: 16, 
    color: '#000000',
    lineHeight: '1.4',
    fontStyle: 'normal',
    fontWeight: 'normal',
    textDecoration: 'none',
    letterSpacing: 0,
    // Block
    backgroundColor: 'transparent',
    textAlign: 'left',
    // Legacy
    padding: 20 
  },
  button: { 
    text: 'Click Me', 
    href: 'https://example.com', 
    // Dimension
    width: 'auto',
    customWidth: 200,
    height: null,
    paddingTop: 12,
    paddingBottom: 12,
    paddingLeft: 24,
    paddingRight: 24,
    // Typography
    fontFamily: 'Arial, sans-serif',
    fontSize: 16,
    color: '#ffffff',
    fontWeight: 'normal',
    letterSpacing: 0,
    // Border
    hasBorder: false,
    borderWidth: 1,
    borderColor: '#000000',
    borderRadius: 4,
    // Block
    backgroundColor: '#3b82f6',
    align: 'center',
    // Legacy
    padding: 15 
  },
  image: { 
    // Image settings
    src: '',
    alt: 'Image',
    href: '',
    fileName: '',
    fileSize: null,
    fullWidthMobile: false,
    // Dimension
    widthType: 'fixed',
    width: 600,
    height: null,
    paddingTop: 20,
    paddingBottom: 20,
    paddingLeft: 20,
    paddingRight: 20,
    // Border
    hasBorder: false,
    borderWidth: 1,
    borderColor: '#e5e7eb',
    borderRadius: 0,
    // Block
    backgroundColor: 'transparent',
    align: 'center',
    // Legacy
    padding: 20 
  },
  divider: { 
    // Line
    height: 4,
    style: 'solid',
    borderColor: '#e5e7eb',
    // Dimension  
    width: '100%',
    customWidth: 300,
    paddingTop: 20,
    paddingBottom: 20,
    paddingLeft: 0,
    paddingRight: 0,
    // Block
    backgroundColor: 'transparent',
    align: 'center',
    // Legacy
    borderWidth: 1,
    padding: 20 
  },
  spacer: { 
    height: 40, 
    backgroundColor: 'transparent',
    padding: 0 
  },
}
