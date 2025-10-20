import moment from 'moment'

/**
 * Format date for database storage (MySQL/MariaDB datetime format)
 * Converts any date input to YYYY-MM-DD HH:mm:ss format
 * @param {string|Date|moment} dateValue - Date value to format
 * @returns {string|null} - Formatted date string or null if invalid
 */
export const formatDateForDatabase = (dateValue) => {
  if (!dateValue) return null
  
  try {
    const momentDate = moment(dateValue)
    if (!momentDate.isValid()) return null
    
    // Format as YYYY-MM-DD HH:mm:ss (MySQL datetime format)
    return momentDate.format('YYYY-MM-DD HH:mm:ss')
  } catch (error) {
    console.warn('Failed to format date for database:', dateValue, error)
    return null
  }
}

/**
 * Convert datetime-local input to database format
 * @param {string} localStr - datetime-local input value
 * @returns {string|null} - Database formatted date or null
 */
export const toIsoIfSet = (localStr) => {
  if (!localStr) return null
  return formatDateForDatabase(localStr)
}

/**
 * Format date for display in UI
 * @param {string|Date|moment} dateValue - Date value to format
 * @param {string} format - Moment.js format string (default: 'DD/MM/YYYY HH:mm')
 * @returns {string} - Formatted date string
 */
export const formatDateForDisplay = (dateValue, format = 'DD/MM/YYYY HH:mm') => {
  if (!dateValue) return ''
  
  try {
    const momentDate = moment(dateValue)
    if (!momentDate.isValid()) return ''
    
    return momentDate.format(format)
  } catch (error) {
    console.warn('Failed to format date for display:', dateValue, error)
    return ''
  }
}

/**
 * Convert database datetime to datetime-local input format
 * @param {string} dbDateTime - Database datetime string
 * @returns {string} - datetime-local input format (YYYY-MM-DDTHH:mm)
 */
export const toLocalDatetimeInput = (dbDateTime) => {
  if (!dbDateTime) return ''
  
  try {
    const momentDate = moment(dbDateTime)
    if (!momentDate.isValid()) return ''
    
    // Format for datetime-local input: YYYY-MM-DDTHH:mm
    return momentDate.format('YYYY-MM-DDTHH:mm')
  } catch (error) {
    console.warn('Failed to convert to local datetime input:', dbDateTime, error)
    return ''
  }
}

/**
 * Get current datetime in database format
 * @returns {string} - Current datetime in YYYY-MM-DD HH:mm:ss format
 */
export const getCurrentDatabaseDateTime = () => {
  return moment().format('YYYY-MM-DD HH:mm:ss')
}

/**
 * Add time to a date and return in database format
 * @param {string|Date|moment} dateValue - Base date
 * @param {number} amount - Amount to add
 * @param {string} unit - Unit (days, hours, minutes, etc.)
 * @returns {string} - New date in database format
 */
export const addTimeToDate = (dateValue, amount, unit) => {
  try {
    const momentDate = moment(dateValue)
    if (!momentDate.isValid()) return getCurrentDatabaseDateTime()
    
    return momentDate.add(amount, unit).format('YYYY-MM-DD HH:mm:ss')
  } catch (error) {
    console.warn('Failed to add time to date:', dateValue, amount, unit, error)
    return getCurrentDatabaseDateTime()
  }
}
