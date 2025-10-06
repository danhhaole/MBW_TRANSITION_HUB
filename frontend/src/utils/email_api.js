// mbw_mira/public/js/email_api.js

import { call } from 'frappe-ui'

/**
 * API client for Email operations
 */
export class EmailAPI {
  
  /**
   * Get list of email templates
   * @param {Object} filters - Filter options
   * @param {string} filters.unit_name - Unit name (optional)
   * @param {string} filters.template_type - Template type (optional)
   * @param {number} filters.is_active - Active status (default: 1)
   * @returns {Promise<Object>} API response
   */
  static async getEmailTemplates(filters = {}) {
    try {
      const response = await call('mbw_mira.api.email_api.get_email_templates', filters)
      return response
    } catch (error) {
      console.error('Error fetching email templates:', error)
      throw error
    }
  }

  /**
   * Get specific email template by ID
   * @param {string} templateId - Template ID
   * @returns {Promise<Object>} API response
   */
  static async getEmailTemplate(templateId) {
    try {
      const response = await call('mbw_mira.api.email_api.get_email_template', {
        template_id: templateId
      })
      return response
    } catch (error) {
      console.error('Error fetching email template:', error)
      throw error
    }
  }

  /**
   * Send email to candidate
   * @param {Object} emailData - Email data
   * @param {string} emailData.template_id - Template ID (optional)
   * @param {string} emailData.candidate_id - Candidate ID (optional)
   * @param {string} emailData.to_emails - Recipient emails (comma separated)
   * @param {string} emailData.cc_emails - CC emails (optional)
   * @param {string} emailData.bcc_emails - BCC emails (optional)
   * @param {string} emailData.subject - Email subject
   * @param {string} emailData.content - Email content
   * @param {Array} emailData.attachments - File attachments
   * @param {string} emailData.job_opening_id - Job opening ID (optional)
   * @returns {Promise<Object>} API response
   */
  static async sendCandidateEmail(emailData) {
    try {
      // Convert file attachments to base64 if needed
      const processedAttachments = await this.processAttachments(emailData.attachments || [])
      
      const payload = {
        ...emailData,
        attachments: JSON.stringify(processedAttachments)
      }

      const response = await call('mbw_mira.api.email_api.send_candidate_email', payload)
      return response
    } catch (error) {
      console.error('Error sending email:', error)
      throw error
    }
  }

  /**
   * Save email as draft
   * @param {Object} emailData - Email data (same as sendCandidateEmail)
   * @param {string} draftId - Existing draft ID (optional, for updates)
   * @returns {Promise<Object>} API response
   */
  static async saveEmailDraft(emailData, draftId = null) {
    try {
      const processedAttachments = await this.processAttachments(emailData.attachments || [])
      
      const payload = {
        ...emailData,
        attachments: JSON.stringify(processedAttachments),
        draft_id: draftId
      }

      const response = await call('mbw_mira.api.email_api.save_email_draft', payload)
      return response
    } catch (error) {
      console.error('Error saving draft:', error)
      throw error
    }
  }

  /**
   * Get available email variables
   * @returns {Promise<Object>} API response
   */
  static async getEmailVariables() {
    try {
      const response = await call('mbw_mira.api.email_api.get_email_variables')
      return response
    } catch (error) {
      console.error('Error fetching email variables:', error)
      throw error
    }
  }


    /**
   * Get candidate by name
   * @returns {Promise<Object>} API response
   */
    static async getCandidates() {
      try {
        const response = await call('mbw_mira.api.email_api.get_candidates')
        return response
      } catch (error) {
        console.error('Error fetching email variables:', error)
        throw error
      }
    }
  
  /**
   * Get template types
   * @returns {Promise<Object>} API response
   */
  static async getTemplateTypes() {
    try {
      const response = await call('mbw_mira.api.email_api.get_template_types')
      return response
    } catch (error) {
      console.error('Error fetching template types:', error)
      throw error
    }
  }

  /**
   * Process file attachments - convert File objects to base64
   * @param {Array} attachments - Array of File objects
   * @returns {Promise<Array>} Processed attachments
   */
  static async processAttachments(attachments) {
    if (!attachments || !Array.isArray(attachments)) {
      return []
    }

    const processedAttachments = []

    for (const file of attachments) {
      if (file instanceof File) {
        try {
          const base64Content = await this.fileToBase64(file)
          processedAttachments.push({
            filename: file.name,
            content: base64Content,
            size: file.size,
            type: file.type
          })
        } catch (error) {
          console.error(`Error processing file ${file.name}:`, error)
        }
      } else if (typeof file === 'string') {
        // Assume it's a file URL/path
        processedAttachments.push({
          file_url: file
        })
      }
    }

    return processedAttachments
  }

  /**
   * Convert File object to base64 string
   * @param {File} file - File object
   * @returns {Promise<string>} Base64 string
   */
  static fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        // Remove the data:mime/type;base64, prefix
        const base64 = reader.result.split(',')[1]
        resolve(base64)
      }
      reader.onerror = error => reject(error)
    })
  }

  /**
   * Replace variables in text with actual values
   * @param {string} text - Text containing variables
   * @param {Object} variables - Variable values
   * @returns {string} Text with replaced variables
   */
  static replaceVariables(text, variables = {}) {
    if (!text || typeof text !== 'string') {
      return text
    }

    let result = text
    for (const [key, value] of Object.entries(variables)) {
      const regex = new RegExp(`\\{{${key}\\}}`, 'g')
      result = result.replace(regex, value || '')
    }

    return result
  }

  /**
   * Validate email address
   * @param {string} email - Email address
   * @returns {boolean} Is valid email
   */
  static isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  }

  /**
   * Validate email list (comma separated)
   * @param {string} emails - Comma separated email list
   * @returns {Object} Validation result
   */
  static validateEmailList(emails) {
    if (!emails || !emails.trim()) {
      return { valid: true, emails: [] }
    }

    const emailList = emails.split(',').map(email => email.trim()).filter(email => email)
    const invalidEmails = emailList.filter(email => !this.isValidEmail(email))

    return {
      valid: invalidEmails.length === 0,
      emails: emailList,
      invalidEmails: invalidEmails
    }
  }
}

// Utility functions for use in Vue components
export const emailUtils = {
  /**
   * Format file size for display
   * @param {number} bytes - File size in bytes
   * @returns {string} Formatted file size
   */
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  },

  /**
   * Get file icon based on file type
   * @param {string} filename - File name
   * @returns {string} Icon name
   */
  getFileIcon(filename) {
    const extension = filename.split('.').pop().toLowerCase()
    const iconMap = {
      'pdf': 'file-text',
      'doc': 'file-text',
      'docx': 'file-text',
      'xls': 'file-text', 
      'xlsx': 'file-text',
      'png': 'image',
      'jpg': 'image',
      'jpeg': 'image',
      'gif': 'image'
    }
    return iconMap[extension] || 'file'
  },

  /**
   * Truncate text with ellipsis
   * @param {string} text - Text to truncate
   * @param {number} maxLength - Maximum length
   * @returns {string} Truncated text
   */
  truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) {
      return text
    }
    return text.substring(0, maxLength) + '...'
  }
}

export default EmailAPI