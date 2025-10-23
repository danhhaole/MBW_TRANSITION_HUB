import { createResource } from 'frappe-ui'

// Hardcoded fields as fallback
const MIRA_CONTACT_FIELDS = [
  { label: 'Full Name', fieldname: 'full_name', fieldtype: 'Data' },
  { label: 'Email', fieldname: 'email', fieldtype: 'Data' },
  { label: 'Phone', fieldname: 'phone', fieldtype: 'Data' },
  { label: 'Status', fieldname: 'status', fieldtype: 'Select', options: 'Active\nInactive\nBlacklisted' },
  { label: 'Gender', fieldname: 'gender', fieldtype: 'Select', options: 'Male\nFemale\nOther' },
  { label: 'Date of Birth', fieldname: 'date_of_birth', fieldtype: 'Date' },
  { label: 'Experience Years', fieldname: 'experience_years', fieldtype: 'Int' },
  { label: 'Education Level', fieldname: 'education_level', fieldtype: 'Select', options: 'High School\nBachelor\nMaster\nPhD' },
  { label: 'Current Position', fieldname: 'current_position', fieldtype: 'Data' },
  { label: 'Current Company', fieldname: 'current_company', fieldtype: 'Data' },
  
  // Special fields for Talent Pool filtering
  { label: 'Tag', fieldname: 'tags', fieldtype: 'Link', options: 'Mira Tag' },
  { label: 'Skill', fieldname: 'skills', fieldtype: 'Small Text' },
  { label: 'Source', fieldname: 'source', fieldtype: 'Data' },
  { label: 'Last Interaction', fieldname: 'last_interaction_date', fieldtype: 'Date' },
  
  { label: 'City', fieldname: 'city', fieldtype: 'Data' },
  { label: 'Country', fieldname: 'country', fieldtype: 'Link', options: 'Country' },
  { label: 'Expected Salary', fieldname: 'expected_salary', fieldtype: 'Currency' },
  { label: 'Rating', fieldname: 'rating', fieldtype: 'Rating' },
  { label: 'Created On', fieldname: 'creation', fieldtype: 'Datetime' },
  { label: 'Modified On', fieldname: 'modified', fieldtype: 'Datetime' },
]

// Create resource to fetch fields from API
export const filterableFieldsResource = createResource({
  url: 'mbw_mira.api.doctype_meta.get_filterable_fields',
  params: {
    doctype: 'Mira Talent'
  },
  auto: false, // Don't auto fetch, will be triggered manually
  initialData: MIRA_CONTACT_FIELDS.map((field) => ({
    value: field.fieldname,
    label: field.label,
    fieldname: field.fieldname,
    fieldtype: field.fieldtype,
    options: field.options,
  })),
  transform: (data) => {
    // API returns array of fields
    if (data && Array.isArray(data) && data.length > 0) {
      return data
    }
    
    // Fallback to hardcoded fields
    console.warn('Using fallback hardcoded fields for Mira Talent')
    return MIRA_CONTACT_FIELDS.map((field) => ({
      value: field.fieldname,
      label: field.label,
      fieldname: field.fieldname,
      fieldtype: field.fieldtype,
      options: field.options,
    }))
  },
  onError: (error) => {
    console.error('Failed to fetch filterable fields:', error)
    // Return hardcoded fields on error
    return MIRA_CONTACT_FIELDS.map((field) => ({
      value: field.fieldname,
      label: field.label,
      fieldname: field.fieldname,
      fieldtype: field.fieldtype,
      options: field.options,
    }))
  }
})
