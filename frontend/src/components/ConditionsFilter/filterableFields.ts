import { createResource } from 'frappe-ui'

// Hardcoded fields as fallback - based on Mira Talent DocType
const MIRA_TALENT_FIELDS = [
  // Basic Information
  { label: 'Full Name', fieldname: 'full_name', fieldtype: 'Data' },
  { label: 'Gender', fieldname: 'gender', fieldtype: 'Select', options: 'Male\nFemale\nOther\nUnknown' },
  { label: 'Date of Birth', fieldname: 'date_of_birth', fieldtype: 'Date' },
  { label: 'Email', fieldname: 'email', fieldtype: 'Data' },
  { label: 'Phone', fieldname: 'phone', fieldtype: 'Data' },
  
  // Social Profiles
  { label: 'LinkedIn Profile', fieldname: 'linkedin_profile', fieldtype: 'Data' },
  { label: 'Facebook Profile', fieldname: 'facebook_profile', fieldtype: 'Data' },
  { label: 'Zalo Profile', fieldname: 'zalo_profile', fieldtype: 'Data' },
  
  // Location
  { label: 'City/Address', fieldname: 'current_city', fieldtype: 'Text' },
  
  // Skills & Experience
  { label: 'Skills', fieldname: 'skills', fieldtype: 'Small Text' },
  { label: 'Hard Skills', fieldname: 'hard_skills', fieldtype: 'Small Text' },
  { label: 'Soft Skills', fieldname: 'soft_skills', fieldtype: 'Small Text' },
  { label: 'Domain Expertise', fieldname: 'domain_expertise', fieldtype: 'Small Text' },
  { label: 'Years of Experience', fieldname: 'total_years_of_experience', fieldtype: 'Float' },
  
  // Career Information
  { label: 'Latest Company', fieldname: 'latest_company', fieldtype: 'Small Text' },
  { label: 'Latest Title', fieldname: 'latest_title', fieldtype: 'Text' },
  { label: 'Desired Role', fieldname: 'desired_role', fieldtype: 'Text' },
  { label: 'Highest Education', fieldname: 'highest_education', fieldtype: 'Small Text' },
  
  // Salary & Availability
  { label: 'Current Salary', fieldname: 'current_salary', fieldtype: 'Currency' },
  { label: 'Expected Salary', fieldname: 'expected_salary', fieldtype: 'Currency' },
  { label: 'Work Model', fieldname: 'preferred_work_model', fieldtype: 'Select', options: '\nOn-site\nRemote\nHybrid' },
  { label: 'Availability Date', fieldname: 'availability_date', fieldtype: 'Date' },
  
  // Status & Assessment
  { label: 'Current Status', fieldname: 'current_status', fieldtype: 'Select', options: 'Active\nPassive\nNot Interested\nHired' },
  { label: 'CRM Status', fieldname: 'crm_status', fieldtype: 'Select', options: 'New\nProfiling\nNurturing' },
  { label: 'Recruitment Readiness', fieldname: 'recruitment_readiness', fieldtype: 'Select', options: 'Cold\nWarm\nHot' },
  { label: 'Internal Rating', fieldname: 'internal_rating', fieldtype: 'Select', options: '\nA\nB\nC' },
  { label: 'Cultural Fit', fieldname: 'cultural_fit', fieldtype: 'Select', options: '\nHigh\nMedium\nLow' },
  { label: 'Priority', fieldname: 'priority_level', fieldtype: 'Select', options: '\nHigh\nMedium\nLow' },
  
  // Source & Tracking
  { label: 'Source', fieldname: 'source', fieldtype: 'Select', options: '\nManually\nZalo\nFacebook\nLinkedIn\nReferral\nHeadhunter\nNurturing Interaction\nMBW ATS\nImport Excel\nImport CV' },
  { label: 'Tags', fieldname: 'tags', fieldtype: 'Small Text' },
  { label: 'Recruiter/Owner', fieldname: 'recruiter_owner_id', fieldtype: 'Link', options: 'User' },
  
  // Interaction & Dates
  { label: 'Last Interaction Date', fieldname: 'last_interaction_date', fieldtype: 'Date' },
  { label: 'Created On', fieldname: 'creation', fieldtype: 'Datetime' },
  { label: 'Modified On', fieldname: 'modified', fieldtype: 'Datetime' },
  
  // Email Status
  { label: 'Email Opt Out', fieldname: 'email_opt_out', fieldtype: 'Int' },
  { label: 'Invalid Email', fieldname: 'email_id_invalid', fieldtype: 'Int' },
]

// Create resource to fetch fields from API
export const filterableFieldsResource = createResource({
  url: 'mbw_transition_hub.api.doctype_meta.get_filterable_fields',
  params: {
    doctype: 'Mira Talent'
  },
  auto: false, // Don't auto fetch, will be triggered manually
  initialData: MIRA_TALENT_FIELDS.map((field) => ({
    value: field.fieldname,
    label: field.label,
    fieldname: field.fieldname,
    fieldtype: field.fieldtype,
    options: field.options,
  })),
  transform: (data: any) => {
    // API returns array of fields
    if (data && Array.isArray(data) && data.length > 0) {
      return data
    }
    
    // Fallback to hardcoded fields
    console.warn('Using fallback hardcoded fields for Mira Talent')
    return MIRA_TALENT_FIELDS.map((field) => ({
      value: field.fieldname,
      label: field.label,
      fieldname: field.fieldname,
      fieldtype: field.fieldtype,
      options: field.options,
    }))
  },
  onError: (error: any) => {
    console.error('Failed to fetch filterable fields:', error)
    // Return hardcoded fields on error
    return MIRA_TALENT_FIELDS.map((field) => ({
      value: field.fieldname,
      label: field.label,
      fieldname: field.fieldname,
      fieldtype: field.fieldtype,
      options: field.options,
    }))
  }
})
